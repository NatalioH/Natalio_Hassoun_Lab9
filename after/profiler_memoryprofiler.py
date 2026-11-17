"""Measure RSS at workload-call boundaries without tracing 10M loop lines."""
from memory_profiler import profile
import profiler


@profile(precision=4)
def main():
    slow_result = profiler.slow_function()
    fast_result = profiler.optimized_fast_function()
    large_result = profiler.memory_intensive_function()
    return slow_result, fast_result, large_result


if __name__ == "__main__":
    main()
