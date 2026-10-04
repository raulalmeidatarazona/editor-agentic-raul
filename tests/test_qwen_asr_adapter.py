"""GENERATED TEST DATA. Injected HTTP only; no service calls."""
from __future__ import annotations
import copy
import io
import json
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
import sys
import unittest
import urllib.error
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import qwen_asr_adapter as v
from content_contract import ContractError, canonical_bytes


def settings(channel=0):
    return {'schema_version': 1, 'provider': 'alibaba-model-studio', 'model': v.MODEL,
            'region': 'ap-southeast-1', 'scope': 'International', 'workspace': 'test-workspace',
            'language': {'declared': 'es', 'requested': ['es','en']}, 'channel_index': channel,
            'vocabulary': dict.fromkeys(('monolito','microservicios','eventos','idempotencia'),1),
            'context': None, 'limits': dict(v.LIMITS)}


def result_payload(duration_ms=3000, fs=8000):
    return {'file_url': 'https://test.oss-ap-southeast-1.aliyuncs.com/audio?Expires=9999999999&OSSAccessKeyId=ID&Signature=CANARY',
            'properties': {'original_sampling_rate': fs, 'original_duration_in_milliseconds': duration_ms, 'channels': [0], 'audio_format': 'pcm_s16le'},
            'transcripts': [{'channel_id':0,'text':'try again, try again.', 'vendor_unknown': {'preserve': True}, 'sentences':[
                {'begin_time':300,'end_time':2100,'text':'try again, try again.', 'sentence_id':1,'words':[
                    {'begin_time':300,'end_time':600,'text':'try ','punctuation':''},
                    {'begin_time':600,'end_time':1000,'text':'again','punctuation':', '},
                    {'begin_time':1200,'end_time':1500,'text':'try ','punctuation':''},
                    {'begin_time':1500,'end_time':2100,'text':'again','punctuation':'.'}]}]}]}


def pricing():
    return {'source_url':v.PRICE_URL,'observed_at_utc': datetime.now(timezone.utc).isoformat(),
            'currency':'USD','input_usd_per_million':'0.15','output_usd_per_million':'0.47'}


class Response(io.BytesIO):
    status=200
    def __enter__(self): return self
    def __exit__(self,*args): self.close()


class AdapterTests(unittest.TestCase):
    def test_effective_request_and_unsupported_options(self):
        s=settings(); b=v.request_body(s, 'signed-url')
        self.assertEqual(b['parameters'], {'channel_id':[0],'language_hints':['es','en'], 'diarization_enabled':False, 'vocabulary':s['vocabulary']})
        s['context']={'text':'arquitectura'}
        self.assertEqual(v.request_body(s,'x')['input']['context'], [{'role':'user','content':[{'type':'input_text','text':'arquitectura'}]}])
        for key,val in [('enable_words',True),('region','cn-beijing'),('vocabulary',{'Again':50}),('context',{'text':'x'*401}),('channel_index',True)]:
            s=settings(); s[key]=val
            with self.assertRaises(ContractError): v.config(s)

    def test_account_coordinates_resolved_only_by_adapter(self):
        import os
        s=settings();s['workspace']=None
        with patch.dict(os.environ,{'F003_QWEN_WORKSPACE':'owner-workspace'}):
            effective=v.resolve_configuration(s)
        self.assertEqual(effective['workspace'],'owner-workspace');self.assertIsNone(s['workspace'])
        self.assertNotIn('api_key',effective)
        with patch.dict(os.environ,{'F003_QWEN_WORKSPACE':''}):
            self.assertIsNone(v.resolve_configuration(s,False)['workspace'])
            with self.assertRaises(ContractError):v.resolve_configuration(s)

    def test_transport_streaming_hash_bytes_and_no_authorization(self):
        import hashlib
        calls=[];data=b'PCM TEST DATA';url='https://bucket.oss-ap-southeast-1.aliyuncs.com/a?Expires=5000&OSSAccessKeyId=ID&Signature=CANARY'
        def ok(req,timeout):calls.append(req);return Response(data)
        h=v.HTTP('KEY_CANARY',opener=ok)
        with patch.object(v.time,'time',return_value=1000):
            result=h.transport(url,hashlib.sha256(data).hexdigest(),len(data))
            self.assertEqual(result['bytes'],len(data));self.assertNotIn('Authorization',calls[0].headers)
            with self.assertRaises(ContractError):h.transport(url,'0'*64,len(data))
            with self.assertRaises(ContractError):h.transport(url,hashlib.sha256(data).hexdigest(),len(data)-1)

    def test_parser_exact_milliseconds_unreported_confidence(self):
        p=result_payload(); prep={'duration_s':'3/1','sample_rate_hz':8000}
        out=v.intermediate(p,prep)
        self.assertEqual(Fraction(out['segments'][0]['words'][0]['start_s']), Fraction(3,10))
        self.assertNotIn('detected_language',out); self.assertNotIn('confidence',out['segments'][0])
        self.assertEqual(out['text'],p['transcripts'][0]['text'])
        p['transcripts'][0]['sentences'][0]['words'][0]['begin_time']=None
        self.assertIsNone(v.intermediate(p,prep)['segments'][0]['words'][0]['start_s'])
        p['transcripts'][0]['sentences'][0]['words']=None
        self.assertIsNone(v.intermediate(p,prep)['segments'][0]['words'])

    def test_partial_channel_duration_and_invalid_time(self):
        for mutate in (lambda p:p['transcripts'].append(copy.deepcopy(p['transcripts'][0])),
                       lambda p:p['transcripts'][0].update(channel_id=1),lambda p:p['properties'].update(original_duration_in_milliseconds=3100),
                       lambda p:p['properties'].update(original_sampling_rate=True),
                       lambda p:p['transcripts'][0]['sentences'][0].update(begin_time=0.1)):
            p=result_payload(); mutate(p)
            with self.assertRaises(ContractError): v.intermediate(p,{'duration_s':'3/1','sample_rate_hz':8000})
        for status in ('FAILED','CANCELED','UNKNOWN'):
            p={'request_id':'req','output':{'task_id':'job','task_status':status}}
            with self.assertRaises(ContractError): v.result_url(p,'job')
        p={'request_id':'req','output':{'task_id':'job','task_status':'SUCCEEDED','results':[{'subtask_status':'FAILED'}]}}
        with self.assertRaises(ContractError): v.result_url(p,'job')

    def test_redaction_canaries_unknown_fields_and_unsafe_recognition(self):
        p=result_payload(); p['unknown']={'token':'KEY_CANARY','message':'Bearer KEY_CANARY and '+p['file_url'], 'numeric':172}
        clean, record=v.safe_payload(canonical_bytes(p),('KEY_CANARY',))
        self.assertNotIn('KEY_CANARY',canonical_bytes(clean).decode()); self.assertNotIn('Signature=CANARY',canonical_bytes(clean).decode())
        self.assertEqual(clean['transcripts'],p['transcripts']); self.assertEqual(clean['unknown']['numeric'],172)
        import hashlib
        self.assertEqual(record['wire_sha256'],hashlib.sha256(canonical_bytes(p)).hexdigest())
        self.assertTrue(record['redactions'])
        p['transcripts'][0]['text']='KEY_CANARY'
        with self.assertRaises(ContractError): v.safe_payload(canonical_bytes(p),('KEY_CANARY',))
        for raw in (b'{bad',b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'[]'):
            with self.assertRaises(ContractError): v.parse_json(raw)

    def test_host_signature_ttl_and_redirect(self):
        good='https://bucket.oss-ap-southeast-1.aliyuncs.com/audio?Expires=5000&OSSAccessKeyId=ID&Signature=S'
        self.assertEqual(v.object_url(good,True,now=1000)['expires_at_epoch_s'],5000)
        for url in ('http://bucket.oss-ap-southeast-1.aliyuncs.com/a','https://localhost/a',
                    'https://bucket.oss-cn-beijing.aliyuncs.com/a','https://user:pass@bucket.oss-ap-southeast-1.aliyuncs.com/a',
                    good+'&Signature=duplicate',good+'#fragment'):
            with self.assertRaises(ContractError): v.object_url(url,True,now=1000)
        with self.assertRaises(ContractError): v.object_url(good,True,now=4000)
        self.assertIsNone(v.NoRedirect().redirect_request(None,None,302,'',{},'https://evil'))

    def test_p7c_auth_host_allowlist_recovery_intl_only(self):
        """p7c: intl recovery host admitted for GET; ws-host intact; Beijing/others rejected."""
        self.assertEqual(v.recovery_endpoint(), 'https://dashscope-intl.aliyuncs.com/api/v1')
        calls = []
        def ok(req, timeout):
            calls.append(req.full_url)
            class R(io.BytesIO):
                status = 200
            return R(canonical_bytes({'request_id':'r','output':{'task_id':'j','task_status':'SUCCEEDED','results':[]}}))
        h = v.HTTP('KEY_CANARY', opener=ok, sleep=lambda _: None, clock=lambda: 0)
        # intl recovery host GET is authorized (no AUTH_HOST_UNAUTHORIZED)
        h.request('GET', 'https://dashscope-intl.aliyuncs.com/api/v1/tasks/j', authenticated=True)
        self.assertEqual(calls, ['https://dashscope-intl.aliyuncs.com/api/v1/tasks/j'])
        # ws-host still authorized
        calls.clear()
        h.request('GET', 'https://test-workspace.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/j', authenticated=True)
        self.assertEqual(len(calls), 1)
        # Beijing and lookalike hosts never receive the Bearer key
        for bad in ('https://dashscope.aliyuncs.com/api/v1/tasks/j',          # Beijing native
                    'https://evil-dashscope-intl.aliyuncs.com/api/v1/tasks/j',
                    'https://dashscope-intl.aliyuncs.com.evil.com/api/v1/tasks/j',
                    'https://dashscope-intlXaliyuncs.com/api/v1/tasks/j'):
            calls.clear()
            with self.assertRaises(ContractError) as e:
                h.request('GET', bad, authenticated=True)
            self.assertEqual(e.exception.code, 'AUTH_HOST_UNAUTHORIZED')
            self.assertEqual(calls, [])

    def test_get_bounded_retries_auth_fail_and_post_never_retries(self):
        calls=[]; sleeps=[]
        def broken(req,timeout):
            calls.append(req); raise urllib.error.URLError('KEY_CANARY')
        h=v.HTTP('KEY_CANARY',opener=broken,sleep=sleeps.append,clock=lambda:0)
        url='https://test-workspace.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/job'
        with self.assertRaises(ContractError): h.request('GET',url,authenticated=True)
        self.assertEqual(len(calls),4); self.assertEqual(sleeps,[1,2,4])
        calls.clear(); sleeps.clear()
        with self.assertRaises(ContractError) as e: h.request('POST',url,{},authenticated=True)
        self.assertEqual(e.exception.code,'SUBMISSION_UNKNOWN'); self.assertEqual(len(calls),1); self.assertEqual(sleeps,[])
        for code in (401,403,302,429,500):
            calls.clear(); sleeps.clear()
            def err(req,timeout):
                calls.append(req); raise urllib.error.HTTPError(url,code,'KEY_CANARY',{},None)
            h=v.HTTP('KEY_CANARY',opener=err,sleep=sleeps.append,clock=lambda:0)
            with self.assertRaises(ContractError): h.request('GET',url,authenticated=True)
            self.assertEqual(len(calls),4 if code in (429,500) else 1)
            calls.clear()
            with self.assertRaises(ContractError): h.request('POST',url,{},authenticated=True)
            self.assertEqual(len(calls),1)

    def test_no_bearer_on_result_and_json_cap(self):
        calls=[]
        def ok(req,timeout): calls.append(req); return Response(b'{}')
        h=v.HTTP('KEY_CANARY',opener=ok)
        h.request('GET','https://bucket.oss-ap-southeast-1.aliyuncs.com/r.json')
        self.assertNotIn('Authorization',calls[0].headers)
        with patch.object(v,'MAX_JSON',2):
            h.open=lambda req,timeout:Response(b'{"x":1}')
            with self.assertRaises(ContractError): h.request('GET','https://bucket.oss-ap-southeast-1.aliyuncs.com/r.json')

    def test_duration_only_missing_negative_usage_and_decimal_oracle(self):
        exe={'execution_id':'id','provider':'x','model':v.MODEL,'region':'ap-southeast-1','job_id':'j','request_ids':['r'],
             'audio_duration_s':'1164/5','original_duration_s':'1164/5'}
        for usage in ({'duration':120},None,{}):
            d=v.cost(exe,{'usage':usage},pricing())
            self.assertIsNone(d['calculated_list_cost_usd']); self.assertIsNone(d['effective_usd_per_audio_minute']); self.assertIsNone(d['extrapolated_usd_per_hour'])
        d=v.cost(exe,{'usage':{'input_tokens':2400,'output_tokens':400}},pricing())
        expected=(Decimal(2400)*Decimal('.15')+Decimal(400)*Decimal('.47'))/Decimal(1000000)
        self.assertEqual(Decimal(d['calculated_list_cost_usd']),expected)
        self.assertEqual(Decimal(d['effective_usd_per_audio_minute']), expected*60/Decimal('232.8'))
        for invalid in (-1,True,0.2):
            with self.assertRaises(ContractError):v.cost(exe,{'usage':{'input_tokens':invalid,'output_tokens':1}},pricing())

if __name__ == '__main__':unittest.main()
