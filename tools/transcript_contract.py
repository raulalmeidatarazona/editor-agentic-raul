"""F003 source-transcript v1. No vendor payloads or editorial decisions."""
from __future__ import annotations

import hashlib
import math
import re
from fractions import Fraction
from pathlib import Path

from content_contract import (ContractError, atomic_json, canonical_bytes, digest,
                              hash_file, load_json, rational, safe_path, verify_project)

STATES = {'READY', 'NEEDS_REVIEW', 'BLOCKED', 'INVALID'}
UNKNOWN = {'NOT_REPORTED', 'NOT_REQUESTED', 'UNSUPPORTED', 'UNRESOLVED'}
BINDING = 'project_id source_id source_sha256 project_manifest_sha256 inspection_sha256 clock_id audio_stream_index'
PROVENANCE = 'execution_id response_sha256 request_fingerprint audio_sha256 preparation_sha256 normalization_version'
CLOCK = 'name unit representation interval provider_resolution_s audio_zero_source_s audio_end_source_s'
CORE = 'schema_version kind transcript_id binding provenance clock language text segments words readiness unknowns extensions'


def bad(field, code='CONTRACT_INVALID', status='INVALID'):
    raise ContractError(code, 'Inspect the retained evidence; do not reuse an invalid transcript.', field, status)


def keys(obj, names, field):
    if type(obj) is not dict or set(obj) != set(names.split()):
        bad(field)


def fraction(value, field='time'):
    if not isinstance(value, str) or not re.fullmatch(r'-?\d{1,64}/[1-9]\d{0,63}', value):
        bad(field)
    f = Fraction(value)
    if rational(f) != value:
        bad(field)
    return f


def sha(value, field):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
        bad(field)


def binding(project, current, inspection):
    return dict(project_id=project['project_id'], source_id=project['source']['id'],
                source_sha256=project['source']['sha256'],
                project_manifest_sha256=current['project_manifest_sha256'],
                inspection_sha256=current['inspection_sha256'],
                clock_id=inspection['timing']['clock_id'],
                audio_stream_index=inspection['selection']['audio_index'])


def version():
    return 'f003-v1/' + hash_file(Path(__file__))


def reasons(doc, preparation, inspection):
    """Derive structural readiness. Acoustic accuracy remains human validation."""
    out = []
    def add(code, field, status='BLOCKED'):
        out.append((status, {'code': code, 'field': field,
                             'action': 'Review the retained response and source timing; no automatic correction.'}))
    zero = fraction(preparation['audio_zero_source_s'])
    end = zero + fraction(preparation['duration_s'])
    timing = inspection['timing']
    alo, ahi = fraction(timing['audio_start_s']), fraction(timing['audio_end_s'])
    video_end = fraction(timing['video_end_s'])
    for group in ('segments', 'words'):
        rows = doc[group]
        if rows is None or not rows:
            add('WORD_TIMING_UNAVAILABLE' if group == 'words' else 'EMPTY_TRANSCRIPT', group)
            continue
        previous = None
        for row in rows:
            if row['start_s'] is None or row['end_s'] is None:
                add('TIMING_UNKNOWN', group + '/' + row['id'])
                continue
            start, stop = fraction(row['start_s']), fraction(row['end_s'])
            if stop <= start or start < max(zero, alo) or stop > min(end, ahi):
                add('TIMING_OUT_OF_BOUNDS', group + '/' + row['id'], 'INVALID')
            if previous and (start < previous[0] or stop < previous[1]):
                add('NONMONOTONIC_TIMING', group + '/' + row['id'], 'INVALID')
            previous = (start, stop)
            if start < 0 or stop > video_end:
                add('OUTSIDE_VIDEO', group + '/' + row['id'], 'NEEDS_REVIEW')
    collapse = lambda s: ' '.join(s.split())
    if doc['segments'] and collapse(' '.join(x['text'] for x in doc['segments'])) != collapse(doc['text']):
        add('TEXT_ALIGNMENT_MISMATCH', 'segments', 'NEEDS_REVIEW')
    if doc['words'] is not None and all(x['punctuation'] is not None for x in doc['words']):
        if collapse(''.join(x['text'] + x['punctuation'] for x in doc['words'])) != collapse(doc['text']):
            add('TEXT_ALIGNMENT_MISMATCH', 'words', 'NEEDS_REVIEW')
    rank = {'READY': 0, 'NEEDS_REVIEW': 1, 'BLOCKED': 2, 'INVALID': 3}
    status = max((x[0] for x in out), key=rank.get, default='READY')
    return {'status': status, 'reasons': [x[1] for x in out]}


def normalize(intermediate, bound, preparation, provenance, language, inspection,
              normalization_version=None):
    """Input uses generic audio-relative rational seconds; values are not repaired."""
    zero = fraction(preparation['audio_zero_source_s'])
    unknowns = {}
    def nullable(value, path, reason='NOT_REPORTED'):
        if value is None:
            unknowns[path] = reason
        return value
    def time(value, path):
        return nullable(None if value is None else rational(zero + fraction(value)), path)
    segments, words = [], []
    for i, segment in enumerate(intermediate['segments']):
        sid = f's{i+1:06d}'
        segments.append({'id': sid, 'text': segment['text'],
                         'start_s': time(segment['start_s'], f'/segments/{i}/start_s'),
                         'end_s': time(segment['end_s'], f'/segments/{i}/end_s'),
                         'confidence': nullable(segment.get('confidence'), f'/segments/{i}/confidence')})
        if segment['words'] is None:
            words = None
        elif words is not None:
            for word in segment['words']:
                j = len(words)
                words.append({'id': f'w{j+1:06d}', 'segment_id': sid, 'text': word['text'],
                              'punctuation': nullable(word.get('punctuation'), f'/words/{j}/punctuation'),
                              'start_s': time(word['start_s'], f'/words/{j}/start_s'),
                              'end_s': time(word['end_s'], f'/words/{j}/end_s'),
                              'confidence': nullable(word.get('confidence'), f'/words/{j}/confidence')})
    if words is None:
        unknowns = {k: v for k, v in unknowns.items() if not k.startswith('/words/')}
        unknowns['/words'] = 'UNSUPPORTED'
    doc = {'schema_version': 1, 'kind': 'source-transcript', 'binding': bound,
           'provenance': {**provenance, 'normalization_version': normalization_version or version()},
           'clock': {'name': 'source-presentation-v1', 'unit': 'seconds',
                     'representation': 'rational', 'interval': 'half-open',
                     'provider_resolution_s': nullable(intermediate.get('resolution_s'), '/clock/provider_resolution_s'),
                     'audio_zero_source_s': rational(zero),
                     'audio_end_source_s': rational(zero + fraction(preparation['duration_s']))},
           'language': {'declared': nullable(language['declared'], '/language/declared', 'NOT_REQUESTED'),
                        'requested': language['requested'],
                        'detected': nullable(intermediate.get('detected_language'), '/language/detected')},
           'text': intermediate['text'], 'segments': segments, 'words': words,
           'unknowns': unknowns, 'extensions': {}}
    doc['readiness'] = reasons(doc, preparation, inspection)
    doc['transcript_id'] = 'sha256:' + digest(doc)
    validate(doc, preparation, inspection)
    return doc


def validate(doc, preparation=None, inspection=None):
    keys(doc, CORE, 'transcript')
    if type(doc['schema_version']) is not int or doc['schema_version'] != 1 or doc['kind'] != 'source-transcript':
        bad('schema_version')
    if doc['transcript_id'] != 'sha256:' + digest({k: v for k, v in doc.items() if k != 'transcript_id'}):
        bad('transcript_id', 'ARTIFACT_CHANGED')
    keys(doc['binding'], BINDING, 'binding')
    b = doc['binding']
    for k in BINDING.split():
        if k.endswith('sha256') or k == 'clock_id':
            sha(b[k], k)
    if b['source_id'] != 'sha256:' + b['source_sha256'] or not isinstance(b['project_id'], str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', b['project_id']):
        bad('binding')
    if type(b['audio_stream_index']) is not int or b['audio_stream_index'] < 0:
        bad('audio_stream_index')
    keys(doc['provenance'], PROVENANCE, 'provenance')
    for k, v in doc['provenance'].items():
        if k.endswith('sha256') or k == 'request_fingerprint':
            sha(v, k)
        elif not isinstance(v, str) or not v:
            bad(k)
    keys(doc['clock'], CLOCK, 'clock')
    c = doc['clock']
    if (c['name'], c['unit'], c['representation'], c['interval']) != ('source-presentation-v1', 'seconds', 'rational', 'half-open'):
        bad('clock')
    fraction(c['audio_zero_source_s']); fraction(c['audio_end_source_s'])
    if c['provider_resolution_s'] is not None and fraction(c['provider_resolution_s']) <= 0:
        bad('provider_resolution_s')
    keys(doc['language'], 'declared requested detected', 'language')
    for k in ('declared', 'detected'):
        if doc['language'][k] is not None and (not isinstance(doc['language'][k], str) or not doc['language'][k]):
            bad('language/' + k)
    if type(doc['language']['requested']) is not list or any(not isinstance(x, str) or not x for x in doc['language']['requested']):
        bad('language/requested')
    if not isinstance(doc['text'], str):
        bad('text')
    ids = set()
    for group in ('segments', 'words'):
        rows = doc[group]
        if rows is None and group == 'words':
            continue
        if type(rows) is not list:
            bad(group)
        for index, row in enumerate(rows):
            keys(row, 'id text start_s end_s confidence' + (' segment_id punctuation' if group == 'words' else ''), group)
            if row['id'] != f'{"s" if group == "segments" else "w"}{index+1:06d}':
                bad(group + '/id')
            if group == 'segments':
                ids.add(row['id'])
            elif row['segment_id'] not in ids or (row['punctuation'] is not None and not isinstance(row['punctuation'], str)):
                bad('words/segment_id')
            if not isinstance(row['text'], str) or not row['text'].strip():
                bad(group + '/text')
            for k in ('start_s', 'end_s'):
                if row[k] is not None:
                    fraction(row[k], group + '/' + k)
            value = row['confidence']
            if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1):
                bad('confidence')
    nulls = set()
    def walk(v, path=''):
        if v is None:
            nulls.add(path)
        elif type(v) is dict:
            for k, item in v.items():
                walk(item, path + '/' + k.replace('~', '~0').replace('/', '~1'))
        elif type(v) is list:
            for i, item in enumerate(v):
                walk(item, path + '/' + str(i))
    for k in ('clock', 'language', 'segments', 'words'):
        walk(doc[k], '/' + k)
    if type(doc['unknowns']) is not dict or set(doc['unknowns']) != nulls or any(v not in UNKNOWN for v in doc['unknowns'].values()):
        bad('unknowns')
    if type(doc['extensions']) is not dict or any(not isinstance(k, str) or '.' not in k for k in doc['extensions']):
        bad('extensions')
    keys(doc['readiness'], 'status reasons', 'readiness')
    if doc['readiness']['status'] not in STATES or type(doc['readiness']['reasons']) is not list:
        bad('readiness')
    for item in doc['readiness']['reasons']:
        keys(item, 'code field action', 'reason')
        if any(not isinstance(x, str) for x in item.values()):
            bad('reason')
    if preparation is not None and inspection is not None and doc['readiness'] != reasons(doc, preparation, inspection):
        bad('readiness')
    if doc['readiness']['status'] == 'READY':
        if doc['readiness']['reasons'] or not doc['segments'] or not doc['words']:
            bad('readiness')
        for group in ('segments', 'words'):
            previous = None
            for row in doc[group]:
                if row['start_s'] is None or row['end_s'] is None:
                    bad('readiness')
                start, end = fraction(row['start_s']), fraction(row['end_s'])
                if end <= start or start < fraction(c['audio_zero_source_s']) or end > fraction(c['audio_end_source_s']) or (previous and (start < previous[0] or end < previous[1])):
                    bad('readiness')
                previous = start, end
    return doc


def _verify_transcript(root):
    root = Path(root).resolve()
    from audio_preparation import check_tree, validate_preparation
    check_tree(root)
    project, current, inspection = verify_project(root)
    pointer = load_json(safe_path(root, 'transcription/current.json'))
    keys(pointer, 'schema_version kind binding request_fingerprint artifacts normalization_version status reasons unknowns extensions', 'current')
    if pointer['schema_version'] != 1 or type(pointer['schema_version']) is not int or pointer['kind'] != 'current-source-transcript' or pointer['binding'] != binding(project, current, inspection):
        bad('current', 'BINDING_MISMATCH')
    if pointer['status'] != 'READY':
        raise ContractError('TRANSCRIPT_NOT_READY', 'Resolve the recorded transcription reasons.', 'current', pointer['status'])
    keys(pointer['artifacts'], 'execution preparation response transcript redaction request cost', 'artifacts')
    docs = {}
    for name, artifact in pointer['artifacts'].items():
        keys(artifact, 'path sha256', name)
        sha(artifact['sha256'], name)
        path = safe_path(root, artifact['path'])
        if not artifact['path'].startswith('transcription/') or path.is_symlink() or hash_file(path) != artifact['sha256']:
            bad(name, 'ARTIFACT_CHANGED')
        docs[name] = load_json(path)
    prep, exe, response, transcript = (docs[x] for x in ('preparation', 'execution', 'response', 'transcript'))
    validate_preparation(root, prep, pointer['binding'], inspection)
    request = docs['request']
    if (request.get('schema_version') != 1 or type(request.get('schema_version')) is not int or request.get('kind') != 'stt-request' or
            exe.get('schema_version') != 1 or type(exe.get('schema_version')) is not int or exe.get('kind') != 'stt-execution' or
            response.get('schema_version') != 1 or type(response.get('schema_version')) is not int or response.get('kind') != 'retained-stt-response'):
        bad('artifacts')
    inputs = {k: request[k] for k in ('binding', 'preparation_id', 'preparation_sha256', 'audio_sha256',
              'provider', 'model', 'region', 'scope', 'workspace', 'endpoint', 'configuration', 'adapter_version')}
    if digest(inputs) != request['request_fingerprint']:
        bad('request_fingerprint', 'ARTIFACT_CHANGED')
    if (exe['request_sha256'] != pointer['artifacts']['request']['sha256'] or
            exe['preparation_sha256'] != pointer['artifacts']['preparation']['sha256'] or
            exe['response_sha256'] != pointer['artifacts']['response']['sha256'] or
            request['preparation_sha256'] != pointer['artifacts']['preparation']['sha256'] or
            request['audio_sha256'] != prep['audio_sha256'] or request['preparation_id'] != prep['preparation_id']):
        bad('execution', 'BINDING_MISMATCH')
    keys(response['payloads'], 'submit queries terminal result', 'response/payloads')
    payloads = response['payloads']
    for payload in [payloads['submit'], *payloads['queries'], payloads['terminal']]:
        if (type(payload) is not dict or type(payload.get('output')) is not dict or
                payload['output'].get('task_id') != exe['job_id'] or payload.get('request_id') not in exe['request_ids']):
            bad('response', 'BINDING_MISMATCH')
    terminal = payloads['terminal']['output']
    results = terminal.get('results')
    if (terminal.get('task_status') != 'SUCCEEDED' or type(results) is not list or len(results) != 1 or
            results[0].get('subtask_status') != 'SUCCEEDED' or not payloads['queries'] or payloads['queries'][-1] != payloads['terminal']):
        bad('response', 'EXECUTION_INCOMPLETE')
    redaction, cost = docs['redaction'], docs['cost']
    if (redaction.get('schema_version') != 1 or type(redaction.get('schema_version')) is not int or
            redaction.get('kind') != 'stt-redaction-manifest' or redaction.get('execution_id') != exe['execution_id'] or
            redaction.get('response_sha256') != pointer['artifacts']['response']['sha256'] or
            cost.get('schema_version') != 1 or type(cost.get('schema_version')) is not int or
            cost.get('kind') != 'stt-execution-cost' or cost.get('execution_id') != exe['execution_id'] or
            cost.get('job_id') != exe['job_id'] or cost.get('prepared_duration_s') != prep['duration_s']):
        bad('external-evidence', 'BINDING_MISMATCH')
    expected_payloads = [('submit', payloads['submit']), *[('query', p) for p in payloads['queries']], ('result', payloads['result'])]
    if len(redaction.get('records', [])) != len(expected_payloads):
        bad('redaction', 'EXECUTION_INCOMPLETE')
    for record, (stage, payload) in zip(redaction['records'], expected_payloads):
        if record.get('stage') != stage or record.get('retained_payload_sha256') != digest(payload):
            bad('redaction', 'ARTIFACT_CHANGED')
        sha(record.get('wire_sha256'), 'wire_sha256')
    for name in ('preparation', 'execution', 'response', 'request'):
        if docs[name]['binding'] != pointer['binding']:
            bad(name, 'BINDING_MISMATCH')
    if exe.get('completed') is not True or exe.get('phase') != 'SUCCEEDED' or exe.get('status') != 'READY':
        bad('execution', 'EXECUTION_INCOMPLETE')
    if response['execution_id'] != exe['execution_id'] or transcript['provenance']['execution_id'] != exe['execution_id']:
        bad('execution_id', 'BINDING_MISMATCH')
    if pointer['request_fingerprint'] != exe['request_fingerprint'] or response['request_fingerprint'] != exe['request_fingerprint'] or docs['request']['request_fingerprint'] != exe['request_fingerprint'] or transcript['provenance']['request_fingerprint'] != exe['request_fingerprint']:
        bad('request_fingerprint', 'BINDING_MISMATCH')
    if prep['audio_sha256'] != hash_file(safe_path(root, prep['audio_path'])):
        bad('audio', 'ARTIFACT_CHANGED')
    for k, name in [('response_sha256', 'response'), ('preparation_sha256', 'preparation')]:
        if transcript['provenance'][k] != pointer['artifacts'][name]['sha256']:
            bad(k, 'BINDING_MISMATCH')
    if transcript['provenance']['audio_sha256'] != prep['audio_sha256'] or transcript['binding'] != pointer['binding'] or transcript['provenance']['normalization_version'] != pointer['normalization_version']:
        bad('provenance', 'BINDING_MISMATCH')
    validate(transcript, prep, inspection)
    if (transcript['clock']['audio_zero_source_s'] != prep['audio_zero_source_s'] or
            fraction(transcript['clock']['audio_end_source_s']) != fraction(prep['audio_zero_source_s']) + fraction(prep['duration_s'])):
        bad('clock', 'BINDING_MISMATCH')
    if transcript['readiness']['status'] != 'READY':
        bad('transcript', 'TRANSCRIPT_NOT_READY')
    if binding(*verify_project(root)) != pointer['binding']:
        bad('source', 'BINDING_MISMATCH')
    return transcript


def verify_transcript(root):
    """Public consumer boundary: malformed artifacts always produce a safe stop."""
    try:
        return _verify_transcript(root)
    except ContractError:
        raise
    except (OSError, KeyError, TypeError, ValueError, AttributeError, RecursionError):
        bad('artifacts', 'ARTIFACT_UNAVAILABLE_OR_INVALID')
