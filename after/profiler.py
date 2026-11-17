"""Equivalent workloads using the exact sum-of-squares identity."""
import time


def sum_of_squares(n):
    """Return sum(i*i for i in range(n)) without allocating a sequence."""
    return n * (n - 1) * (2 * n - 1) // 6


def slow_function():
    # Keep the lab's intentional delay; do not hide it from the profiler.
    time.sleep(2)
    return sum_of_squares(10000)


def optimized_fast_function():
    return sum_of_squares(100)


def memory_intensive_function():
    return sum_of_squares(10000000)


def main():
    slow_function()
    optimized_fast_function()
    memory_intensive_function()


if __name__ == "__main__":
    main()
