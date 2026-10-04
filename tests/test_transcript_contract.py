"""Independent Fraction/JSON consumer oracles; GENERATED TEST DATA, no network."""
from __future__ import annotations
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import transcript_contract as c
import transcribe as orchestration
from content_contract import ContractError, canonical_bytes, digest


def inputs(zero='1/4'):
    b={'project_id':'synthetic','source_id':'sha256:'+'a'*64,'source_sha256':'a'*64,
       'project_manifest_sha256':'b'*64,'inspection_sha256':'c'*64,'clock_id':'d'*64,'audio_stream_index':1}
    p={'audio_zero_source_s':zero,'duration_s':'3/1'}
    prov={'execution_id':'opaque-execution','response_sha256':'e'*64,'request_fingerprint':'f'*64,'audio_sha256':'1'*64,'preparation_sha256':'2'*64}
    info={'timing':{'audio_start_s':zero,'audio_end_s':str(Fraction(zero)+3)+'/1' if (Fraction(zero)+3).denominator==1 else str(Fraction(zero)+3), 'video_end_s':'4/1'}}
    if '/' not in info['timing']['audio_end_s']: info['timing']['audio_end_s']+='/1'
    generic={'text':'Again. try again, try again.', 'resolution_s':'1/1000','segments':[
        {'text':'Again.', 'start_s':'1/10','end_s':'1/2','words':[{'text':'Again','punctuation':'.','start_s':'1/10','end_s':'11/20'}]},
        {'text':'try again, try again.', 'start_s':'3/5','end_s':'14/5','words':[
            {'text':' try ','punctuation':'','start_s':'3/5','end_s':'9/10'},
            {'text':'again','punctuation':', ','start_s':'9/10','end_s':'6/5'},
            {'text':'try ','punctuation':'','start_s':'8/5','end_s':'2/1'},
            {'text':'again','punctuation':'.','start_s':'2/1','end_s':'14/5'}]}]}
    return generic,b,p,prov,{'declared':'es','requested':['es','en']},info


def reidentify(doc):
    doc['transcript_id']='sha256:'+digest({k:v for k,v in doc.items() if k!='transcript_id'})


class TranscriptTests(unittest.TestCase):
    def review_fixture(self):
        args=list(inputs('0/1'));starts=[0,60,90,130,195];ends=[25,85,115,155,228]
        g={'text':'','resolution_s':'1/1000','segments':[]};windows=[]
        for wi,start in enumerate(starts):
            lexical=['voz']*40
            if wi==1:lexical[10:14]=['monolito','microservicios','eventos','idempotencia']
            if wi==2:lexical[20]='Again'
            if wi==3:lexical[10:14]=['try','again','try','again']
            words=[]
            for j,text in enumerate(lexical):
                a=Fraction(start)+Fraction(1,10)+j*Fraction(11,20);b=a+Fraction(1,5)
                words.append({'text':text,'punctuation':' ' if j<39 else '.', 'start_s':f'{a.numerator}/{a.denominator}','end_s':f'{b.numerator}/{b.denominator}'})
            text=''.join(w['text']+w['punctuation'] for w in words)
            # Preserve whitespace supplied by this test provider, including inter-sentence space.
            if wi<4:
                words[-1]['punctuation']+=" ";text+=' '
            g['segments'].append({'text':text,'start_s':words[0]['start_s'],'end_s':words[-1]['end_s'],'words':words})
            windows.append({'start_s':f'{start}/1','end_s':f'{ends[wi]}/1','text':text})
        g['text']=' '.join(s['text'] for s in g['segments']);args[0]=g;args[2]['duration_s']='1164/5'
        args[5]['timing'].update(audio_end_s='1164/5',video_end_s='1164/5')
        doc=c.normalize(*args);controls=[]
        def add(wi,j,group,critical=False):
            w=g['segments'][wi]['words'][j];a,b=map(Fraction,(w['start_s'],w['end_s']))
            r=lambda f:f'{f.numerator}/{f.denominator}'
            controls.append({'id':f'c{wi}-{j}','window_index':wi,'lexical_index':j,'text':w['text'],
                'group':group,'critical':critical,'onset_bounds_s':[r(a-Fraction(1,100)),r(a+Fraction(1,100))],
                'offset_bounds_s':[r(b-Fraction(1,100)),r(b+Fraction(1,100))]})
        for wi,group in ((0,'opening'),(2,'correction'),(4,'ending')):
            for j in range(10):add(wi,j,group)
        add(2,20,'additional',True)
        for j in range(10,14):add(3,j,'additional',True)
        for j in range(10,14):add(1,j,'additional')
        refs={'schema_version':1,'kind':'f003-human-reference','binding':doc['binding'],'candidate_seen':False,
              'status':'OWNER_CONFIRMED','reviewer':'GENERATED TEST DATA','method':'synthetic oracle', 'windows':windows,'controls':controls,
              'terms':dict(zip(('monolito','microservicios','eventos','idempotencia'),('c1-10','c1-11','c1-12','c1-13'))),
              'pauses':[{'kind':'before-again','start_s':'403/4','end_s':'1011/10'},
                        {'kind':'after-again','start_s':'1013/10','end_s':'2033/20'},
                        {'kind':'natural','start_s':'43/4','end_s':'111/10'}],
              'incorrect_statement':'preserve incorrect speech','corrected_statement':'preserve correction'}
        return doc,refs

    def test_quantitative_review_wer_timing_and_independent_counts(self):
        doc,refs=self.review_fixture();report=orchestration.evaluate(doc,refs)
        self.assertEqual(report['wer'],{'S':0,'D':0,'I':0,'N':200,'ratio':'0/1'})
        self.assertEqual(report['result'],'HUMAN_REVIEW_REQUIRED')
        self.assertEqual(report['ordinary_p95_s'],'1/100');self.assertEqual(report['drift_s'],{'onset':'0/1','offset':'0/1'})
        # External hand-worked Levenshtein oracle: one substitution/deletion/insertion.
        counts,_=orchestration.edit_alignment(['a','b','c'],['a','x','c','d'])
        self.assertEqual(counts,{'S':1,'D':0,'I':1,'N':3})
        counts,_=orchestration.edit_alignment(['a','b','c'],['a','c']);self.assertEqual(counts['D'],1)
        broken=copy.deepcopy(doc);broken['words'][100]['text']='Thank you';reidentify(broken)
        report=orchestration.evaluate(broken,refs)
        self.assertEqual(report['result'],'FAIL');self.assertTrue(any('CONTROL_MISSING' in x for x in report['failures']))

    def test_reference_no_candidate_unknown_bounds_duplicates_and_minimum(self):
        doc,refs=self.review_fixture()
        for mutate in (lambda r:r.update(candidate_seen=True),lambda r:r['controls'][0].update(onset_bounds_s=['0/1','1/5']),
                       lambda r:r['controls'][1].update(lexical_index=0),lambda r:r['windows'][0].update(text='too short')):
            r=copy.deepcopy(refs);mutate(r)
            with self.assertRaises(ContractError):orchestration.validate_reference(r,doc['binding'])

    def test_independent_wire_consumer_mapping_crossing_and_provider_free(self):
        doc=c.normalize(*inputs()); raw=canonical_bytes(doc)
        # Consumer below imports JSON/hashlib/Fraction only; assertions don't use adapter/normalizer helpers.
        wire=json.loads(raw)
        identity=dict(wire); tid=identity.pop('transcript_id')
        expected_bytes=(json.dumps(identity,ensure_ascii=False,allow_nan=False,sort_keys=True,indent=2)+'\n').encode()
        self.assertEqual(tid,'sha256:'+hashlib.sha256(expected_bytes).hexdigest())
        self.assertEqual(Fraction(wire['words'][0]['start_s']),Fraction(1,4)+Fraction(100,1000))
        self.assertEqual(Fraction(wire['words'][0]['end_s']),Fraction(1,4)+Fraction(550,1000))
        self.assertGreater(Fraction(wire['words'][0]['end_s']),Fraction(wire['segments'][0]['end_s']))
        self.assertEqual([w['text'].strip().casefold() for w in wire['words']],['again','try','again','try','again'])
        self.assertEqual(wire['clock']['name'],'source-presentation-v1'); self.assertEqual(wire['readiness']['status'],'READY')
        for forbidden in ('provider','model','pricing','task_id','retake','caption','semantic','edl'):
            self.assertNotIn('"'+forbidden+'"',raw.decode())
        self.assertIsNone(wire['language']['detected']); self.assertIsNone(wire['words'][0]['confidence'])
        self.assertEqual(canonical_bytes(c.normalize(*inputs())),raw)

    def test_second_provider_decimal_seconds_double_same_domain(self):
        args=list(inputs()); g=args[0]
        # A fictional provider returns decimal seconds; its test adapter uses Fraction externally.
        fictional={'start':'0.100','finish':'0.550','unit':'seconds'}
        g['segments'][0]['words'][0].update(start_s=f'{Fraction(fictional["start"]).numerator}/{Fraction(fictional["start"]).denominator}',
            end_s=f'{Fraction(fictional["finish"]).numerator}/{Fraction(fictional["finish"]).denominator}')
        args[0]=g
        self.assertEqual(canonical_bytes(c.normalize(*args)),canonical_bytes(c.normalize(*inputs())))

    def test_missing_words_times_and_punctuation_unknown_distinct_from_empty(self):
        for mutate in (lambda g:g['segments'][0].update(words=None),
                       lambda g:g['segments'][0]['words'][0].update(start_s=None)):
            args=list(inputs()); mutate(args[0]); doc=c.normalize(*args)
            self.assertNotEqual(doc['readiness']['status'],'READY'); self.assertTrue(doc['unknowns'])
        args=list(inputs()); args[0]['segments'][0]['words'][0]['punctuation']=None
        doc=c.normalize(*args)
        self.assertEqual(doc['unknowns']['/words/0/punctuation'],'NOT_REPORTED')
        self.assertNotIn('/words/1/punctuation',doc['unknowns'])

    def test_negative_audio_preserved_outside_video_review(self):
        args=inputs('-1/4'); doc=c.normalize(*args)
        self.assertEqual(Fraction(doc['words'][0]['start_s']),Fraction(-3,20))
        self.assertEqual(doc['readiness']['status'],'NEEDS_REVIEW')
        self.assertIn('OUTSIDE_VIDEO',[r['code'] for r in doc['readiness']['reasons']])

    def test_not_repairing_mismatch_nonmonotonic_zero_and_bounds(self):
        for mutate,expected in ((lambda g:g.update(text='different'),'NEEDS_REVIEW'),
            (lambda g:g['segments'][1]['words'][0].update(start_s='0/1'),'INVALID'),
            (lambda g:g['segments'][0]['words'][0].update(end_s='1/10'),'INVALID'),
            (lambda g:g['segments'][1]['words'][-1].update(end_s='4/1'),'INVALID')):
            args=list(inputs()); mutate(args[0]); doc=c.normalize(*args)
            self.assertEqual(doc['readiness']['status'],expected)
            self.assertEqual(doc['text'],args[0]['text'])

    def test_closed_schema_unknowns_hash_ids_rationals_and_extensions(self):
        original=c.normalize(*inputs())
        mutations=[lambda d:d.update(schema_version=True),lambda d:d.update(kind='qwen'),lambda d:d.update(new_core=1),
            lambda d:d['words'][1].update(id='w000001'),lambda d:d['clock'].update(audio_zero_source_s=0.25),
            lambda d:d['words'][0].update(start_s='2/2'),lambda d:d['words'][0].update(confidence=float('nan')),
            lambda d:d['unknowns'].clear(),lambda d:d['extensions'].update(unscoped={}),
            lambda d:d['provenance'].update(audio_sha256='wrong')]
        for mutate in mutations:
            doc=copy.deepcopy(original);mutate(doc)
            with self.assertRaises((ContractError,ValueError)):
                reidentify(doc); c.validate(doc)
        doc=copy.deepcopy(original); doc['extensions']={'org.example.inert':{'future':None}}; reidentify(doc); c.validate(doc)
        doc=copy.deepcopy(original);doc['text']='tampered'
        with self.assertRaises(ContractError):c.validate(doc)

if __name__=='__main__':unittest.main()
