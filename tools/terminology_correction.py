#!/usr/bin/env python3
"""D003 — deterministic, human-reviewed terminology-correction layer.

Provider-independent (Constitution S35): this module knows nothing about any STT
vendor, service, credential or transport. It consumes a `source-transcript v1`
document and produces a corrected VIEW plus an audit report.

Non-negotiable properties, each covered by tests:

- The canonical transcript is never mutated. This module only reads it.
- Timing is never moved. Word start/end pass through byte-identically.
- No word is invented and none is deleted. A word absorbed into a corrected
  phrase keeps its row, its timing and its recognized text; it is only marked
  `absorbed_by` so display consumers skip it.
- Every recognized token keeps its original text in `text`; the correction lives
  in a separate `display_text`.
- An entry that matches nothing, or matches ambiguously, FAILS loudly instead of
  being silently ignored. Silent no-ops are how wrong subtitles ship.

Entry schema (data, reviewed by a human, never code):

    {
      "id": "term-idempotencia",
      "kind": "phrase",            # "word" | "phrase"
      "sourceStart": 111.9,        # seconds in the SOURCE clock
      "tolerance_s": 0.6,          # match window around sourceStart
      "original": "en potencia",   # exact recognized text, space-joined
      "replacement": "idempotencia",
      "reason": "...",             # why this is what was spoken
      "reviewer": "Raúl Almeida"   # human who approved the entry
    }

`kind: "word"` replaces a single recognized token with a single token (the form
proven in production by MotionGraphics 006). `kind: "phrase"` replaces a run of
consecutive tokens inside the window with one replacement string, marking the
extra tokens as absorbed. Both are text-only.
"""
from __future__ import annotations

import json
import sys
import unicodedata
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

SCHEMA_VERSION = 1
KIND = 'terminology-corrected-transcript-view'
REQUIRED_ENTRY = ('id', 'kind', 'sourceStart', 'tolerance_s', 'original',
                  'replacement', 'reason', 'reviewer')


class CorrectionError(Exception):
    """Raised for a malformed table or an entry that cannot be applied safely."""


def now_utc():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def norm(text):
    """Comparison-only normalization. Never written into any artifact."""
    text = unicodedata.normalize('NFC', text or '')
    text = text.casefold()
    return ' '.join(''.join(' ' if unicodedata.category(c).startswith('P') else c
                            for c in text).split())


def fraction(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(str(value))
    if isinstance(value, str):
        return Fraction(value)
    raise CorrectionError(f'unrepresentable time value: {value!r}')


def validate_table(table):
    """Strict validation. A table is data owned by a human reviewer."""
    if not isinstance(table, dict) or table.get('schema_version') != SCHEMA_VERSION:
        raise CorrectionError('table schema_version must be 1')
    if table.get('kind') != 'f003-terminology-corrections':
        raise CorrectionError('table kind must be f003-terminology-corrections')
    entries = table.get('entries')
    if not isinstance(entries, list):
        raise CorrectionError('table entries must be a list')
    seen = set()
    for e in entries:
        if not isinstance(e, dict):
            raise CorrectionError('entry must be an object')
        missing = [k for k in REQUIRED_ENTRY if k not in e or e[k] in (None, '')]
        if missing:
            raise CorrectionError(f'entry {e.get("id")!r} missing {missing}')
        if e['kind'] not in ('word', 'phrase'):
            raise CorrectionError(f'entry {e["id"]!r} kind must be word|phrase')
        if e['id'] in seen:
            raise CorrectionError(f'duplicate entry id {e["id"]!r}')
        seen.add(e['id'])
        for key in ('sourceStart', 'tolerance_s'):
            try:
                v = fraction(e[key])
            except (CorrectionError, ValueError, ZeroDivisionError) as exc:
                raise CorrectionError(f'entry {e["id"]!r} {key} invalid: {exc}') from exc
            if v < 0:
                raise CorrectionError(f'entry {e["id"]!r} {key} must be >= 0')
        if not norm(e['original']):
            raise CorrectionError(f'entry {e["id"]!r} original is empty after normalization')
        if not str(e['replacement']).strip():
            raise CorrectionError(f'entry {e["id"]!r} replacement is blank')
        if len(norm(e['original']).split()) != 1 and e['kind'] == 'word':
            raise CorrectionError(f'entry {e["id"]!r} kind=word requires a single-token original')
    return table


def _token_text(word):
    """Recognized token text for DISPLAY: text plus any attached punctuation."""
    return (word.get('text') or '') + (word.get('punctuation') or '')


def _match_text(word):
    """Recognized token text for MATCHING: the word field only.

    In source-transcript v1, `text` and `punctuation` are separate fields, so
    matching a recognized phrase must not swallow the punctuation that happens
    to hang off the last token. This mirrors the production rule proven in
    MotionGraphics 006, which compares the recognized word alone.
    """
    return word.get('text') or ''


def apply(doc, table):
    """Produce a corrected view of `doc`. `doc` is never mutated."""
    if not isinstance(doc, dict) or doc.get('kind') != 'source-transcript':
        raise CorrectionError('doc must be a source-transcript v1 document')
    words = doc.get('words')
    if not isinstance(words, list):
        raise CorrectionError('transcript has no word-level timing; nothing to correct')
    validate_table(table)

    audit, corrected_words = [], []
    for w in words:
        corrected_words.append({
            'id': w.get('id'),
            'segment_id': w.get('segment_id'),
            'text': w.get('text'),
            'punctuation': w.get('punctuation'),
            'start_s': w.get('start_s'),
            'end_s': w.get('end_s'),
            'display_text': None,
            'absorbed_by': None,
            'corrected_by': None,
        })

    for e in table['entries']:
        start = fraction(e['sourceStart'])
        tol = fraction(e['tolerance_s'])
        target = norm(e['original'])
        n_target = len(target.split())

        # Candidate windows: consecutive runs of n_target words whose FIRST word
        # starts inside [start - tol, start + tol] and whose joined text matches.
        hits = []
        for i, w in enumerate(words):
            if w.get('start_s') is None:
                continue
            ws = fraction(w['start_s'])
            if abs(ws - start) > tol:
                continue
            run = words[i:i + n_target]
            if len(run) != n_target or any(r.get('start_s') is None for r in run):
                continue
            if norm(' '.join(_match_text(r) for r in run)) == target:
                hits.append(i)

        if not hits:
            raise CorrectionError(
                f'entry {e["id"]!r} matched nothing: no {n_target}-token run '
                f'"{e["original"]}" within {float(tol)}s of {float(start)}s')
        if len(hits) > 1:
            raise CorrectionError(
                f'entry {e["id"]!r} is ambiguous: matched at word indices {hits}; '
                'narrow tolerance_s or make original more specific')

        i = hits[0]
        last = i + n_target - 1
        first = corrected_words[i]
        # The replacement carries the punctuation that hung off the LAST absorbed
        # token, so the corrected sentence still reads as spoken. Each row keeps
        # its own recognized `punctuation` untouched.
        trailing = corrected_words[last].get('punctuation') or ''
        first['display_text'] = e['replacement'] + trailing
        first['corrected_by'] = e['id']
        absorbed = []
        for j in range(i + 1, i + n_target):
            row = corrected_words[j]
            row['absorbed_by'] = first['id']
            row['corrected_by'] = e['id']
            absorbed.append(row['id'])

        audit.append({
            'entry_id': e['id'],
            'kind': e['kind'],
            'word_id': first['id'],
            'absorbed_word_ids': absorbed,
            'recognized': ' '.join((_match_text(w) or '').strip() for w in words[i:i + n_target]),
            'replacement': e['replacement'],
            'reason': e['reason'],
            'reviewer': e['reviewer'],
            'matched_start_s': words[i]['start_s'],
            'matched_end_s': words[i + n_target - 1]['end_s'],
            'timing_changed': False,
        })

    # Corrected full text for display consumers: skip absorbed tokens, prefer
    # display_text. The original `text` field of the doc is left untouched.
    # Vendor tokens carry a leading space, so a replacement inherits the spacing
    # of the token it replaces; otherwise words would run together.
    parts = []
    for c in corrected_words:
        if c['absorbed_by'] is not None:
            continue
        if c['display_text'] is not None:
            lead = ' ' if (c['text'] or '').startswith(' ') else ''
            parts.append(lead + c['display_text'])
        else:
            parts.append(_token_text(c))
    corrected_text = ''.join(parts)

    return {
        'schema_version': SCHEMA_VERSION,
        'kind': KIND,
        'derived_from': {
            'transcript_id': doc.get('transcript_id'),
            'binding': doc.get('binding'),
            'clock': doc.get('clock'),
        },
        'generated_at_utc': now_utc(),
        'table': {
            'kind': table['kind'],
            'entry_ids': [e['id'] for e in table['entries']],
            'entries': table['entries'],
        },
        'corrections': audit,
        'words': corrected_words,
        'corrected_text': corrected_text,
        'guarantees': {
            'timing_unchanged': True,
            'no_words_invented': True,
            'no_words_deleted': True,
            'recognized_text_preserved': True,
            'canonical_transcript_mutated': False,
        },
        'unknowns': {
            '/acoustic_accuracy_of_replacement': ('UNRESOLVED: a human reviewer asserted the replacement '
                                                  'from the assembled preview; no acoustic re-measurement is claimed'),
        },
    }


def verify_timing_preserved(doc, view):
    """Cheap invariant check consumers may run before trusting a view."""
    src = {w['id']: (w['start_s'], w['end_s']) for w in doc['words'] if w.get('id')}
    got = {c['id']: (c['start_s'], c['end_s']) for c in view['words']}
    if set(src) != set(got) or any(src[k] != got[k] for k in src):
        raise CorrectionError('view does not preserve word timing')
    return True


def _load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _dump_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def main(argv=None):
    """Standalone CLI: transcript + table -> corrected view artifact.

    Reads a canonical `source-transcript v1` document and a human-reviewed
    corrections table, writes a corrected VIEW (never mutating the transcript),
    then verifies the timing invariant before exiting. Exit 0 on success, 2 on a
    correction/validation error. This module stays free of any provider
    vocabulary: it does not know which engine produced the transcript.
    """
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--transcript', required=True)
    parser.add_argument('--table', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    try:
        doc = _load_json(args.transcript)
        table = _load_json(args.table)
        view = apply(doc, table)
        verify_timing_preserved(doc, view)
        _dump_json(args.output, view)
    except (CorrectionError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({'operation': 'correct', 'outcome': 'STOPPED',
                          'error': str(exc)}, ensure_ascii=False))
        return 2
    summary = {'operation': 'correct', 'outcome': 'CORRECTED',
               'transcript_id': view['derived_from']['transcript_id'],
               'corrections_applied': len(view['corrections']),
               'words': len(view['words']),
               'timing_unchanged': view['guarantees']['timing_unchanged'],
               'canonical_transcript_mutated': view['guarantees']['canonical_transcript_mutated'],
               'output': str(Path(args.output).resolve())}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
