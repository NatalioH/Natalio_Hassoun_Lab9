# Lab 9 Python Profiling

**Nathalio Hassoun** · Software Tools Lab · Fall 2026–2027

This submission includes the original and optimized programs, real profiling
results, complete coverage HTML, and the required Word report with ten terminal
snapshots and analysis.

## Submission files

| Required item | Location |
| --- | --- |
| Word report with all before/after snapshots and analysis | [lab9_Nathalio_Hassoun.docx](lab9_Nathalio_Hassoun.docx) |
| Complete submission including raw logs and screenshots | [Lab9_Submission.zip](Lab9_Submission.zip) |
| Original four code files | [before/](before/) |
| Optimized four code files | [after/](after/) |
| Coverage HTML entry point | [index.html](index.html) |
| Original coverage report and assets | [coverage_before/index.html](coverage_before/index.html) |
| Optimized coverage report and assets | [coverage_after/index.html](coverage_after/index.html) |

Download or clone the repository before opening HTML locally; GitHub shows HTML
source rather than executing the coverage viewer. Keep each coverage directory's
CSS and JavaScript files together with its index.html.

## Measured results

| Measurement | Before | After |
| --- | --- | --- |
| Full workload median | 2.535 s | 2.001 s |
| Fast function median | 3.679 microseconds | 0.106 microseconds |
| Ten-million-term calculation median | 0.524 s | Below 2 microseconds in all three samples |
| Tests | 3 passed | 5 passed |
| Combined statement and branch coverage | 83.9% (displayed 84%) | 100% |

The optimized implementation uses the exact sum-of-squares identity and calls
`optimized_fast_function` in all optimized scripts and tests. The intentional
two-second sleep remains. The full workload improved by approximately 21.1%.
Measurements used Python 3.12.14 on Linux and are environment-specific.

The original large loop retains an accumulator, not a ten-million-element list.
RSS remained roughly flat; a major memory saving is not claimed. The report
explains profiling overhead, sampling limitations and why the supplied test's
strict memory-increase assertion is unreliable. All numeric outputs are tested.

## Reproduce

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
python -m pip install -r requirements.txt
python reproduce.py
python benchmark.py
```

The scripts generate `results/before/` and `results/after/` with raw cProfile,
line_profiler, memory_profiler, unittest and coverage logs plus HTML and JSON
coverage. `results/benchmark.json` retains all timing samples and sampled RSS.
The complete submission ZIP includes the recorded results and native terminal
snapshots. Snapshots display saved output from actual completed runs, with the
project name visible; they are not additional benchmark runs.

For a single tool, change into `before` or `after` and run:

```bash
python -m cProfile -s time profiler.py
python profiler_lineprofiler.py
python -m memory_profiler profiler_memoryprofiler.py
python -m unittest -v test_profiler
python -m coverage run --branch --source=profiler -m unittest discover -v
python -m coverage report -m
python -m coverage html
```

The original coverage gaps were main's calls and its script entry point. The
optimized tests exercise those paths and formula edge cases. Coverage gain is
attributed to expanded tests as well as changed source, not optimization alone.
The memory wrapper measures at function-call boundaries to avoid RSS sampling
on every iteration of the full ten-million-term loop.
