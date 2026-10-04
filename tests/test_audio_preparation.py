"""GENERATED TEST DATA: tiny AV fixtures, no real speech and no network."""
from __future__ import annotations
import copy
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import audio_preparation as audio
import ingest
from content_contract import ContractError, load_json, verify_project


def generated_project(base, audio_start='0.35', video_start='0.1', vfr=False):
    """PCM native 8kHz, 400 samples/frame: MKV ms PTS represent every block exactly."""
    base = Path(base); base.mkdir(parents=True, exist_ok=True)
    source = base / 'fixture.mkv'
    select = ",select='not(eq(n,3))'" if vfr else ''
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=blue:s=90x160:r=10:d=3',
               '-f', 'lavfi', '-i', 'aevalsrc=0.03*sin(2*PI*440*t)|0.02*sin(2*PI*880*t):s=8000:d=3:n=400',
               '-filter_complex', f'[0:v]setpts=PTS+{video_start}/TB{select}[v];[1:a]asetpts=PTS+{audio_start}/TB[a]',
               '-map', '[v]', '-map', '[a]', '-c:v', 'ffv1', '-c:a', 'pcm_s16le',
               '-fps_mode', 'passthrough', '-copyts', '-avoid_negative_ts', 'disabled', '-y', str(source)]
    subprocess.run(command, check=True, capture_output=True, timeout=30)
    if source.stat().st_size > 2*1024*1024: raise AssertionError('Fixture cap')
    (base / 'fixture-command.json').write_text(json.dumps({'label': 'GENERATED TEST DATA', 'argv': command}))
    result = ingest.ingest(source, 'f003-synthetic', base / 'projects')
    return Path(result['project_path'])


class AudioTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / '.local/validation/F003/tests'; parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent); self.base = Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()

    def test_native_channel_samples_positive_offset_and_reuse(self):
        root = generated_project(self.base)
        before = {p: p.stat().st_mtime_ns for p in root.rglob('*') if p.is_file()}
        p = audio.prepare(root, 0); second = audio.prepare(root, 1)
        self.assertEqual(p['audio_zero_source_s'], '1/4')  # independently .35-.1
        self.assertEqual(p['duration_s'], '3/1'); self.assertEqual(p['sample_count'], 24000)
        with wave.open(str(root / p['audio_path'])) as w:
            self.assertEqual((w.getnchannels(), w.getframerate(), w.getsampwidth()), (1, 8000, 2))
        # Oracle: select the original PCM channel independently using ffmpeg's sample map.
        original = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(self.base/'fixture.mkv'),
           '-map', '0:a:0', '-f', 's16le', '-c:a', 'pcm_s16le', '-'], capture_output=True, check=True).stdout
        import struct
        pairs = list(struct.iter_unpack('<hh', original))
        for ch, prepared in enumerate((p, second)):
            with wave.open(str(root / prepared['audio_path'])) as w: actual = w.readframes(w.getnframes())
            expected = b''.join(struct.pack('<h', row[ch]) for row in pairs)
            self.assertEqual(actual, expected)
        times = {f: f.stat().st_mtime_ns for f in (root / p['audio_path']).parent.iterdir()}
        self.assertEqual(audio.prepare(root, 0), p)
        self.assertEqual(times, {f: f.stat().st_mtime_ns for f in times})
        self.assertEqual(before, {f: f.stat().st_mtime_ns for f in before})

    def test_negative_audio_and_vfr_nonzero_video_pts(self):
        root = generated_project(self.base, audio_start='0.15', video_start='0.4', vfr=True)
        p = audio.prepare(root, 1); info = verify_project(root)[2]
        self.assertEqual(p['audio_zero_source_s'], '-1/4')
        self.assertEqual(info['timing']['origin_media_s'], '2/5')
        self.assertEqual(info['timing']['cadence'], 'VARYING')
        self.assertEqual(Fraction(p['audio_zero_source_s'])+Fraction(p['duration_s']), Fraction('11/4'))

    def test_gap_overlap_missing_priming_and_sample_discrepancy(self):
        root = generated_project(self.base)
        p = audio.prepare(root, 0); info = verify_project(root)[2]
        stream = info['streams'][1]
        frames = load_json((root / p['audio_path']).parent / 'audio-frames.stdout')['frames']
        rows = [(str(stream['index']), str(f['pts']), str(f['duration']), stream['time_base_s']) for f in frames]
        for mutate in (lambda f: f[1].update(pts=f[1]['pts']+1), lambda f: f[1].update(pts=f[1]['pts']-1),
                       lambda f: f[0].pop('pts'), lambda f: f[0].update(nb_samples=399),
                       lambda f: f[0].update(duration=49)):
            broken = copy.deepcopy(frames); mutate(broken)
            with self.assertRaises(ContractError): audio.sample_ledger(broken, stream, info, rows)

    def test_invalid_channel_symlink_and_tampered_wave(self):
        root = generated_project(self.base)
        for ch in (None, True, 2, -1):
            with self.assertRaises(ContractError): audio.prepare(root, ch)
        p = audio.prepare(root, 0); path = root/p['audio_path']; path.chmod(0o644)
        path.write_bytes(path.read_bytes()+b'x')
        with self.assertRaises(ContractError): audio.prepare(root, 0)
        link = root/'transcription/link'; link.symlink_to(root/'project.json')
        with self.assertRaises(ContractError): audio.check_tree(root)

    def test_tool_timeout_and_cap_leave_no_completed_preparation(self):
        root = generated_project(self.base)
        for code in ('TOOL_TIMEOUT', 'LIMIT_EXCEEDED'):
            with patch.object(audio.Runner, 'run', side_effect=ContractError(code, 'test')):
                with self.assertRaises(ContractError): audio.prepare(root, 0)
        self.assertFalse(list((root/'transcription/preparations').glob('*/preparation.json')))

if __name__ == '__main__': unittest.main()
