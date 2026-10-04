"""Replaceable F003 Qwen Filetrans adapter. HTTP is opt-in; no SDK or upload."""
from __future__ import annotations

import hashlib
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from content_contract import ContractError, canonical_bytes, hash_file, rational

MODEL = 'qwen-audio-3.1-asr-flash-filetrans'
MAX_JSON = 16 * 1024 * 1024
LIMITS = {'audio_seconds': 1800, 'evidence_bytes': 256 * 1024 * 1024,
          'vendor_json_bytes': MAX_JSON, 'stderr_bytes': 2 * 1024 * 1024,
          'ffmpeg_timeout_s': 600, 'post_timeout_s': 60, 'post_retries': 0,
          'poll_interval_s': 5, 'poll_deadline_s': 1800, 'get_retries': 3}
PRICE_URL = 'https://www.alibabacloud.com/help/en/model-studio/model-pricing'
LANGUAGES = set('zh en ja ko vi th id ms tl hi ar fr de es pt ru it nl sv da fi no el pl cs hu ro bg hr sk'.split())
IDENTIFIER = re.compile(r'[A-Za-z0-9_-]{1,128}')
OSS = re.compile(r'[a-z0-9][a-z0-9-]*\.oss-ap-southeast-1\.aliyuncs\.com')


def fail(code, field='provider', status='BLOCKED'):
    raise ContractError(code, 'Resolve the retained diagnostic; never automatically resubmit.', field, status)


def adapter_version():
    return 'qwen-filetrans-v1/' + hash_file(Path(__file__))


def resolve_configuration(value, require_workspace=True, validate=True):
    """Account coordinates belong to this adapter, never to the transcript domain.

    The resolved workspace is retained as non-secret execution identity. The key
    stays exclusively in HTTP memory. No environment values are echoed.
    """
    resolved = dict(value)
    if resolved.get('workspace') is None:
        resolved['workspace'] = os.environ.get('F003_QWEN_WORKSPACE') or None
    return config(resolved, require_workspace=require_workspace) if validate else resolved


def config(value, require_workspace=True):
    expected = set('schema_version provider model region scope workspace language channel_index vocabulary context limits'.split())
    if type(value) is not dict or set(value) != expected or type(value['schema_version']) is not int or value['schema_version'] != 1:
        fail('CONFIG_INVALID', status='INVALID')
    if (value['provider'], value['model'], value['region'], value['scope']) != ('alibaba-model-studio', MODEL, 'ap-southeast-1', 'International'):
        fail('UNSUPPORTED_PROVIDER_CONFIGURATION', status='INVALID')
    if value['workspace'] is None and not require_workspace:
        pass
    elif not isinstance(value['workspace'], str) or not re.fullmatch('[a-z0-9][a-z0-9-]{0,63}', value['workspace']):
        fail('WORKSPACE_REQUIRED')
    if value['channel_index'] is not None and (type(value['channel_index']) is not int or value['channel_index'] not in (0, 1)):
        fail('CONFIG_INVALID', 'channel_index', 'INVALID')
    lang = value['language']
    if (type(lang) is not dict or set(lang) != {'declared', 'requested'} or
            (lang['declared'] is not None and lang['declared'] not in LANGUAGES) or
            type(lang['requested']) is not list or len(lang['requested']) > 4 or
            len(set(lang['requested'])) != len(lang['requested']) or any(x not in LANGUAGES for x in lang['requested'])):
        fail('UNSUPPORTED_LANGUAGE_CONFIGURATION', status='INVALID')
    vocab = value['vocabulary']
    if vocab is not None and (type(vocab) is not dict or len(vocab) > 32 or any(
            not isinstance(k, str) or not k.strip() or len(k) > 64 or type(v) is not int or not 1 <= v <= 5 for k, v in vocab.items())):
        fail('UNSUPPORTED_VOCABULARY', status='INVALID')
    context = value['context']
    if context is not None and (type(context) is not dict or set(context) != {'text'} or
                                not isinstance(context['text'], str) or not 1 <= len(context['text']) <= 400):
        fail('UNSUPPORTED_CONTEXT', status='INVALID')
    if value['limits'] != LIMITS:
        fail('UNSUPPORTED_LIMITS', status='INVALID')
    return value


def endpoint(settings):
    return 'https://' + settings['workspace'] + '.ap-southeast-1.maas.aliyuncs.com/api/v1'


def request_body(settings, audio_url):
    config(settings)
    body = {'model': settings['model'], 'input': {'file_urls': [audio_url]},
            'parameters': {'channel_id': [0], 'language_hints': settings['language']['requested'], 'diarization_enabled': False}}
    if settings['vocabulary'] is not None:
        body['parameters']['vocabulary'] = settings['vocabulary']
    if settings['context'] is not None:
        body['input']['context'] = [{'role': 'user', 'content': [{'type': 'input_text', 'text': settings['context']['text']}]}]
    return body


def object_url(url, signed=False, now=None):
    """Allow only existing Singapore OSS over TLS, never redirects or embedded credentials."""
    try:
        parts = urllib.parse.urlsplit(url)
        if (parts.scheme != 'https' or parts.username or parts.password or parts.port not in (None, 443) or
                parts.fragment or not OSS.fullmatch(parts.hostname or '') or not parts.path or parts.path == '/'):
            fail('TRANSPORT_HOST_UNAUTHORIZED')
        pairs = urllib.parse.parse_qsl(parts.query, strict_parsing=True)
        if len(pairs) != len(dict(pairs)):
            fail('TRANSPORT_SIGNATURE_INVALID')
        query = {k.casefold(): v for k, v in pairs}
        expiry = None
        if 'signature' in query and 'expires' in query and 'ossaccesskeyid' in query:
            expiry = int(query['expires'])
        elif 'x-oss-signature' in query and 'x-oss-date' in query and 'x-oss-expires' in query and 'x-oss-credential' in query:
            date = datetime.strptime(query['x-oss-date'], '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)
            expiry = int(date.timestamp()) + int(query['x-oss-expires'])
        if signed:
            remaining = (expiry - (time.time() if now is None else now)) if expiry is not None else -1
            if not 1800 <= remaining <= 7200:
                fail('TRANSPORT_TTL_INVALID')
        return {'host': parts.hostname, 'expires_at_epoch_s': expiry}
    except (ValueError, TypeError, AttributeError):
        fail('TRANSPORT_SIGNATURE_INVALID')


def parse_json(raw):
    if len(raw) > MAX_JSON:
        fail('RESPONSE_LIMIT')
    def unique(pairs):
        out = {}
        for k, v in pairs:
            if k in out: fail('MALFORMED_RESPONSE')
            out[k] = v
        return out
    def nonfinite(_): fail('MALFORMED_RESPONSE')
    try:
        result = json.loads(raw.decode('utf-8'), object_pairs_hook=unique, parse_constant=nonfinite)
        if type(result) is not dict: fail('MALFORMED_RESPONSE')
        return result
    except (UnicodeError, ValueError, RecursionError):
        fail('MALFORMED_RESPONSE')


def sanitize(payload, secrets=()):
    removed = []
    secret_values = tuple(dict.fromkeys(y for x in secrets if x for y in (x, urllib.parse.quote(x, safe=''), urllib.parse.quote_plus(x))))
    key_pattern = re.compile(r'^(authorization|(?:x[-_])?api[_-]?key|access[_-]?key(?:[_-]?(?:id|secret))?|secret|password|(?:security[_-]?)?token|signature|credential|file_url|file_urls|transcription_url|x-oss-(?:signature|credential|security-token))$', re.I)
    url_pattern = re.compile(r'https?://[^\s\"<>]+', re.I)
    def signed_url(m):
        text = m.group(0)
        parsed = urllib.parse.urlsplit(text)
        if parsed.username or parsed.password or re.search(r'(signature|credential|token|ossaccesskeyid)=', parsed.query, re.I):
            return '[REDACTED_TRANSPORT]'
        return text
    def walk(value, path='', recognition=False):
        if type(value) is dict:
            result = {}
            for k, v in value.items():
                if any(s in k for s in secret_values): fail('UNSAFE_RESPONSE')
                p = path + '/' + k.replace('~', '~0').replace('/', '~1')
                if key_pattern.fullmatch(k):
                    removed.append({'path': p, 'reason': 'TRANSPORT_OR_AUTH'}); result[k] = '[REDACTED_TRANSPORT]'
                else:
                    result[k] = walk(v, p, recognition or k in ('transcripts', 'sentences', 'words'))
            return result
        if type(value) is list:
            return [walk(v, path + '/' + str(i), recognition) for i, v in enumerate(value)]
        if isinstance(value, str):
            clean = value
            for s in secret_values: clean = clean.replace(s, '[REDACTED_SECRET]')
            clean = url_pattern.sub(signed_url, clean)
            # Bearer echoes must be removed even when no known credential was supplied.
            clean = re.sub(r'Bearer\s+[A-Za-z0-9._~+/-]+', '[REDACTED_AUTH]', clean, flags=re.I)
            if clean != value:
                if recognition: fail('UNSAFE_RESPONSE')
                removed.append({'path': path, 'reason': 'SECRET_OR_SIGNED_URL_ECHO'})
            return clean
        return value
    return walk(payload), removed


def safe_payload(raw, secrets=()):
    clean, paths = sanitize(parse_json(raw), secrets)
    return clean, {'wire_sha256': hashlib.sha256(raw).hexdigest(),
                   'retained_payload_sha256': hashlib.sha256(canonical_bytes(clean)).hexdigest(), 'redactions': paths}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class HTTP:
    def __init__(self, key=None, opener=None, sleep=time.sleep, clock=time.monotonic):
        self.key = key if key is not None else os.environ.get('DASHSCOPE_API_KEY', '')
        self.open = opener or urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect(),
                urllib.request.HTTPSHandler(context=ssl.create_default_context())).open
        self.sleep, self.clock = sleep, clock

    def _read(self, response, maximum):
        pieces, total = [], 0
        while True:
            part = response.read(min(65536, maximum - total + 1))
            if not part: break
            total += len(part)
            if total > maximum: fail('RESPONSE_LIMIT')
            pieces.append(part)
        return b''.join(pieces)

    def request(self, method, url, body=None, authenticated=False, deadline=None):
        deadline = self.clock() + 1800 if deadline is None else deadline
        if method not in ('GET', 'POST'): fail('HTTP_METHOD_INVALID')
        headers = {}
        if authenticated:
            if not self.key or '\n' in self.key or '\r' in self.key: fail('CREDENTIAL_UNAVAILABLE')
            host = urllib.parse.urlsplit(url).hostname or ''
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*\.ap-southeast-1\.maas\.aliyuncs\.com', host): fail('AUTH_HOST_UNAUTHORIZED')
            headers['Authorization'] = 'Bearer ' + self.key
        else:
            object_url(url)
        if method == 'POST':
            headers.update({'Content-Type': 'application/json', 'X-DashScope-Async': 'enable'})
        req = urllib.request.Request(url, data=canonical_bytes(body) if body is not None else None, headers=headers, method=method)
        for retry in range(4 if method == 'GET' else 1):
            remaining = deadline - self.clock()
            if remaining <= 0: fail('GET_DEADLINE')
            try:
                with self.open(req, timeout=min(60, remaining)) as response:
                    if not 200 <= response.status < 300: fail('HTTP_UNEXPECTED_STATUS')
                    return self._read(response, MAX_JSON)
            except urllib.error.HTTPError as error:
                code, retry_after = error.code, error.headers.get('Retry-After', '')
                error.close()
                if method == 'POST': fail('POST_REJECTED' if code < 500 else 'SUBMISSION_UNKNOWN')
                if code not in (429, 500, 502, 503, 504): fail('HTTP_' + str(code))
                delay = 2 ** retry
                if retry_after:
                    try: delay = max(delay, int(retry_after))
                    except ValueError:
                        from email.utils import parsedate_to_datetime
                        try: delay = max(delay, parsedate_to_datetime(retry_after).timestamp() - time.time())
                        except (ValueError, TypeError): pass
            except (urllib.error.URLError, TimeoutError, OSError):
                if method == 'POST': fail('SUBMISSION_UNKNOWN')
                delay = 2 ** retry
            if retry == 3 or delay >= deadline - self.clock(): fail('GET_RETRIES_EXHAUSTED')
            self.sleep(delay)
        fail('GET_RETRIES_EXHAUSTED')

    def transport(self, url, audio_sha256, audio_bytes):
        meta = object_url(url, signed=True)
        deadline = self.clock() + 1800
        # Stream instead of collecting the audio in memory; no credential header.
        request = urllib.request.Request(url, method='GET')
        digest = hashlib.sha256(); count = 0
        for retry in range(4):
            try:
                digest = hashlib.sha256(); count = 0
                remaining = deadline - self.clock()
                if remaining <= 0: fail('GET_DEADLINE')
                with self.open(request, timeout=min(60, remaining)) as response:
                    if response.status != 200: fail('TRANSPORT_UNAVAILABLE')
                    while True:
                        if self.clock() >= deadline: fail('GET_DEADLINE')
                        chunk = response.read(65536)
                        if not chunk: break
                        count += len(chunk)
                        if count > audio_bytes: fail('TRANSPORT_BYTES_MISMATCH')
                        digest.update(chunk)
                break
            except urllib.error.HTTPError as error:
                code, retry_after = error.code, error.headers.get('Retry-After', '')
                error.close()
                if code not in (429, 500, 502, 503, 504): fail('TRANSPORT_UNAVAILABLE')
                delay = 2 ** retry
                if retry_after:
                    try: delay = max(delay, int(retry_after))
                    except ValueError:
                        from email.utils import parsedate_to_datetime
                        try: delay = max(delay, parsedate_to_datetime(retry_after).timestamp() - time.time())
                        except (ValueError, TypeError): pass
            except (urllib.error.URLError, OSError, TimeoutError): delay = 2 ** retry
            if retry == 3 or delay >= deadline - self.clock(): fail('TRANSPORT_UNAVAILABLE')
            self.sleep(delay)
        if count != audio_bytes or digest.hexdigest() != audio_sha256: fail('TRANSPORT_HASH_MISMATCH')
        object_url(url, signed=True)  # remaining TTL after the download
        return {**meta, 'sha256': digest.hexdigest(), 'bytes': count, 'status': 'VERIFIED'}


def job(payload, expected=None):
    if type(payload.get('output')) is not dict: fail('JOB_RESPONSE_INVALID')
    output = payload['output']
    jid, rid, status = output.get('task_id'), payload.get('request_id'), output.get('task_status')
    if not isinstance(jid, str) or not IDENTIFIER.fullmatch(jid) or not isinstance(rid, str) or not IDENTIFIER.fullmatch(rid):
        fail('JOB_ID_INVALID')
    if expected is not None and jid != expected: fail('JOB_ID_MISMATCH')
    if status not in ('PENDING', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELED', 'UNKNOWN'):
        fail('JOB_STATUS_INVALID')
    return jid, rid, status


def result_url(payload, expected):
    _, _, status = job(payload, expected)
    if status != 'SUCCEEDED': fail('JOB_' + status)
    rows = payload['output'].get('results')
    if type(rows) is not list or len(rows) != 1 or type(rows[0]) is not dict or rows[0].get('subtask_status') != 'SUCCEEDED':
        fail('SUBTASK_INCOMPLETE')
    metrics = payload['output'].get('task_metrics')
    if metrics is not None and (type(metrics) is not dict or any(type(metrics.get(k)) is not int or metrics[k] != n
            for k,n in (('TOTAL',1),('SUCCEEDED',1),('FAILED',0)))):
        fail('SUBTASK_INCOMPLETE')
    url = rows[0].get('transcription_url')
    object_url(url)
    return url


def intermediate(result, preparation):
    """Only structure and units are adapted. Unreported confidence/language remain absent."""
    props, tracks = result.get('properties'), result.get('transcripts')
    if (type(props) is not dict or type(tracks) is not list or len(tracks) != 1 or
            type(tracks[0]) is not dict or type(tracks[0].get('channel_id')) is not int or tracks[0]['channel_id'] != 0):
        fail('RESULT_CHANNEL_INVALID', status='INVALID')
    if (type(props.get('original_sampling_rate')) is not int or props['original_sampling_rate'] != preparation['sample_rate_hz'] or
            props.get('channels') != [0] or any(type(x) is not int for x in props['channels']) or
            props.get('audio_format') not in ('wav', 'pcm_s16le')):
        fail('RESULT_MEDIA_MISMATCH', status='INVALID')
    ms = props.get('original_duration_in_milliseconds')
    if type(ms) is not int or abs(Fraction(ms, 1000) - Fraction(preparation['duration_s'])) > Fraction(1, 1000) + Fraction(1, preparation['sample_rate_hz']):
        fail('RESULT_DURATION_MISMATCH', status='INVALID')
    track = tracks[0]
    if not isinstance(track.get('text'), str) or type(track.get('sentences')) is not list:
        fail('RESULT_TEXT_INVALID', status='INVALID')
    def timestamp(row, key):
        value = row.get(key)
        if value is None: return None
        if type(value) is not int: fail('RESULT_TIME_INVALID', status='INVALID')
        return rational(Fraction(value, 1000))
    segments = []
    for row in track['sentences']:
        if type(row) is not dict or not isinstance(row.get('text'), str): fail('RESULT_TEXT_INVALID', status='INVALID')
        words = row.get('words')
        if words is not None and type(words) is not list: fail('RESULT_WORDS_INVALID', status='INVALID')
        parsed = None if words is None else []
        for word in words or []:
            if type(word) is not dict or not isinstance(word.get('text'), str): fail('RESULT_WORDS_INVALID', status='INVALID')
            punctuation = word.get('punctuation')
            if punctuation is not None and not isinstance(punctuation, str): fail('RESULT_WORDS_INVALID', status='INVALID')
            parsed.append({'text': word['text'], 'punctuation': punctuation,
                           'start_s': timestamp(word, 'begin_time'), 'end_s': timestamp(word, 'end_time')})
        segments.append({'text': row['text'], 'start_s': timestamp(row, 'begin_time'),
                         'end_s': timestamp(row, 'end_time'), 'words': parsed})
    return {'text': track['text'], 'segments': segments, 'resolution_s': '1/1000'}


def cost(execution, terminal, pricing):
    """Final usage only, no duration-to-token inference or accumulated polling sums."""
    usage = terminal.get('usage')
    unknowns = {}
    def unknown(value, key, reason='NOT_REPORTED'):
        if value is None: unknowns[key] = reason
        return value
    counts = []
    for key in ('input_tokens', 'output_tokens'):
        v = usage.get(key) if type(usage) is dict else None
        if v is not None and (type(v) is not int or v < 0): fail('USAGE_INVALID', status='INVALID')
        counts.append(unknown(v, '/' + key))
    total = per_min = per_hour = None
    if all(v is not None for v in counts):
        total = (Decimal(counts[0]) * Decimal(pricing['input_usd_per_million']) + Decimal(counts[1]) * Decimal(pricing['output_usd_per_million'])) / Decimal(1000000)
        duration = Fraction(execution['audio_duration_s'])
        if duration <= 0: fail('COST_DURATION_INVALID')
        per_min = total * Decimal(60) * Decimal(duration.denominator) / Decimal(duration.numerator)
        per_hour = per_min * 60
    doc = {'schema_version': 1, 'kind': 'stt-execution-cost', 'execution_id': execution['execution_id'],
           **{k: execution[k] for k in ('provider', 'model', 'region', 'job_id', 'request_ids')},
           'original_duration_s': execution['original_duration_s'], 'prepared_duration_s': execution['audio_duration_s'],
           'vendor_usage': unknown(usage, '/vendor_usage'), 'input_tokens': counts[0], 'output_tokens': counts[1],
           'metered_speech_duration': unknown(usage.get('duration') if type(usage) is dict else None, '/metered_speech_duration'),
           'pricing_snapshot': pricing,
           'calculated_list_cost_usd': unknown(str(total) if total is not None else None, '/calculated_list_cost_usd', 'UNRESOLVED'),
           'effective_usd_per_audio_minute': unknown(str(per_min) if per_min is not None else None, '/effective_usd_per_audio_minute', 'UNRESOLVED'),
           'extrapolated_usd_per_hour': unknown(str(per_hour) if per_hour is not None else None, '/extrapolated_usd_per_hour', 'UNRESOLVED'),
           'billing_amount': unknown(None, '/billing_amount', 'UNRESOLVED'), 'billing_currency': unknown(None, '/billing_currency', 'UNRESOLVED'),
           'reconciliation': {'status': 'PENDING', 'reference': None},
           'storage_cost': unknown(None, '/storage_cost', 'UNRESOLVED'), 'transfer_cost': unknown(None, '/transfer_cost', 'UNRESOLVED')}
    unknowns['/reconciliation/reference'] = 'UNRESOLVED'; doc['unknowns'] = unknowns
    return doc
