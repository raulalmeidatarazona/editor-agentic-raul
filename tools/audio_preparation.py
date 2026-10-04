"""F003 lossless single-channel preparation from a freshly guarded F002 project."""
from __future__ import annotations

import csv
import os
import shutil
import uuid
import wave
from array import array
from fractions import Fraction
from pathlib import Path

from content_contract import (ContractError, atomic_json, digest, hash_file,
                              load_json, rational, safe_path, sync_directory, verify_project)
from media_inspection import Runner, tool_versions
from transcript_contract import binding, fraction

MAX_BYTES = 256 * 1024 * 1024
WINDOWS = [('opening', 0, 25), ('technical', 60, 85), ('correction', 90, 115),
           ('ordinary-again', 130, 155), ('ending', 195, 228),
           ('isolated-again-buffer', 96, 106), ('ordinary-again-buffer', 132, 148),
           ('pause-candidate', 35, 43)]


def blocked(code, field='audio', status='BLOCKED'):
    raise ContractError(code, 'Resolve preparation evidence before any provider submission.', field, status)


def check_tree(root):
    """No symlinks, including internal links, in the new F003 storage boundary."""
    tree = Path(root) / 'transcription'
    if tree.is_symlink() or (tree.exists() and any(p.is_symlink() for p in tree.rglob('*'))):
        blocked('UNSAFE_PATH', 'transcription')
    return tree


def sample_ledger(frames, stream, inspection, previous_rows):
    fs = stream['audio']['sample_rate_hz']
    tb = fraction(stream['time_base_s'])
    rows, count, next_time = [], 0, None
    for item in frames:
        if (type(item) is not dict or item.get('stream_index') != stream['index'] or
                type(item.get('pts')) is not int or type(item.get('nb_samples')) is not int or
                item['nb_samples'] <= 0 or type(item.get('duration')) is not int):
            blocked('AUDIO_FRAME_UNKNOWN')
        start = item['pts'] * tb
        duration = Fraction(item['nb_samples'], fs)
        if duration != item['duration'] * tb or (next_time is not None and start != next_time):
            blocked('AUDIO_DISCONTINUITY')
        rows.append((str(stream['index']), str(item['pts']), str(item['duration']), rational(tb)))
        next_time = start + duration
        count += item['nb_samples']
    if not rows or rows != previous_rows or len(rows) != inspection['timing']['audio_frame_count']:
        blocked('AUDIO_INSPECTION_MISMATCH')
    first = int(rows[0][1]) * tb
    zero = first - fraction(inspection['timing']['origin_media_s'])
    duration = Fraction(count, fs)
    if (zero != fraction(inspection['timing']['audio_start_s']) or
            zero + duration != fraction(inspection['timing']['audio_end_s'])):
        blocked('AUDIO_EXTENT_MISMATCH')
    return {'first_pts': rows[0][1], 'time_base_s': rational(tb),
            'decoded_frame_count': len(rows), 'sample_count': count,
            'sample_rate_hz': fs, 'audio_zero_source_s': rational(zero),
            'duration_s': rational(duration), 'continuity': 'CONTIGUOUS'}, rows


def validate_preparation(root, doc, bound, inspection):
    if (doc.get('schema_version') != 1 or type(doc.get('schema_version')) is not int or
            doc.get('kind') != 'source-audio-preparation' or doc.get('binding') != bound):
        blocked('PREPARATION_INVALID')
    descriptor = doc['identity']
    if doc['preparation_id'] != digest(descriptor) or descriptor['binding'] != bound:
        blocked('PREPARATION_IDENTITY_CHANGED')
    for k in ('channel_index', 'audio_sha256', 'sample_count', 'sample_rate_hz',
              'audio_zero_source_s', 'duration_s', 'ledger_sha256'):
        if doc[k] != descriptor[k]:
            blocked('PREPARATION_IDENTITY_CHANGED', k)
    if (type(doc['channel_index']) is not int or doc['channel_index'] not in (0, 1) or
            type(doc['sample_count']) is not int or doc['sample_count'] < 1 or
            type(doc['sample_rate_hz']) is not int or doc['sample_rate_hz'] < 1):
        blocked('PREPARATION_INVALID')
    audio = safe_path(root, doc['audio_path'])
    prefix = 'transcription/preparations/' + doc['preparation_id'] + '/'
    if doc['audio_path'] != prefix + 'audio.wav' or audio.is_symlink() or hash_file(audio) != doc['audio_sha256']:
        blocked('ARTIFACT_CHANGED', 'audio')
    ledger_path = safe_path(root, prefix + 'sample-ledger.tsv')
    if ledger_path.is_symlink() or hash_file(ledger_path) != doc['ledger_sha256']:
        blocked('ARTIFACT_CHANGED', 'sample-ledger')
    stream = next(s for s in inspection['streams'] if s['index'] == bound['audio_stream_index'])
    own_frames = []
    with ledger_path.open() as file:
        for row in csv.DictReader(file, delimiter='\t'):
            if row['time_base_s'] != stream['time_base_s']: blocked('AUDIO_INSPECTION_MISMATCH')
            own_frames.append({'stream_index': int(row['stream_index']), 'pts': int(row['pts']),
                               'duration': int(row['duration_ticks']), 'nb_samples': int(row['nb_samples'])})
    current = load_json(Path(root) / 'current.json')
    previous = []
    with safe_path(root, str(Path(current['inspection_path']).parent / 'frames.tsv')).open() as file:
        for row in csv.reader(file, delimiter='\t'):
            if row and row[0] == str(stream['index']): previous.append(tuple(row))
    measured, _ = sample_ledger(own_frames, stream, inspection, previous)
    for k, v in measured.items():
        if doc.get(k) != v: blocked('PREPARATION_TIMING_INVALID', k)
    with wave.open(str(audio), 'rb') as wav:
        if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes(), wav.getcomptype()) != (
                1, 2, doc['sample_rate_hz'], doc['sample_count'], 'NONE'):
            blocked('WAV_PROPERTIES_MISMATCH')
    duration = Fraction(doc['sample_count'], doc['sample_rate_hz'])
    zero = fraction(doc['audio_zero_source_s'])
    if (fraction(doc['duration_s']) != duration or zero != fraction(inspection['timing']['audio_start_s']) or
            zero + duration != fraction(inspection['timing']['audio_end_s']) or
            duration > 1800 or audio.stat().st_size > MAX_BYTES):
        blocked('PREPARATION_TIMING_INVALID')
    return doc


def prepare(root, channel):
    root = Path(root).resolve()
    project, current, inspection = verify_project(root)
    bound = binding(project, current, inspection)
    stream = next(s for s in inspection['streams'] if s['index'] == bound['audio_stream_index'])
    a = stream['audio']
    if (stream['codec'] not in {'pcm_s16be', 'pcm_s16le'} or a['bits_per_sample'] != 16 or
            a['sample_format'] != 's16' or a['channels'] not in (1, 2)):
        blocked('LOSSLESS_PCM16_REQUIRES_REVIEW', status='NEEDS_REVIEW')
    if type(channel) is not int or not 0 <= channel < a['channels']:
        blocked('CHANNEL_SELECTION_REQUIRED', status='NEEDS_REVIEW')
    tree = check_tree(root)
    parent = tree / 'preparations'; parent.mkdir(parents=True, exist_ok=True)
    # Valid reusable preparation: validate bytes, binding, and ledger; no writes.
    versions = tool_versions()
    preparer_version = 'f003-pcm16-v1/' + hash_file(Path(__file__))
    for path in sorted(parent.glob('*/preparation.json')):
        old = load_json(path)
        if (old.get('binding') == bound and old.get('channel_index') == channel and old.get('tool_versions') == versions and
                old.get('identity', {}).get('preparer_version') == preparer_version):
            validate_preparation(root, old, bound, inspection)
            return old
    work = parent / ('.work-' + str(uuid.uuid4())); work.mkdir()
    runner = Runner(work, timeout=600, limit=MAX_BYTES)
    source = safe_path(root, project['source']['path'])
    argv = ['ffprobe', '-v', 'error', '-select_streams', str(stream['index']), '-show_frames',
            '-show_entries', 'frame=stream_index,pts,duration,nb_samples', '-of', 'json', str(source)]
    out, _ = runner.run(argv, 'audio-frames')
    frames = load_json(out).get('frames', [])
    previous = []
    tsv = safe_path(root, str(Path(current['inspection_path']).parent / 'frames.tsv'))
    with tsv.open() as file:
        for row in csv.reader(file, delimiter='\t'):
            if row and row[0] == str(stream['index']):
                previous.append(tuple(row))
    ledger, rows = sample_ledger(frames, stream, inspection, previous)
    if fraction(ledger['duration_s']) > 1800 or ledger['sample_count'] * 2 + 4096 > MAX_BYTES:
        blocked('RESOURCE_LIMIT')
    ledger_path = work / 'sample-ledger.tsv'
    with ledger_path.open('x') as file:
        file.write('stream_index\tpts\tduration_ticks\ttime_base_s\tnb_samples\n')
        for row, frame in zip(rows, frames):
            file.write('\t'.join(row) + '\t' + str(frame['nb_samples']) + '\n')
        file.flush(); os.fsync(file.fileno())
    argv = ['ffmpeg', '-nostdin', '-v', 'error', '-i', str(source), '-map', '0:' + str(stream['index']),
            '-vn', '-sn', '-dn', '-af', f'pan=mono|c0=c{channel}', '-c:a', 'pcm_s16le',
            '-map_metadata', '-1', '-fflags', '+bitexact', '-flags:a', '+bitexact', '-n', str(work / 'audio.wav')]
    runner.run(argv, 'extract', stdout_limit=1024)
    audio = work / 'audio.wav'
    with wave.open(str(audio), 'rb') as wav:
        if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes()) != (
                1, 2, ledger['sample_rate_hz'], ledger['sample_count']):
            blocked('SAMPLE_COUNT_MISMATCH')
    if sum(p.stat().st_size for p in work.rglob('*') if p.is_file()) > MAX_BYTES:
        blocked('RESOURCE_LIMIT')
    descriptor = {'binding': bound, 'channel_index': channel, **{k: ledger[k] for k in (
        'sample_count', 'sample_rate_hz', 'audio_zero_source_s', 'duration_s')},
        'audio_sha256': hash_file(audio), 'ledger_sha256': hash_file(ledger_path),
        'tool_versions': versions, 'preparer_version': preparer_version}
    pid = digest(descriptor)
    doc = {'schema_version': 1, 'kind': 'source-audio-preparation', 'preparation_id': pid,
           'identity': descriptor, 'binding': bound, 'channel_index': channel, **ledger,
           'audio_path': f'transcription/preparations/{pid}/audio.wav', 'audio_sha256': descriptor['audio_sha256'],
           'ledger_sha256': descriptor['ledger_sha256'], 'tool_versions': versions,
           'commands': runner.commands, 'channel_layout': a['channel_layout'],
           'channel_review': 'HUMAN_REVIEW_REQUIRED', 'microphone_identity': None,
           'unknowns': {'microphone_identity': 'UNRESOLVED', **({'channel_layout': 'NOT_REPORTED'} if a['channel_layout'] is None else {})}}
    atomic_json(work / 'preparation.json', doc)
    if binding(*verify_project(root)) != bound:
        blocked('SOURCE_CHANGED')
    target = parent / pid
    if target.exists():
        existing = load_json(target / 'preparation.json')
        validate_preparation(root, existing, bound, inspection)
        shutil.rmtree(work)
        return existing
    os.rename(work, target); sync_directory(parent)
    for path in target.iterdir():
        if path.is_file(): path.chmod(0o444)
    return validate_preparation(root, doc, bound, inspection)


def listening_pack(root, preparation, destination):
    """Native samples and measured waveform; neither word boundaries nor acoustic verdicts."""
    root, destination = Path(root).resolve(), Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    full = safe_path(root, preparation['audio_path'])
    with wave.open(str(full), 'rb') as source:
        fs, samples = source.getframerate(), source.getnframes()
        zero = fraction(preparation['audio_zero_source_s'])
        evidence = []
        for name, low, high in WINDOWS:
            lo, hi = Fraction(low), min(Fraction(high), zero + Fraction(samples, fs))
            if lo < zero or hi <= lo: continue
            a, b = (lo - zero) * fs, (hi - zero) * fs
            if a.denominator != 1 or b.denominator != 1:
                blocked('PREVIEW_BOUNDARY_NOT_SAMPLE')
            clip = destination / (name + '.wav')
            if not clip.exists():
                source.setpos(int(a)); data = source.readframes(int(b-a))
                with wave.open(str(clip), 'wb') as sink:
                    sink.setnchannels(1); sink.setsampwidth(2); sink.setframerate(fs); sink.writeframes(data)
                # 20ms measured extrema give context, never automatic word alignment.
                values = array('h', data)
                import sys
                if sys.byteorder != 'little': values.byteswap()
                step = max(1, fs // 50)
                csv_path = destination / (name + '-waveform.csv')
                points = []
                with csv_path.open('x') as file:
                    file.write('source_start_s,source_end_s,min_pcm16,max_pcm16\n')
                    for j in range(0, len(values), step):
                        block = values[j:j+step]
                        file.write(f'{rational(lo+Fraction(j,fs))},{rational(lo+Fraction(j+len(block),fs))},{min(block)},{max(block)}\n')
                        x = 40 + 1160 * j / len(values)
                        points.append(f'M{x:.3f},{110-min(block)*90/32768:.3f}V{110-max(block)*90/32768:.3f}')
                (destination / (name + '-waveform.svg')).write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 240">'
                    '<rect width="1240" height="240" fill="white"/>'
                    f'<text x="40" y="24">{name}: source {float(lo):.3f}–{float(hi):.3f}s; 20ms extrema</text>'
                    '<path stroke="#177" stroke-width="1" d="' + ' '.join(points) + '"/>'
                    '<text x="40" y="228">Measured waveform; word boundaries require listening.</text></svg>')
            evidence.append({'name': name, 'source_start_s': rational(lo), 'source_end_s': rational(hi),
                             'sample_start': int(a), 'sample_end': int(b), 'path': str(clip.resolve()), 'sha256': hash_file(clip)})
    if sum(p.stat().st_size for p in destination.rglob('*') if p.is_file()) + full.stat().st_size > MAX_BYTES:
        blocked('RESOURCE_LIMIT', 'listening-pack')
    result = {'schema_version': 1, 'kind': 'source-listening-pack', 'binding': preparation['binding'],
              'preparation_id': preparation['preparation_id'], 'full_audio_path': str(full),
              'full_audio_sha256': preparation['audio_sha256'], 'channel_index': preparation['channel_index'],
              'windows': evidence, 'reference_status': 'HUMAN_REVIEW_REQUIRED'}
    atomic_json(destination / 'listening-pack.json', result)
    return result
