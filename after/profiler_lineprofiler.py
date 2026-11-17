"""Run line_profiler on the complete, unchanged-size lab workload."""
from line_profiler import LineProfiler
import profiler


def main():
    lp = LineProfiler()
    for name in ['slow_function', 'optimized_fast_function', 'memory_intensive_function', 'sum_of_squares']:
        lp.add_function(getattr(profiler, name))
    lp.runcall(profiler.main)
    lp.print_stats(output_unit=1e-6)
    lp.dump_stats("line_profile.lprof")


if __name__ == "__main__":
    main()
