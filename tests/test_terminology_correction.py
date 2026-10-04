"""D003 terminology-correction layer: provider-independent, text-only, no fabrication."""
from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

import terminology_correction as tc


def word(i, text, start, end, punct=None, seg='s1'):
    return {'id': f'w{i:03d}', 'segment_id': seg, 'text': text, 'punctuation': punct,
            'start_s': start, 'end_s': end}


def doc(words=None):
    words = words if words is not None else [
        word(1, ' duplicados', '1/1', '3/2', ','),
        word(2, ' reintentos', '3/2', '4/1', ' y'),
        word(3, ' en', '223/2', '112/1'),
        word(4, ' potencia', '112/1', '113/1', ' y'),
        word(5, ' fallos', '113/1', '229/2', ','),
        word(6, ' parciales', '229/2', '116/1', '.'),
    ]
    return {'schema_version': 1, 'kind': 'source-transcript', 'transcript_id': 'sha256:abc',
            'binding': {'project_id': 'p'}, 'clock': {'name': 'source-presentation-v1'},
            'words': words, 'text': 'x'}


def table(entries, kind='f003-terminology-corrections'):
    return {'schema_version': 1, 'kind': kind, 'entries': entries}


def phrase_entry(eid='term-idempotencia', original='en potencia', replacement='idempotencia'):
    return {'id': eid, 'kind': 'phrase', 'sourceStart': '111.9', 'tolerance_s': '0.6',
            'original': original, 'replacement': replacement,
            'reason': 'ASR produced "en potencia" for the spoken technical term.',
            'reviewer': 'Raúl Almeida'}


class TableValidationTests(unittest.TestCase):
    def test_accepts_valid_phrase_and_word_entries(self):
        t = table([phrase_entry(),
                   {'id': 'acronym-erp', 'kind': 'word', 'sourceStart': '18.44',
                    'tolerance_s': '0.2', 'original': 'RP', 'replacement': 'ERP',
                    'reason': 'Enterprise software acronym in the speech.',
                    'reviewer': 'Raúl Almeida'}])
        self.assertIs(tc.validate_table(t), t)

    def test_rejects_bad_schema_kind_missing_fields_and_duplicates(self):
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table({'schema_version': 2, 'kind': 'f003-terminology-corrections', 'entries': []})
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table({'schema_version': 1, 'kind': 'other', 'entries': []})
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table(table([{'id': 'x', 'kind': 'phrase'}]))          # missing required
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table(table([phrase_entry(), phrase_entry()]))         # duplicate id
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table(table([{**phrase_entry(), 'kind': 'sentence'}]))  # bad kind
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table(table([{**phrase_entry(), 'sourceStart': '-1'}]))
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table(table([{**phrase_entry(), 'original': '   '}]))
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table(table([{**phrase_entry(), 'replacement': ' '}]))

    def test_word_kind_rejects_multi_token_original(self):
        with self.assertRaises(tc.CorrectionError):
            tc.validate_table(table([{**phrase_entry(), 'kind': 'word'}]))


class ApplicationTests(unittest.TestCase):
    def test_phrase_correction_changes_text_only_and_preserves_all_rows(self):
        d = doc()
        before = [dict(w) for w in d['words']]
        view = tc.apply(d, table([phrase_entry()]))

        # Canonical document untouched.
        self.assertEqual(d['words'], before)
        self.assertEqual(len(view['words']), len(d['words']))

        # Timing identical, row by row.
        for src, got in zip(d['words'], view['words']):
            self.assertEqual(src['start_s'], got['start_s'])
            self.assertEqual(src['end_s'], got['end_s'])
        self.assertTrue(tc.verify_timing_preserved(d, view))

        # Recognized text preserved on every row; correction is separate.
        # display_text carries the punctuation that hung off the last absorbed
        # token so the sentence still reads as spoken.
        self.assertEqual(view['words'][2]['text'], ' en')
        self.assertEqual(view['words'][2]['display_text'], 'idempotencia y')
        self.assertEqual(view['words'][2]['punctuation'], None)
        self.assertEqual(view['words'][3]['text'], ' potencia')
        self.assertEqual(view['words'][3]['punctuation'], ' y')
        self.assertIsNone(view['words'][3]['display_text'])
        self.assertEqual(view['words'][3]['absorbed_by'], 'w003')

        # Audit trail carries the human's reason and reviewer, and states no timing change.
        self.assertEqual(len(view['corrections']), 1)
        c = view['corrections'][0]
        self.assertEqual(c['entry_id'], 'term-idempotencia')
        self.assertEqual(c['recognized'], 'en potencia')
        self.assertEqual(c['replacement'], 'idempotencia')
        self.assertEqual(c['reviewer'], 'Raúl Almeida')
        self.assertTrue(c['reason'])
        self.assertIs(c['timing_changed'], False)

        # Corrected display text contains the term, and the misrecognized run is
        # gone as WORDS (not as a substring: 'potencia' is inside 'idempotencia').
        self.assertIn('idempotencia', view['corrected_text'])
        self.assertNotIn('potencia', tc.norm(view['corrected_text']).replace('idempotencia', ''))
        self.assertEqual([w for w in view['words'] if w['display_text']],
                         [view['words'][2]])

        # Guarantees are explicit in the artifact.
        g = view['guarantees']
        self.assertTrue(g['timing_unchanged'] and g['no_words_invented']
                        and g['no_words_deleted'] and g['recognized_text_preserved'])
        self.assertIs(g['canonical_transcript_mutated'], False)

    def test_word_correction_single_token(self):
        words = [word(1, ' una', '1/1', '2/1'), word(2, ' RP', '2/1', '3/1'),
                 word(3, ' de', '3/1', '4/1')]
        d = doc(words)
        t = table([{'id': 'acronym-erp', 'kind': 'word', 'sourceStart': '18.44',
                   'tolerance_s': '0.2', 'original': 'RP', 'replacement': 'ERP',
                   'reason': 'r', 'reviewer': 'Raúl Almeida'}])
        # start_s 2/1 = 2.0 s is NOT near 18.44 s -> no match, must fail loudly
        with self.assertRaises(tc.CorrectionError):
            tc.apply(d, t)
        # Move the word to the right neighbourhood and it matches.
        words[1]['start_s'] = '18.4'
        view = tc.apply(doc(words), t)
        self.assertEqual(view['words'][1]['display_text'], 'ERP')
        self.assertEqual(view['words'][1]['text'], ' RP')

    def test_unmatched_entry_fails_loudly_not_silently(self):
        d = doc()
        with self.assertRaises(tc.CorrectionError) as e:
            tc.apply(d, table([phrase_entry(original='quantum tunnelling')]))
        self.assertIn('matched nothing', str(e.exception))

    def test_ambiguous_entry_fails_instead_of_picking_one(self):
        # Same phrase twice inside the tolerance window -> ambiguous.
        words = [word(1, ' en', '111.8', '111.9'), word(2, ' potencia', '111.9', '112.0'),
                 word(3, ' en', '112.0', '112.1'), word(4, ' potencia', '112.1', '112.2')]
        d = doc(words)
        with self.assertRaises(tc.CorrectionError) as e:
            tc.apply(d, table([phrase_entry()]))
        self.assertIn('ambiguous', str(e.exception))

    def test_empty_table_is_a_clean_passthrough(self):
        d = doc()
        view = tc.apply(d, table([]))
        self.assertEqual(view['corrections'], [])
        self.assertTrue(all(w['display_text'] is None and w['absorbed_by'] is None
                            for w in view['words']))
        self.assertEqual(view['corrected_text'], ''.join(tc._token_text(w) for w in d['words']))
        self.assertTrue(tc.verify_timing_preserved(d, view))

    def test_rejects_non_transcript_and_wordless_documents(self):
        with self.assertRaises(tc.CorrectionError):
            tc.apply({'kind': 'other'}, table([phrase_entry()]))
        with self.assertRaises(tc.CorrectionError):
            tc.apply({'kind': 'source-transcript', 'words': None}, table([phrase_entry()]))

    def test_case_and_punctuation_insensitive_matching(self):
        words = [word(1, ' En', '111.85', '111.95', '.'),
                 word(2, ' POTENCIA', '111.95', '112.1', ',')]
        view = tc.apply(doc(words), table([phrase_entry()]))
        # Case/punctuation are ignored when matching; the replacement carries the
        # punctuation that hung off the last absorbed token.
        self.assertEqual(view['words'][0]['display_text'], 'idempotencia,')
        self.assertEqual(view['words'][0]['text'], ' En')
        self.assertEqual(view['words'][1]['absorbed_by'], 'w001')

    def test_replacement_inherits_leading_space_so_words_do_not_run_together(self):
        """Regression: vendor tokens carry a leading space; a replacement must keep it."""
        d = doc()
        view = tc.apply(d, table([phrase_entry()]))
        self.assertIn(' y idempotencia y', view['corrected_text'])
        self.assertNotIn('yidempotencia', view['corrected_text'])

    def test_module_is_provider_free(self):
        """D003/Constitution S35: no vendor, endpoint, credential or transport vocabulary."""
        src = (ROOT / 'tools' / 'terminology_correction.py').read_text().lower()
        for banned in ('alibaba', 'qwen', 'dashscope', 'whisper', 'oss', 'http',
                       'endpoint', 'api_key', 'apikey', 'bearer', 'signature'):
            self.assertNotIn(banned, src, f'provider vocabulary leaked: {banned}')


if __name__ == '__main__':
    unittest.main()
