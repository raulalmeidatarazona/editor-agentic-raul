#!/usr/bin/env python3
"""F003 local CLI: guarded preparation, one authorized POST, GET recovery, replay."""
from __future__ import annotations

import argparse
import contextlib
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import audio_preparation as audio
import qwen_asr_adapter as vendor
import transcript_contract as domain
from content_contract import (ContractError, atomic_json, canonical_bytes, digest,
                              hash_file, load_json, safe_path, sync_directory, verify_project)

REPO = Path(__file__).resolve().parents[1]
APPROVED_COMMIT = '74aaa0b64254dfbf0c801e3e7a46a11fb402d357'
APPROVED_SOURCE = '68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc'
APPROVED_FILES = {'requirements.md': '56fcb6a9e5b1057c5ae07366c4ee485d9f9456b505531e1d2576ab3de680f3e1',
                  'plan.md': '105d3f5925619ef7e3ed30f000414b3aacd985ab47827042f8469d40f142910e',
                  'validation.md': '0ac3c53c48ba6c50d8c74b667b3642e5309305a90a730c45afeb22a0bed8ee75',
                  'D002-initial-f003-stt-provider.md': 'e38f1f935fdfd9d6493f3f2f463e89dbae04cd1fdee9a4d49c9eb036167ae9d2'}


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


@contextlib.contextmanager
def project_lock(root):
    tree = audio.check_tree(root); tree.mkdir(parents=True, exist_ok=True)
    path = tree / '.lock'
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        vendor.fail('BUSY_OR_STALE_LOCK', 'transcription/.lock')
    try:
        with os.fdopen(fd, 'wb') as file:
            file.write(canonical_bytes({'pid': os.getpid(), 'created_at_utc': now()})); file.flush(); os.fsync(file.fileno())
        sync_directory(tree)
        yield
    finally:
        path.unlink(); sync_directory(tree)


def stable(root, bound):
    guarded = verify_project(root)
    if domain.binding(*guarded) != bound: vendor.fail('SOURCE_CHANGED')
    return guarded


def request_document(bound, preparation, settings, preparation_sha):
    inputs = {'binding': bound, 'preparation_id': preparation['preparation_id'],
              'preparation_sha256': preparation_sha, 'audio_sha256': preparation['audio_sha256'],
              'provider': settings['provider'], 'model': settings['model'], 'region': settings['region'],
              'scope': settings['scope'], 'workspace': settings['workspace'], 'endpoint': vendor.endpoint(settings),
              'configuration': settings, 'adapter_version': vendor.adapter_version()}
    return {'schema_version': 1, 'kind': 'stt-request', **inputs, 'request_fingerprint': digest(inputs),
            'effective_body': vendor.request_body(settings, 'sha256:' + preparation['audio_sha256'])}


def fingerprint(request):
    return digest({k: request[k] for k in ('binding', 'preparation_id', 'preparation_sha256', 'audio_sha256',
                  'provider', 'model', 'region', 'scope', 'workspace', 'endpoint', 'configuration', 'adapter_version')})


def invalidate(root, bound, error, request_fingerprint=None):
    atomic_json(Path(root) / 'transcription/current.json', {
        'schema_version': 1, 'kind': 'current-source-transcript', 'binding': bound,
        'request_fingerprint': request_fingerprint, 'artifacts': {}, 'normalization_version': None,
        'status': error.status, 'reasons': [error.reason()],
        'unknowns': {'/normalization_version': 'UNRESOLVED'}, 'extensions': {}})


def immutable(path, value):
    path = Path(path)
    if len(canonical_bytes(value)) > vendor.MAX_JSON: vendor.fail('RESPONSE_LIMIT')
    if path.exists():
        if path.read_bytes() != canonical_bytes(value): vendor.fail('IMMUTABLE_ARTIFACT_CONFLICT')
        return
    atomic_json(path, value); path.chmod(0o444)


def approval(reference, bound, preparation, settings):
    if reference not in ('74aaa0b', APPROVED_COMMIT): vendor.fail('APPROVAL_REFERENCE_REQUIRED')
    root = REPO / '.local/spec-approvals/F003/r1'
    doc = load_json(root / 'approval.json')
    if (doc['approved_commit'] != APPROVED_COMMIT or doc['max_submissions'] != 1 or
            hash_file(root / 'owner-message.txt') != doc['owner_message_sha256']):
        vendor.fail('APPROVAL_INVALID')
    for name, sha in APPROVED_FILES.items():
        if hash_file(root / name) != sha: vendor.fail('APPROVAL_BUNDLE_CHANGED')
    if (bound['source_sha256'] != APPROVED_SOURCE or bound['project_id'] != 'f002-studio-001' or
            preparation['duration_s'] != '1164/5' or settings['model'] != vendor.MODEL or
            settings['language'] != {'declared': 'es', 'requested': ['es', 'en']} or
            settings['vocabulary'] != dict.fromkeys(('monolito', 'microservicios', 'eventos', 'idempotencia'), 1) or
            settings['context'] is not None):
        vendor.fail('NEW_PAID_AUTHORIZATION_REQUIRED')
    return {'approved_commit': APPROVED_COMMIT, 'owner_message_sha256': doc['owner_message_sha256'], 'max_submissions': 1}


def human_gate(root, bound, preparation, settings, review_path):
    if review_path is None: vendor.fail('HUMAN_PREFLIGHT_REQUIRED', 'review')
    review = load_json(review_path)
    if (review.get('schema_version') != 1 or review.get('kind') != 'f003-owner-preflight' or
            review.get('owner') != 'Raúl Almeida' or review.get('source') != 'direct-human-message' or
            not review.get('owner_words') or review.get('binding') != bound or
            review.get('preparation_id') != preparation['preparation_id'] or
            review.get('channel_index') != settings['channel_index'] or review.get('full_playback_1x') is not True or
            review.get('both_channels_reviewed') is not True or review.get('voice_complete') is not True):
        vendor.fail('CHANNEL_HUMAN_REVIEW_REQUIRED', 'review')
    refs = load_json(review['reference_path'])
    if hash_file(review['reference_path']) != review['reference_sha256']:
        vendor.fail('REFERENCE_CHANGED')
    validate_reference(refs, bound)
    if review.get('directed_original_comparison') is not True:
        vendor.fail('DIRECTED_SOURCE_COMPARISON_REQUIRED', 'review')
    account = review.get('account', {})
    if (account.get('workspace') != settings['workspace'] or account.get('region') != 'ap-southeast-1' or
            account.get('scope') != 'International' or account.get('metered_api_eligible') is not True or
            account.get('coding_plan_key') is not False or account.get('model_enabled') is not True):
        vendor.fail('ACCOUNT_ELIGIBILITY_REQUIRED', 'account')
    storage = review.get('storage', {})
    if (storage.get('existing_private_oss_singapore') is not True or storage.get('owner_managed_upload') is not True or
            storage.get('delete_after_result_within_24h') is not True or review.get('privacy_limits_accepted') is not True):
        vendor.fail('TRANSPORT_UNAVAILABLE', 'storage')
    price = review.get('pricing_snapshot', {})
    try:
        if (price.get('source_url') != vendor.PRICE_URL or price.get('currency') != 'USD' or
                datetime.fromisoformat(price['observed_at_utc'].replace('Z', '+00:00')).date() != datetime.now(timezone.utc).date() or
                not Decimal('0') <= Decimal(price['input_usd_per_million']) <= Decimal('0.15') or
                not Decimal('0') <= Decimal(price['output_usd_per_million']) <= Decimal('0.47')):
            vendor.fail('PRICE_REVIEW_REQUIRED', 'pricing')
    except (KeyError, ValueError, TypeError, ArithmeticError): vendor.fail('PRICE_REVIEW_REQUIRED', 'pricing')
    return review


def validate_reference(refs, bound):
    """Human-only facts are required, never generated by an energy detector."""
    if (refs.get('schema_version') != 1 or refs.get('kind') != 'f003-human-reference' or
            refs.get('binding') != bound or refs.get('candidate_seen') is not False or
            refs.get('status') != 'OWNER_CONFIRMED' or not refs.get('reviewer') or not refs.get('method')):
        vendor.fail('INDEPENDENT_REFERENCE_REQUIRED', 'references')
    windows = refs.get('windows', [])
    expected = [('0/1', '25/1'), ('60/1', '85/1'), ('90/1', '115/1'), ('130/1', '155/1'), ('195/1', '228/1')]
    if len(windows) < 5 or [(x.get('start_s'), x.get('end_s')) for x in windows[:5]] != expected:
        vendor.fail('REFERENCE_WINDOWS_REQUIRED')
    if any(not isinstance(x.get('text'), str) or not x['text'].strip() for x in windows): vendor.fail('REFERENCE_TEXT_REQUIRED')
    if sum(len(comparison_words(x['text'])) for x in windows) < 200: vendor.fail('REFERENCE_WORD_COUNT')
    controls = refs.get('controls', [])
    if type(controls) is not list or len(controls) < 30: vendor.fail('REFERENCE_CONTROLS_REQUIRED')
    ids = set(); positions=set(); groups = {'opening': 0, 'correction': 0, 'ending': 0}; critical = []
    for row in controls:
        if row.get('id') in ids or not row.get('id') or not isinstance(row.get('text'), str) or not row['text'].strip():
            vendor.fail('REFERENCE_CONTROL_INVALID')
        ids.add(row['id'])
        wi, li = row.get('window_index'), row.get('lexical_index')
        if (type(wi) is not int or not 0 <= wi < len(windows) or type(li) is not int or li < 0 or
                li >= len(comparison_words(windows[wi]['text'])) or
                comparison_words(row['text']) != [comparison_words(windows[wi]['text'])[li]]):
            vendor.fail('REFERENCE_CONTROL_POSITION_REQUIRED')
        if (wi,li) in positions: vendor.fail('REFERENCE_DUPLICATE_CONTROL')
        positions.add((wi,li))
        if row.get('group') in groups: groups[row['group']] += 1
        if row.get('critical'): critical.append(row['text'].casefold())
        for edge in ('onset', 'offset'):
            try: lo, hi = map(domain.fraction, row[edge + '_bounds_s'])
            except (KeyError, TypeError, ValueError): vendor.fail('REFERENCE_BOUNDS_REQUIRED')
            if hi < lo or hi - lo > domain.fraction('1/20'): vendor.fail('REFERENCE_UNCERTAINTY')
        if domain.fraction(row['onset_bounds_s'][1]) >= domain.fraction(row['offset_bounds_s'][0]): vendor.fail('REFERENCE_INTERVAL_INVALID')
    if any(v < 10 for v in groups.values()) or critical != ['again', 'try', 'again', 'try', 'again']:
        vendor.fail('REFERENCE_CONTROL_SELECTION')
    for group, wi in (('opening', 0), ('correction', 2), ('ending', 4)):
        rows = [r for r in controls if r.get('group') == group]
        if len(rows) != 10 or [(r['window_index'], r['lexical_index']) for r in rows] != [(wi,i) for i in range(10)]:
            vendor.fail('REFERENCE_FIRST_TEN_REQUIRED')
    if set(refs.get('terms', {})) != {'monolito', 'microservicios', 'eventos', 'idempotencia'}:
        vendor.fail('REFERENCE_TERMS_REQUIRED')
    for term, cid in refs['terms'].items():
        if not any(r['id'] == cid and r['text'].casefold() == term for r in controls): vendor.fail('REFERENCE_TERMS_REQUIRED')
    pauses = refs.get('pauses', [])
    if len(pauses) != 3 or {r.get('kind') for r in pauses} != {'before-again', 'after-again', 'natural'}:
        vendor.fail('REFERENCE_PAUSES_REQUIRED')
    for row in pauses:
        if domain.fraction(row['end_s']) - domain.fraction(row['start_s']) <= domain.fraction('3/10'):
            vendor.fail('REFERENCE_PAUSE_CORE_EMPTY')
    if not refs.get('incorrect_statement') or not refs.get('corrected_statement'):
        vendor.fail('REFERENCE_STATEMENTS_REQUIRED')
    return refs


def comparison_words(text):
    import unicodedata
    # Comparison only; never writes into canonical transcript.
    text = unicodedata.normalize('NFC', text).casefold()
    return ''.join(' ' if unicodedata.category(c).startswith('P') else c for c in text).split()


def edit_alignment(reference, candidate):
    """Deterministic Levenshtein counts and positional alignment for evaluation only."""
    rows = [[(0, None)] * (len(candidate)+1) for _ in range(len(reference)+1)]
    for i in range(1, len(reference)+1): rows[i][0] = (i, 'D')
    for j in range(1, len(candidate)+1): rows[0][j] = (j, 'I')
    for i in range(1, len(reference)+1):
        for j in range(1, len(candidate)+1):
            same = reference[i-1] == candidate[j-1]
            options = [(rows[i-1][j-1][0]+(not same), 'M' if same else 'S'),
                       (rows[i-1][j][0]+1, 'D'), (rows[i][j-1][0]+1, 'I')]
            rows[i][j] = min(options, key=lambda x:x[0])
    counts = dict(S=0,D=0,I=0,N=len(reference)); mapping={}
    i,j=len(reference),len(candidate)
    while i or j:
        op=rows[i][j][1]
        if op in ('M','S'):
            mapping[i-1]=j-1
            if op=='S':counts['S']+=1
            i-=1;j-=1
        elif op=='D': counts['D']+=1;mapping[i-1]=None;i-=1
        else: counts['I']+=1;j-=1
    return counts,mapping


def evaluate(doc, refs):
    """Quantitative review; human acceptance/as-spoken judgment remains a separate gate."""
    from fractions import Fraction
    from math import ceil
    from statistics import median
    validate_reference(refs, doc['binding']); domain.validate(doc)
    if doc['readiness']['status'] != 'READY': vendor.fail('TRANSCRIPT_NOT_READY')
    totals=dict(S=0,D=0,I=0,N=0); windows=[]; correspondences={}
    for wi, window in enumerate(refs['windows']):
        lo,hi=map(domain.fraction,(window['start_s'],window['end_s']))
        selected=[]; word_rows=[]
        for word in doc['words']:
            midpoint=(domain.fraction(word['start_s'])+domain.fraction(word['end_s']))/2
            if lo <= midpoint < hi:
                lexical=comparison_words(word['text']+(word['punctuation'] or ''))
                selected.extend(lexical);word_rows.extend([word]*len(lexical))
        count, mapping=edit_alignment(comparison_words(window['text']),selected)
        for k,v in count.items():totals[k]+=v
        windows.append({'index':wi,**count,'candidate_lexical_words':selected})
        for ri,ci in mapping.items():correspondences[(wi,ri)]=None if ci is None else word_rows[ci]
    failures=[];timing=[]; ordinary=[];critical=[];signed={g:{e:[] for e in ('onset','offset')} for g in ('opening','ending')}
    for row in refs['controls']:
        word=correspondences.get((row['window_index'],row['lexical_index']))
        measured={'reference_id':row['id'],'reference_text':row['text'],'word_id':None if word is None else word['id']}
        if word is None or comparison_words(row['text']) != comparison_words(word['text']):
            failures.append('CONTROL_MISSING_OR_SUBSTITUTED:'+row['id']);timing.append({**measured,'status':'FAIL'});continue
        for edge,key in (('onset','start_s'),('offset','end_s')):
            low,high=map(domain.fraction,row[edge+'_bounds_s']); actual=domain.fraction(word[key])
            error=max(abs(actual-low),abs(actual-high));measured[edge+'_conservative_error_s']=f'{error.numerator}/{error.denominator}'
            (critical if row.get('critical') else ordinary).append(error)
            if row.get('critical') and error > Fraction(3,20):failures.append('CRITICAL_TIMING:'+row['id']+':'+edge)
            if row.get('group') in signed:signed[row['group']][edge].append(actual-(low+high)/2)
        measured['status']='MEASURED';timing.append(measured)
    p95=sorted(ordinary)[ceil(.95*len(ordinary))-1] if ordinary else None
    maximum=max(ordinary,default=None)
    if p95 is None or p95>Fraction(1,5) or maximum>Fraction(3,10):failures.append('CONTROL_TIMING_THRESHOLD')
    drift={}
    for edge in ('onset','offset'):
        if len(signed['opening'][edge])!=10 or len(signed['ending'][edge])!=10:
            drift[edge]=None;failures.append('DRIFT_CONTROLS_INCOMPLETE');continue
        difference=abs(median(signed['opening'][edge])-median(signed['ending'][edge]))
        drift[edge]=f'{difference.numerator}/{difference.denominator}'
        if difference>Fraction(1,10):failures.append('DRIFT_THRESHOLD:'+edge)
    wer=Fraction(totals['S']+totals['D']+totals['I'],totals['N'])
    if wer>Fraction(1,10):failures.append('WER_THRESHOLD')
    pause_results=[]
    for pause in refs['pauses']:
        lo=domain.fraction(pause['start_s'])+Fraction(3,20);hi=domain.fraction(pause['end_s'])-Fraction(3,20)
        intruders=[w['id'] for w in doc['words'] if domain.fraction(w['start_s'])<hi and domain.fraction(w['end_s'])>lo]
        pause_results.append({'kind':pause['kind'],'word_ids_in_core':intruders})
        if intruders:failures.append('PAUSE_HALLUCINATION:'+pause['kind'])
    r=lambda x:None if x is None else f'{x.numerator}/{x.denominator}'
    return {'schema_version':1,'kind':'f003-quantitative-review','transcript_id':doc['transcript_id'],
            'result':'FAIL' if failures else 'HUMAN_REVIEW_REQUIRED','failures':failures,'wer':{**totals,'ratio':r(wer)},
            'windows':windows,'controls':timing,'ordinary_p95_s':r(p95),'ordinary_max_s':r(maximum),
            'critical_max_s':r(max(critical,default=None)),'drift_s':drift,'pauses':pause_results,
            'human_remaining':['as-spoken incorrect/corrected statements and negations','full voice fidelity','cost reconciliation','exact evidence acceptance']}


def locate_execution(root, eid):
    try:
        if str(uuid.UUID(eid)) != eid: vendor.fail('EXECUTION_ID_INVALID')
    except (ValueError, TypeError): vendor.fail('EXECUTION_ID_INVALID')
    matches = list((Path(root) / 'transcription/requests').glob('*/attempts/' + eid))
    if len(matches) != 1: vendor.fail('EXECUTION_NOT_FOUND')
    return matches[0]


def budget(attempt, preparation, root):
    used = sum(p.stat().st_size for p in Path(attempt).rglob('*') if p.is_file())
    used += sum(p.stat().st_size for p in safe_path(root, preparation['audio_path']).parent.rglob('*') if p.is_file())
    if used > vendor.LIMITS['evidence_bytes']: vendor.fail('RESOURCE_LIMIT')


def normalize_attempt(root, attempt, normalization_version=None):
    project, current, inspection = verify_project(root); bound = domain.binding(project, current, inspection)
    request = load_json(attempt / 'request.json'); exe = load_json(attempt / 'execution.json')
    if request['binding'] != bound or exe['binding'] != bound or fingerprint(request) != request['request_fingerprint']:
        vendor.fail('BINDING_MISMATCH')
    prep_path = safe_path(root, 'transcription/preparations/' + request['preparation_id'] + '/preparation.json')
    prep = audio.validate_preparation(root, load_json(prep_path), bound, inspection)
    if hash_file(prep_path) != request['preparation_sha256'] or prep['audio_sha256'] != request['audio_sha256']:
        vendor.fail('PREPARATION_CHANGED')
    if exe['phase'] != 'SUCCEEDED' or exe['completed'] is not True: vendor.fail('EXECUTION_INCOMPLETE')
    response_path = attempt / 'provider-response.json'; response = load_json(response_path)
    if (response['binding'] != bound or response['execution_id'] != exe['execution_id'] or
            response['request_fingerprint'] != request['request_fingerprint'] or hash_file(response_path) != exe['response_sha256']):
        vendor.fail('RESPONSE_CHANGED')
    vendor.job(response['payloads']['submit'], exe['job_id'])
    _, _, status = vendor.job(response['payloads']['terminal'], exe['job_id'])
    rows = response['payloads']['terminal']['output'].get('results', [])
    if status != 'SUCCEEDED' or len(rows) != 1 or rows[0]['subtask_status'] != 'SUCCEEDED': vendor.fail('SUBTASK_INCOMPLETE')
    generic = vendor.intermediate(response['payloads']['result'], prep)
    nv = normalization_version or domain.version()
    doc = domain.normalize(generic, bound, prep,
        {'execution_id': exe['execution_id'], 'response_sha256': hash_file(response_path),
         'request_fingerprint': request['request_fingerprint'], 'audio_sha256': prep['audio_sha256'],
         'preparation_sha256': hash_file(prep_path)}, request['configuration']['language'], inspection, nv)
    revision = attempt / 'revisions' / digest({'normalization_version': nv}); revision.mkdir(parents=True, exist_ok=True)
    immutable(revision / 'transcript.json', doc)
    paths = {'execution': attempt / 'execution.json', 'preparation': prep_path, 'response': response_path,
             'transcript': revision / 'transcript.json', 'redaction': attempt / 'redaction.json',
             'request': attempt / 'request.json', 'cost': attempt / 'cost.json'}
    pointer = {'schema_version': 1, 'kind': 'current-source-transcript', 'binding': bound,
               'request_fingerprint': request['request_fingerprint'],
               'artifacts': {k: {'path': str(p.relative_to(root)), 'sha256': hash_file(p)} for k, p in paths.items()},
               'normalization_version': nv, 'status': doc['readiness']['status'], 'reasons': doc['readiness']['reasons'],
               'unknowns': {}, 'extensions': {}}
    budget(attempt, prep, root); stable(root, bound)
    old = Path(root) / 'transcription/current.json'
    if not old.exists() or load_json(old) != pointer: atomic_json(old, pointer)
    if pointer['status'] == 'READY': domain.verify_transcript(root)
    return {'operation': 'normalize', 'outcome': 'READY' if pointer['status'] == 'READY' else 'REVIEW_REQUIRED',
            'project_id': bound['project_id'], 'status': pointer['status'], 'reasons': pointer['reasons'],
            'execution_id': exe['execution_id'], 'transcript_id': doc['transcript_id'],
            'path': str((revision / 'transcript.json').resolve())}


def collect(root, attempt, http, secrets=(), hook=None):
    """Known task recovery only: GET, never POST. Sanitized payloads retained as received."""
    exe = load_json(attempt / 'execution.json'); request = load_json(attempt / 'request.json')
    bound = exe['binding']; stable(root, bound)
    if exe['completed'] and exe['phase'] == 'SUCCEEDED': return normalize_attempt(root, attempt)
    if not exe.get('job_id'): vendor.fail('SUBMISSION_UNKNOWN')
    if exe['phase'] in ('FAILED', 'CANCELED', 'UNKNOWN'): vendor.fail('JOB_' + exe['phase'])
    if (attempt / 'provider-response.json').exists():
        # Crash after download: the immutable local envelope wins. No refetch,
        # replacement response, or second charge is needed to finish locally.
        response = load_json(attempt / 'provider-response.json')
        redaction = load_json(attempt / 'redaction.json')
        response_sha = hash_file(attempt / 'provider-response.json')
        if (response.get('binding') != bound or response.get('execution_id') != exe['execution_id'] or
                response.get('request_fingerprint') != exe['request_fingerprint'] or
                redaction.get('response_sha256') != response_sha): vendor.fail('RESPONSE_CHANGED')
        terminal = response['payloads']['terminal']
        _, _, terminal_status = vendor.job(terminal, exe['job_id'])
        results = terminal['output'].get('results', [])
        if terminal_status != 'SUCCEEDED' or len(results) != 1 or results[0].get('subtask_status') != 'SUCCEEDED': vendor.fail('SUBTASK_INCOMPLETE')
        prep = load_json(safe_path(root, 'transcription/preparations/' + request['preparation_id'] + '/preparation.json'))
        vendor.intermediate(response['payloads']['result'], prep)
        stable(root, bound)
        atomic_json(attempt / 'cost.json', vendor.cost(exe, terminal, exe['pricing_snapshot']))
        exe.update(phase='SUCCEEDED', status='READY', completed=True, response_sha256=response_sha,
                   finished_at_utc=now(), reasons=[], stability_after={'binding': bound, 'checked_at_utc': now()})
        atomic_json(attempt / 'execution.json', exe)
        return normalize_attempt(root, attempt)
    job_id = exe['job_id']; settings = request['configuration']
    vendor.config(settings)
    if not vendor.IDENTIFIER.fullmatch(job_id) or fingerprint(request) != request['request_fingerprint']: vendor.fail('EXECUTION_INVALID')
    deadline = http.clock() + vendor.LIMITS['poll_deadline_s']
    history = list(exe.get('query_payloads', [])); redactions = list(exe.get('redaction_records', []))
    try:
        while True:
            raw = http.request('GET', vendor.endpoint(settings) + '/tasks/' + job_id, authenticated=True, deadline=deadline)
            parsed = vendor.parse_json(raw)
            clean, record = vendor.safe_payload(raw, secrets)
            _, rid, status = vendor.job(parsed, job_id)
            exe['request_ids'].append(rid); history.append(clean); redactions.append({'stage': 'query', **record})
            candidate = {**exe, 'phase': status, 'query_payloads': history, 'redaction_records': redactions}
            if len(canonical_bytes(candidate)) > vendor.MAX_JSON: vendor.fail('RESPONSE_LIMIT')
            exe = candidate
            atomic_json(attempt / 'execution.json', exe)
            if status not in ('PENDING', 'RUNNING'): break
            if http.clock() + 5 >= deadline: vendor.fail('POLL_DEADLINE')
            http.sleep(5)
        if status != 'SUCCEEDED': vendor.fail('JOB_' + status)
        url = vendor.result_url(parsed, job_id)
        # If the provider echoes the input URL, bind it before it is redacted.
        if exe.get('input_url_sha256') != digest({'url': parsed['output']['results'][0].get('file_url')}):
            vendor.fail('RESULT_INPUT_MISMATCH')
        raw = http.request('GET', url, authenticated=False, deadline=deadline)
        if exe.get('input_url_sha256') != digest({'url': vendor.parse_json(raw).get('file_url')}):
            vendor.fail('RESULT_INPUT_MISMATCH')
        clean_result, record = vendor.safe_payload(raw, secrets + (url,))
        redactions.append({'stage': 'result', **record})
        response = {'schema_version': 1, 'kind': 'retained-stt-response', 'binding': bound,
                    'request_fingerprint': exe['request_fingerprint'], 'execution_id': exe['execution_id'],
                    'payloads': {'submit': exe['submit_payload'], 'queries': history, 'terminal': clean, 'result': clean_result}}
        immutable(attempt / 'provider-response.json', response)
        immutable(attempt / 'redaction.json', {'schema_version': 1, 'kind': 'stt-redaction-manifest',
            'execution_id': exe['execution_id'], 'response_sha256': hash_file(attempt / 'provider-response.json'), 'records': redactions})
        prep = load_json(safe_path(root, 'transcription/preparations/' + request['preparation_id'] + '/preparation.json'))
        # Validate payload completeness, not just the terminal task status.
        vendor.intermediate(clean_result, prep)
        # Pending accounting is an administrative journal, finalized only at completion.
        atomic_json(attempt / 'cost.json', vendor.cost(exe, clean, exe['pricing_snapshot']))
        exe.update(phase='SUCCEEDED', status='READY', completed=True, finished_at_utc=now(),
                   response_sha256=hash_file(attempt / 'provider-response.json'), reasons=[],
                   stability_after={'binding': bound, 'checked_at_utc': now()})
        stable(root, bound); budget(attempt, prep, root)
        atomic_json(attempt / 'execution.json', exe)
        (attempt / 'report.md').write_text('F003 provider execution retained. Acoustic review and billing reconciliation remain required.\n')
        if hook: hook('before_normalize', attempt)
        return normalize_attempt(root, attempt)
    except ContractError as error:
        exe.update(status=error.status, reasons=[error.reason()], finished_at_utc=now())
        if exe['phase'] not in ('FAILED', 'CANCELED', 'UNKNOWN'): exe['phase'] = 'RECOVERY_REQUIRED'
        atomic_json(attempt / 'execution.json', exe)
        if not (attempt / 'cost.json').exists():
            immutable(attempt / 'cost.json', vendor.cost(exe, history[-1] if history else {}, exe['pricing_snapshot']))
        invalidate(root, bound, error, exe['request_fingerprint'])
        raise


def _submit_locked(root, settings, allow=False, reference=None, review_path=None, http=None, hook=None):
    project, current, inspection = verify_project(root); bound = domain.binding(project, current, inspection)
    prep = audio.prepare(root, settings['channel_index'])
    prep_path = safe_path(root, 'transcription/preparations/' + prep['preparation_id'] + '/preparation.json')
    request = request_document(bound, prep, settings, hash_file(prep_path)); fp = request['request_fingerprint']
    pointer_path = root / 'transcription/current.json'
    if pointer_path.exists():
        pointer = load_json(pointer_path)
        if pointer.get('request_fingerprint') == fp and pointer.get('status') == 'READY':
            doc = domain.verify_transcript(root)
            return {'operation': 'submit', 'outcome': 'NO_OP', 'project_id': bound['project_id'],
                    'status': 'READY', 'reasons': [], 'transcript_id': doc['transcript_id']}
    error = ContractError('PREFLIGHT_PENDING', 'Complete the required preflight before submission.')
    invalidate(root, bound, error, fp)
    # Any existing paid intent, including a damaged/incomplete journal, consumes r1.
    if any((root / 'transcription/requests').glob('*/attempts/*')):
        vendor.fail('PAID_ATTEMPT_ALREADY_CONSUMED')
    if not allow: vendor.fail('EXPLICIT_PROVIDER_CALL_REQUIRED')
    permission = approval(reference, bound, prep, settings)
    review = human_gate(root, bound, prep, settings, review_path)
    url = os.environ.get('F003_AUDIO_URL', '')
    if not url: vendor.fail('TRANSPORT_UNAVAILABLE')
    http = http or vendor.HTTP()
    if not http.key: vendor.fail('CREDENTIAL_UNAVAILABLE')
    metadata = {k:v for k,v in request.items() if k != 'effective_body'}
    clean_request, _ = vendor.sanitize(metadata, (http.key, url))
    if clean_request != metadata: vendor.fail('UNSAFE_REQUEST')
    transport = http.transport(url, prep['audio_sha256'], safe_path(root, prep['audio_path']).stat().st_size)
    stable(root, bound)
    eid = str(uuid.uuid4())
    attempt = root / 'transcription/requests' / fp / 'attempts' / eid
    attempt.mkdir(parents=True); sync_directory(attempt.parent)
    immutable(attempt / 'request.json', request)
    exe = {'schema_version': 1, 'kind': 'stt-execution', 'binding': bound,
           'execution_id': eid, 'request_fingerprint': fp, **{k: settings[k] for k in ('provider', 'model', 'region', 'scope', 'workspace')},
           'requested_model': settings['model'], 'reported_model': None, 'backend_revision': None,
           'adapter_version': request['adapter_version'], 'request_sha256': hash_file(attempt / 'request.json'),
           'preparation_sha256': hash_file(prep_path), 'started_at_utc': now(), 'finished_at_utc': None,
           'completed': False, 'phase': 'SUBMIT_INTENT', 'status': 'BLOCKED', 'reasons': [],
           'job_id': None, 'request_ids': [], 'audio_duration_s': prep['duration_s'],
           'original_duration_s': inspection['container']['reported_duration_s'], 'response_sha256': None,
           'limits': vendor.LIMITS, 'approval': permission, 'review_sha256': hash_file(review_path),
           'stability_before': {'binding': bound, 'checked_at_utc': now()},
           'pricing_snapshot': review['pricing_snapshot'], 'transport': transport,
           'input_url_sha256': digest({'url': url}), 'query_payloads': [], 'redaction_records': [],
           'unknowns': {'/reported_model': 'NOT_REPORTED', '/backend_revision': 'NOT_REPORTED'}}
    atomic_json(attempt / 'execution.json', exe)  # fsync BEFORE the only POST
    if hook: hook('after_submit_intent', attempt)
    try:
        raw = http.request('POST', vendor.endpoint(settings) + '/services/audio/asr/transcription',
                           vendor.request_body(settings, url), authenticated=True)
        if hook: hook('after_post_before_task', attempt)
        clean, redaction = vendor.safe_payload(raw, (http.key, url))
        candidate = {**exe, 'submit_payload': clean, 'redaction_records': [{'stage': 'submit', **redaction}]}
        if len(canonical_bytes(candidate)) > vendor.MAX_JSON: vendor.fail('RESPONSE_LIMIT')
        exe = candidate
        job_id, rid, status = vendor.job(clean)
        exe.update(job_id=job_id, request_ids=[rid], phase=status, submit_payload=clean,
                   redaction_records=[{'stage': 'submit', **redaction}])
        atomic_json(attempt / 'execution.json', exe)
    except ContractError as error:
        exe.update(phase='SUBMISSION_UNKNOWN' if error.code != 'POST_REJECTED' else 'FAILED',
                   status='BLOCKED', reasons=[error.reason()], finished_at_utc=now())
        atomic_json(attempt / 'execution.json', exe)
        immutable(attempt / 'cost.json', vendor.cost(exe, {}, review['pricing_snapshot']))
        invalidate(root, bound, error, fp)
        raise
    return collect(root, attempt, http, (http.key, url), hook)


def submit(root, settings, allow=False, reference=None, review_path=None, http=None, hook=None):
    root = Path(root).resolve()
    with project_lock(root):
        try:
            vendor.config(settings)
            return _submit_locked(root, settings, allow, reference, review_path, http, hook)
        except ContractError as error:
            # Retain the exact stopped gate while still holding the exclusive lock.
            try:
                bound = domain.binding(*verify_project(root))
                pointer_path = root / 'transcription/current.json'
                fp = load_json(pointer_path).get('request_fingerprint') if pointer_path.exists() else None
                invalidate(root, bound, error, fp)
            except (ContractError, OSError, KeyError, TypeError):
                pass  # Invalid predecessor still blocks every consumer; never edit F002.
            raise


def prepare_operation(root, settings, evidence=None):
    root = Path(root).resolve()
    # Workspace is irrelevant for preparation, but all other config remains validated.
    vendor.config(settings, require_workspace=False)
    with project_lock(root):
        project, _, inspection = verify_project(root)
        stream = next(s for s in inspection['streams'] if s['index'] == inspection['selection']['audio_index'])
        channels = [settings['channel_index']] if settings['channel_index'] is not None else list(range(min(2, stream['audio']['channels'])))
        candidates = [audio.prepare(root, ch) for ch in channels]
        packs = [audio.listening_pack(root, prep, Path(evidence) / ('channel-' + str(prep['channel_index']))) for prep in candidates] if evidence else []
        return {'operation': 'prepare', 'outcome': 'REVIEW_REQUIRED', 'project_id': project['project_id'],
                'status': 'NEEDS_REVIEW', 'reasons': [{'code': 'CHANNEL_HUMAN_REVIEW_REQUIRED', 'field': 'channel_index',
                  'action': 'Listen to both channels and the selected full WAV at 1x before submission.'}],
                'preparations': [{'id': p['preparation_id'], 'channel_index': p['channel_index'], 'audio_path': str(safe_path(root, p['audio_path'])),
                                  'sha256': p['audio_sha256'], 'duration_s': p['duration_s'], 'samples': p['sample_count']} for p in candidates],
                'listening_packs': [str(Path(evidence) / ('channel-' + str(p['channel_index'])) / 'listening-pack.json') for p in packs]}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        vendor.fail('CLI_ARGUMENT_INVALID', 'arguments', 'INVALID')


def main(argv=None):
    parser = Parser(description=__doc__)
    sub = parser.add_subparsers(dest='operation', required=True, parser_class=Parser)
    for op in ('prepare', 'submit', 'resume', 'normalize', 'verify', 'evaluate'):
        p = sub.add_parser(op); p.add_argument('--project', required=True)
        if op in ('prepare', 'submit'): p.add_argument('--config', required=True)
        if op == 'prepare': p.add_argument('--evidence')
        if op == 'submit':
            p.add_argument('--allow-provider-call', action='store_true'); p.add_argument('--approval-reference'); p.add_argument('--review')
        if op in ('resume', 'normalize'): p.add_argument('--execution-id', required=True)
        if op == 'evaluate': p.add_argument('--reference', required=True); p.add_argument('--output', required=True)
    args = None
    try:
        args = parser.parse_args(argv); root = Path(args.project).resolve()
        if args.operation == 'prepare': result = prepare_operation(root, vendor.resolve_configuration(load_json(args.config), False), args.evidence)
        elif args.operation == 'submit': result = submit(root, vendor.resolve_configuration(load_json(args.config), validate=False), args.allow_provider_call, args.approval_reference, args.review)
        elif args.operation == 'verify':
            doc = domain.verify_transcript(root)
            result = {'operation': 'verify', 'outcome': 'READY', 'status': 'READY', 'reasons': [],
                      'project_id': doc['binding']['project_id'], 'transcript_id': doc['transcript_id']}
        elif args.operation == 'evaluate':
            doc=domain.verify_transcript(root); report=evaluate(doc,load_json(args.reference));atomic_json(args.output,report)
            result={'operation':'evaluate','outcome':report['result'],'status':'NEEDS_REVIEW' if report['result']=='HUMAN_REVIEW_REQUIRED' else 'INVALID',
                    'reasons':[],'path':str(Path(args.output).resolve()),'transcript_id':doc['transcript_id']}
        else:
            with project_lock(root):
                attempt = locate_execution(root, args.execution_id)
                if args.operation == 'normalize': result = normalize_attempt(root, attempt)
                else:
                    http = vendor.HTTP(); result = collect(root, attempt, http, (http.key,))
        print(canonical_bytes(result).decode(), end='')
        return {'READY': 0, 'NEEDS_REVIEW': 2, 'BLOCKED': 3, 'INVALID': 4}[result['status']]
    except (ContractError, OSError, KeyError, TypeError, ValueError, RecursionError) as error:
        if not isinstance(error, ContractError):
            error = ContractError('LOCAL_IO_OR_CONTRACT_FAILURE', 'Inspect local evidence without automatically retrying a provider call.')
        # No arbitrary exception message/path, argv, environment or HTTP body on stdout.
        print(canonical_bytes({'operation': args.operation if args else 'arguments', 'outcome': 'STOPPED',
                              'status': error.status, 'reasons': [{'code': error.code, 'field': '', 'action': 'Resolve retained evidence before continuing.'}]}).decode(), end='')
        return {'NEEDS_REVIEW': 2, 'BLOCKED': 3, 'INVALID': 4}.get(error.status, 3)


if __name__ == '__main__':
    sys.exit(main())
