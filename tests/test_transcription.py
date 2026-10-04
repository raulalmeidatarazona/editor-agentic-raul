"""F003 journal/payment/replay offline integration. GENERATED TEST DATA only."""
from __future__ import annotations
import copy
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_audio_preparation import ROOT, generated_project
from test_qwen_asr_adapter import settings, result_payload, pricing
import audio_preparation as audio
import qwen_asr_adapter as v
import transcribe as t
import transcript_contract as domain
from content_contract import ContractError, atomic_json, canonical_bytes, hash_file, load_json, verify_project

URL='https://test.oss-ap-southeast-1.aliyuncs.com/audio?Expires=9999999999&OSSAccessKeyId=ID&Signature=URL_CANARY'
RESULT='https://test.oss-ap-southeast-1.aliyuncs.com/result?Expires=9999999999&OSSAccessKeyId=ID&Signature=RESULT_CANARY'


class FakeHTTP:
    """No urllib or socket, even when a test passes the opt-in flag."""
    def __init__(self,terminal='SUCCEEDED',failure=None,result=None):
        self.key='KEY_CANARY';self.calls=[];self.terminal=terminal;self.failure=failure;self.result=result
        self.clock=lambda:0;self.sleep=lambda _:None
    def transport(self,url,sha,bytes):
        self.calls.append('transport');return {'sha256':sha,'bytes':bytes,'status':'VERIFIED','host':'test.oss-ap-southeast-1.aliyuncs.com'}
    def request(self,method,url,body=None,authenticated=False,deadline=None):
        self.calls.append(method)
        if self.failure=='post' and method=='POST':raise ContractError('SUBMISSION_UNKNOWN','test')
        if method=='POST':return canonical_bytes({'request_id':'submit-id','output':{'task_id':'job-id','task_status':'PENDING'},'echo':URL})
        if '/tasks/' in url:
            if self.failure=='query':raise ContractError('GET_RETRIES_EXHAUSTED','test')
            rows=[{'file_url':URL,'transcription_url':RESULT,'subtask_status':'SUCCEEDED' if self.failure!='partial' else 'FAILED'}]
            if self.failure=='multiple':rows=rows*2
            return canonical_bytes({'request_id':'query-id','output':{'task_id':'job-id','task_status':self.terminal,'results':rows},'usage':{'duration':2}})
        if self.failure=='download':raise ContractError('GET_RETRIES_EXHAUSTED','test')
        if self.failure=='malformed':return b'{bad KEY_CANARY'
        result=self.result or result_payload();result=copy.deepcopy(result);result['file_url']=URL
        return canonical_bytes(result)


class TranscriptionTests(unittest.TestCase):
    def setUp(self):
        parent=ROOT/'.local/validation/F003/tests';parent.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=parent);self.base=Path(self.temp.name)
        self.root=generated_project(self.base);self.s=settings()
        self.review=self.base/'review.json';atomic_json(self.review,{'generated_test_data':True})
        self.env=patch.dict(os.environ,{'F003_AUDIO_URL':URL});self.env.start()
        # Prevent all accidental real HTTP. Tests use an injected provider double exclusively.
        self.network=patch('urllib.request.OpenerDirector.open',side_effect=AssertionError('NETWORK DISABLED'));self.network.start()
        self.permission=patch.object(t,'approval',return_value={'generated_test_data':True,'max_submissions':1});self.permission.start()
        self.human=patch.object(t,'human_gate',return_value={'pricing_snapshot':pricing()});self.human.start()
    def tearDown(self):
        self.human.stop();self.permission.stop();self.network.stop();self.env.stop();self.temp.cleanup()
    def run_submit(self,http=None,hook=None):
        return t.submit(self.root,self.s,True,'test',self.review,http or FakeHTTP(),hook)
    def attempt(self):return next((self.root/'transcription/requests').glob('*/attempts/*'))

    def test_complete_replay_guard_noop_without_network_or_artifact_writes(self):
        http=FakeHTTP();out=self.run_submit(http);self.assertEqual(out['status'],'READY')
        self.assertEqual(http.calls,['transport','POST','GET','GET'])
        doc=domain.verify_transcript(self.root)
        self.assertEqual(doc['clock']['audio_zero_source_s'],'1/4')
        self.assertEqual(doc['words'][0]['start_s'],'11/20')
        before={p:(hash_file(p),p.stat().st_mtime_ns) for p in (self.root/'transcription').rglob('*') if p.is_file()}
        n=FakeHTTP();self.assertEqual(self.run_submit(n)['outcome'],'NO_OP');self.assertEqual(n.calls,[])
        self.assertEqual(before,{p:(hash_file(p),p.stat().st_mtime_ns) for p in before})
        first=Path(out['path']);data=first.read_bytes();first.chmod(0o644);first.unlink()
        regenerated=t.normalize_attempt(self.root,self.attempt());self.assertEqual(Path(regenerated['path']).read_bytes(),data)
        changed=t.normalize_attempt(self.root,self.attempt(),'test-normalizer-version-2')
        self.assertNotEqual(out['path'],changed['path']);self.assertEqual(first.read_bytes(),data)
        self.assertEqual(http.calls,['transport','POST','GET','GET'])
        persisted=b''.join(p.read_bytes() for p in (self.root/'transcription').rglob('*') if p.is_file() and p.suffix in ('.json','.md'))
        for secret in (b'KEY_CANARY',b'URL_CANARY',b'RESULT_CANARY'):self.assertNotIn(secret,persisted)

    def test_crash_intent_before_and_after_post_never_automatically_resubmits(self):
        class Crash(BaseException):pass
        for point in ('after_submit_intent','after_post_before_task'):
            base=self.base/point;root=generated_project(base);http=FakeHTTP()
            def hook(where,attempt):
                if where==point:raise Crash()
            with self.assertRaises(Crash):t.submit(root,self.s,True,'test',self.review,http,hook)
            attempt=next((root/'transcription/requests').glob('*/attempts/*'))
            self.assertEqual(load_json(attempt/'execution.json')['phase'],'SUBMIT_INTENT')
            next_http=FakeHTTP()
            with self.assertRaises(ContractError) as e:t.submit(root,self.s,True,'test',self.review,next_http)
            self.assertEqual(e.exception.code,'PAID_ATTEMPT_ALREADY_CONSUMED');self.assertEqual(next_http.calls,[])
            with self.assertRaises(ContractError):t.collect(root,attempt,next_http)
            self.assertEqual(next_http.calls,[])

    def test_failed_ambiguous_partial_malformed_empty_no_ready_no_second_post(self):
        for failure in ('post','partial','multiple','malformed','download'):
            root=generated_project(self.base/failure);http=FakeHTTP(failure=failure)
            with self.assertRaises(ContractError):t.submit(root,self.s,True,'test',self.review,http)
            self.assertNotEqual(load_json(root/'transcription/current.json')['status'],'READY')
            n=FakeHTTP()
            with self.assertRaises(ContractError):t.submit(root,self.s,True,'test',self.review,n)
            self.assertEqual(n.calls,[])
        for status in ('FAILED','CANCELED','UNKNOWN'):
            root=generated_project(self.base/status)
            with self.assertRaises(ContractError):t.submit(root,self.s,True,'test',self.review,FakeHTTP(terminal=status))
            with self.assertRaises(ContractError):domain.verify_transcript(root)
        payload=result_payload();payload['transcripts'][0]['sentences']=[]
        out=self.run_submit(FakeHTTP(result=payload));self.assertNotEqual(out['status'],'READY')

    def test_known_task_resume_get_only(self):
        h=FakeHTTP(failure='query')
        with self.assertRaises(ContractError):self.run_submit(h)
        exe=load_json(self.attempt()/'execution.json');self.assertEqual(exe['job_id'],'job-id')
        h=FakeHTTP();out=t.collect(self.root,self.attempt(),h,(h.key,URL))
        self.assertEqual(out['status'],'READY');self.assertEqual(h.calls,['GET','GET'])

    def test_crash_after_download_finishes_from_retained_response_without_network(self):
        original=t.atomic_json
        def crash(path,value):
            if Path(path).name=='execution.json' and value.get('completed') is True:raise OSError('disk full')
            return original(path,value)
        with patch.object(t,'atomic_json',side_effect=crash):
            with self.assertRaises(OSError):self.run_submit()
        self.assertTrue((self.attempt()/'provider-response.json').exists())
        h=FakeHTTP();out=t.collect(self.root,self.attempt(),h)
        self.assertEqual(out['status'],'READY');self.assertEqual(h.calls,[])

    def test_changed_config_requires_new_authorization_invalidates_current(self):
        self.run_submit();before=load_json(self.root/'transcription/current.json')['request_fingerprint']
        changes=[('channel_index',1),('language',{'declared':'es','requested':['es']}),('vocabulary',{'monolito':2}),('context',{'text':'architecture'})]
        for key,value in changes:
            s=copy.deepcopy(self.s);s[key]=value;http=FakeHTTP()
            with self.assertRaises(ContractError):t.submit(self.root,s,True,'test',self.review,http)
            self.assertEqual(http.calls,[])
            pointer=load_json(self.root/'transcription/current.json');self.assertNotEqual(pointer['status'],'READY')
            self.assertNotEqual(pointer['request_fingerprint'],before)
        s=copy.deepcopy(self.s);s['provider']='unapproved-provider';http=FakeHTTP()
        with self.assertRaises(ContractError):t.submit(self.root,s,True,'test',self.review,http)
        self.assertEqual(http.calls,[]);self.assertEqual(load_json(self.root/'transcription/current.json')['status'],'INVALID')

    def test_guard_rejects_tamper_missing_incomplete_and_wrong_bindings(self):
        out=self.run_submit();pointer=load_json(self.root/'transcription/current.json')
        for name in ('response','preparation','cost','redaction','request','execution','transcript'):
            p=self.root/pointer['artifacts'][name]['path'];original=p.read_bytes();p.chmod(0o644);p.write_bytes(original+b' ')
            with self.assertRaises(ContractError):domain.verify_transcript(self.root)
            p.write_bytes(original)
        p=self.attempt()/'execution.json';original=load_json(p);broken=copy.deepcopy(original);broken['completed']=False;atomic_json(p,broken)
        changed=copy.deepcopy(pointer);changed['artifacts']['execution']['sha256']=hash_file(p);atomic_json(self.root/'transcription/current.json',changed)
        with self.assertRaises(ContractError):domain.verify_transcript(self.root)
        atomic_json(p,original);atomic_json(self.root/'transcription/current.json',pointer)
        self.assertEqual(domain.verify_transcript(self.root)['transcript_id'],out['transcript_id'])

    def test_lock_explicit_optin_and_preflight_gate_without_payment(self):
        h=FakeHTTP()
        with t.project_lock(self.root):
            with self.assertRaises(ContractError) as e:self.run_submit(h)
            self.assertEqual(e.exception.code,'BUSY_OR_STALE_LOCK')
        self.assertEqual(h.calls,[])
        with self.assertRaises(ContractError):t.submit(self.root,self.s,False,'test',self.review,h)
        self.assertEqual(h.calls,[])
        self.human.stop()
        with self.assertRaises(ContractError):self.run_submit(h)
        self.assertEqual(h.calls,[])

    def test_directed_original_comparison_remains_required_before_payment(self):
        prep=audio.prepare(self.root,0);bound=prep['binding'];reference=self.base/'reference.json'
        atomic_json(reference,{'generated_test_data':True})
        review={'schema_version':1,'kind':'f003-owner-preflight','owner':'Raúl Almeida','source':'direct-human-message',
                'owner_words':'GENERATED TEST DATA','binding':bound,'preparation_id':prep['preparation_id'],'channel_index':0,
                'full_playback_1x':True,'both_channels_reviewed':True,'voice_complete':True,
                'reference_path':str(reference),'reference_sha256':hash_file(reference)}
        atomic_json(self.review,review)
        self.human.stop()
        with patch.object(t,'validate_reference',return_value={}):
            with self.assertRaises(ContractError) as error:t.human_gate(self.root,bound,prep,self.s,self.review)
        self.assertEqual(error.exception.code,'DIRECTED_SOURCE_COMPARISON_REQUIRED')

    def test_io_failure_before_intent_and_before_normalize_not_ready(self):
        h=FakeHTTP()
        original=t.atomic_json
        def full(path,value):
            if Path(path).name=='execution.json':raise OSError('disk full')
            return original(path,value)
        with patch.object(t,'atomic_json',side_effect=full):
            with self.assertRaises(OSError):self.run_submit(h)
        self.assertNotIn('POST',h.calls)
        with self.assertRaises(ContractError):self.run_submit(FakeHTTP()) # damaged attempt conservatively consumes intent

    def test_derived_reference_gate_order_and_content_never_fabricated(self):
        """p7 OWNER_OVERRIDE: pending pre-POST, derived post-POST, markers mandatory."""
        prep=audio.prepare(self.root,0);bound=prep['binding']
        pending_path=self.base/'derived-reference.json'
        pending={'schema_version':1,'kind':'f003-human-reference','binding':bound,
                 'derivation':'CANDIDATE_DERIVED','owner_override':True,'derivation_pending':True,
                 'candidate_seen':False,'status':'HUMAN_REVIEW_REQUIRED','reviewer':'Raúl Almeida',
                 'method':'candidate-derived','windows':[],'controls':[],'pauses':[],
                 'incorrect_statement':None,'corrected_statement':None,
                 'terms':{'monolito':'term-monolito','microservicios':'term-microservicios','eventos':'term-eventos','idempotencia':'term-idempotencia'},
                 'unknowns':{}}
        atomic_json(pending_path,pending)
        # Without markers the r1 independence requirement is untouched.
        with self.assertRaises(ContractError):t.validate_reference(dict(pending,candidate_seen=True),bound)
        # A pending derived reference is NOT a valid full reference pre-POST content check.
        self.assertTrue(t.pending_derived_reference(pending,bound))
        with self.assertRaises(ContractError):t.validate_reference(pending,bound)
        # Wrong binding never derives.
        wrong=dict(pending);wrong['binding']=dict(bound,project_id='other')
        self.assertFalse(t.pending_derived_reference(wrong,bound))
        # Derivation without a READY transcript fails; nothing is written.
        with self.assertRaises(ContractError):t.derive_operation(self.root,pending_path)

    def test_derive_from_synthetic_candidate_fails_on_missing_events_never_invents(self):
        """A candidate lacking required events must FAIL, not be padded."""
        out=self.run_submit()  # synthetic fixture: only 'try again, try again.' words
        doc=domain.verify_transcript(self.root)
        pending_path=self.base/'derived2.json'
        pending={'schema_version':1,'kind':'f003-human-reference','binding':doc['binding'],
                 'derivation':'CANDIDATE_DERIVED','owner_override':True,'derivation_pending':True,
                 'candidate_seen':False,'status':'HUMAN_REVIEW_REQUIRED','reviewer':'Raúl Almeida',
                 'method':'candidate-derived','windows':[],'controls':[],'pauses':[],
                 'incorrect_statement':None,'corrected_statement':None,
                 'terms':{'monolito':'term-monolito','microservicios':'term-microservicios','eventos':'term-eventos','idempotencia':'term-idempotencia'},
                 'unknowns':{}}
        atomic_json(pending_path,pending)
        with self.assertRaises(ContractError) as e:t.derive_reference(doc,pending)
        self.assertIn(e.exception.code,('DERIVATION_WINDOW_TOO_SPARSE','DERIVATION_WORD_COUNT','DERIVATION_EVENT_MISSING'))
        self.assertEqual(load_json(pending_path),pending)  # pending file untouched by the pure function
        self.assertEqual(out['status'],'READY')

if __name__=='__main__':unittest.main()
