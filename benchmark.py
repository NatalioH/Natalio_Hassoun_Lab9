"""Uninstrumented repeat timings and sampled RSS, separate from profiler overhead."""
from pathlib import Path
import importlib.util
import json
import platform
import statistics
import sys
import timeit
from memory_profiler import memory_usage

ROOT = Path(__file__).resolve().parent

def load(version):
    spec = importlib.util.spec_from_file_location('workload_' + version, ROOT / version / 'profiler.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    results = {'environment': {'python': sys.version, 'platform': platform.platform()}, 'versions': {}}
    for version in ['before', 'after']:
        module = load(version)
        fast = getattr(module, 'fast_function' if version == 'before' else 'optimized_fast_function')
        item = {}
        for name, func, number in [('fast', fast, 20000), ('large', module.memory_intensive_function, 1), ('main', module.main, 1)]:
            samples = timeit.repeat(func, number=number, repeat=5 if name=='fast' else 3)
            item[name] = {'seconds_per_call': statistics.median(samples) / number, 'repetitions': number, 'samples_seconds': samples}
        samples = memory_usage((module.main, (), {}), interval=0.01, max_iterations=1)
        item['rss'] = {'min_mib': min(samples), 'peak_mib': max(samples), 'peak_minus_min_mib': max(samples) - min(samples), 'interval_seconds': 0.01}
        results['versions'][version] = item
        print(version, json.dumps(item, indent=2), flush=True)
    (ROOT / 'results/benchmark.json').write_text(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
