"""Correctness tests with diagnostic wall-time and RSS measurements."""
import time
import unittest
from memory_profiler import memory_usage
import profiler


class TestProfiler(unittest.TestCase):
    def time_function(self, func):
        start = time.perf_counter()
        result = func()
        duration = time.perf_counter() - start
        print(f"{func.__name__}: {duration:.9f} seconds", flush=True)
        return result, duration

    def test_slow_function(self):
        result, duration = self.time_function(profiler.slow_function)
        self.assertEqual(result, 333283335000)
        self.assertGreaterEqual(duration, 2.0)

    def test_fast_function(self):
        result, _ = self.time_function(profiler.fast_function)
        self.assertEqual(result, 328350)

    def test_memory_intensive_function(self):
        before = memory_usage(-1, interval=0.01, timeout=0.01)[0]
        result, _ = self.time_function(profiler.memory_intensive_function)
        after = memory_usage(-1, interval=0.01, timeout=0.01)[0]
        print(f"RSS before: {before:.4f} MiB; after: {after:.4f} MiB")
        self.assertEqual(result, 333333283333335000000)
        self.assertGreater(before, 0)
        self.assertGreater(after, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
