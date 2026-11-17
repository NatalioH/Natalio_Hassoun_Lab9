"""Reproduce the submitted profiler logs and coverage HTML from the repo root."""
from pathlib import Path
import subprocess
import sys
import time
import json

ROOT = Path(__file__).resolve().parent

def run_all():
    measurements = {}
    for version in ['before', 'after']:
        cwd = ROOT / version
        dest = ROOT / 'results' / version
        dest.mkdir(parents=True, exist_ok=True)
        commands = {
            'cprofile': ['-m', 'cProfile', '-s', 'time', 'profiler.py'],
            'line_profiler': ['profiler_lineprofiler.py'],
            'memory_profiler': ['-m', 'memory_profiler', 'profiler_memoryprofiler.py'],
            'tests': ['-m', 'unittest', '-v', 'test_profiler'],
            'coverage_run': ['-m', 'coverage', 'run', '--branch', '--source=profiler', '-m', 'unittest', 'discover', '-v'],
            'coverage': ['-m', 'coverage', 'report', '-m'],
            'coverage_html': ['-m', 'coverage', 'html', '-d', str(dest / 'htmlcov')],
            'coverage_json': ['-m', 'coverage', 'json', '-o', str(dest / 'coverage.json')],
        }
        measurements[version] = {}
        for name, args in commands.items():
            start = time.perf_counter()
            done = subprocess.run([sys.executable, *args], cwd=cwd,
                                  text=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
            elapsed = time.perf_counter() - start
            (dest / (name + '.txt')).write_text(
                f'lab9_Nathalio_Hassoun/{version}$ python ' + ' '.join(args) + '\n\n' + done.stdout + f'\nExit code: {done.returncode}\n')
            if done.returncode:
                raise RuntimeError(done.stdout)
            measurements[version][name] = elapsed
            print(version, name, f'{elapsed:.4f}s', flush=True)
    (ROOT / 'results' / 'command_wall_times.json').write_text(json.dumps(measurements, indent=2))

if __name__ == '__main__':
    run_all()
