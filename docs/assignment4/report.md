# Report for assignment 4

This is a template for your report. You are free to modify it as needed.
It is not required to use markdown for your report either, but the report
has to be delivered in a standard, cross-platform format.

## Project

Name: Rich

URL: https://github.com/DD2480-2026-Group-8/rich-Assignment-4

Rich is a Python library for rich text and beautiful formatting in the terminal (tables, progress bars, markdown, syntax highlighting, and more). We use only the Python code in the `rich/` package.

## Onboarding experience

Did you choose a new project or continue on the previous one?
We continued with the same project (Rich) from Assignment 3, so we already had familiarity with the codebase and tooling.

### Setup steps

Since we already had experience from Assignment 3, setup was straightforward:

1. **Clone the repository**

   ```
   git clone git@github.com:DD2480-2026-Group-8/rich-Assignment-4.git
   cd rich-Assignment-4
   ```

2. **Install Poetry**
   Rich uses [Poetry](https://python-poetry.org/) for packaging and dependency management, as documented in `CONTRIBUTING.md`. We installed it with `pip3 install poetry`. Poetry version 2.3.2 was installed; Python 3.12.1 was already available.

3. **Create virtual environment and install dependencies**

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   poetry install
   ```

   Poetry installed 25 packages (pytest, black, mypy, pygments, markdown-it-py, etc.) and the Rich project itself in editable mode. No errors or manual intervention required.

4. **Run the test suite**

   ```
   TERM=unknown pytest tests/ -v --tb=short
   ```

   Result: **952 passed, 25 skipped** in 5.5 seconds. All 25 skips are platform-specific (Windows-only tests) or optional-dependency tests. No failures.

5. **Run tests with coverage**
   ```
   pytest tests/ --cov=rich --cov-report=term-missing -q
   ```
   Result: **95% overall coverage**. The file relevant to our issue (`rich/progress.py`) has 92% coverage.

### Quality of onboarding documentation

The project's `CONTRIBUTING.md` provides clear instructions: install Poetry, create a fork, run `poetry install`, then use `make test` / `make typecheck` / `make format-check`. The `Makefile` wraps common commands. The README is aimed at end users (install with `pip`, usage examples) and does not describe developer setup, but `CONTRIBUTING.md` fills that gap well.

Compared to Assignment 3, setup was faster because we already knew the project structure and tooling. The only new step was installing Poetry (which was not on the system), which took under a minute.

### Existing CI

The project already has a GitHub Actions workflow (`.github/workflows/pythonpackage.yml`) that runs on pull requests. But added also so it is triggered on push to the master branch. And also had to manually turn it on for the repository.

## Effort spent

For each team member, time spent (in hours) per activity:

| Activity                        | Filip | Anna | Jingze | Louisa | Erik | **Total** |
| ------------------------------- | ----- | ---- | ------ | ------ | ---- | --------- |
| 1. Plenary discussions/meetings |       |      |        |        |      |           |
| 2. Discussions within subgroup  |       |      |        |        |      |           |
| 3. Reading documentation        |       |      |        |        |      |           |
| 4. Configuration and setup      |       |      |        |        |      |           |
| 5. Analyzing code/output        |       |      |        |        |      |           |
| 6. Writing documentation        |       |      |        |        |      |           |
| 7. Writing code                 |       |      |        |        |      |           |
| 8. Running code                 |       |      |        |        |      |           |
| **Per-person total**            |       |      |        |        |      |           |

For setting up tools and libraries (step 4), enumerate all dependencies
you took care of and where you spent your time, if that time exceeds
30 minutes:

No dependency took more than 30 minutes. Poetry and all 25 project packages via `poetry install` were the only installs needed. That part of the set up took less than 30 minutes. However the overall approach, creating a coverage branch for testing, did require some thought process before starting with the issue. Detailed documentation can be seen in setup experience section.

## Overview of issue(s) and work done.

Title: [BUG] Progress with multiple tasks and transient will delete written lines on stop() and start()

URL: https://github.com/Textualize/rich/issues/3121

Summary in one or two sentences: When using `Progress` with `transient=True` and multiple tasks, calling `stop()` and then `start()` deletes previously printed lines from the terminal. The maintainer clarified that `stop()` was never designed for pause/restart; the solution is to add a new `pause()` and `resume()`, making the issue a feature request.

Scope (functionality and code affected). `rich/live.py` (Live), `rich/live_render.py` (LiveRender), `rich/progress.py` (Progress). New methods `pause()` and `resume()` on Live and Progress; `LiveRender._shape` reset logic.

## Requirements for the new feature or requirements affected by functionality being refactored

Optional (point 3): trace tests to requirements.
| ID | Title | Description |
| ----- | ---------------------------------- | ------------------------------------------------------------------------ |
| REQ-1 | Transient progress clears on pause | When paused, progress bar lines are erased from the terminal. |
| REQ-2 | Resume preserves prior output | Lines printed before `pause()` must not be overwritten after `resume()`. |
| REQ-3 | Restart renders correctly | After `resume()`, progress bars render at the correct position. |
| REQ-4 | Safe to call pause/resume twice | Calling `pause()` when already paused, or `resume()` when already showing, must do nothing and not crash. |
| REQ-5 | Non-transient unaffected | Behavior for `transient=False` unchanged. |

## Code changes

### Patch

(copy your changes or the add git command to show them)

git diff ...

Optional (point 4): the patch is clean.

Optional (point 5): considered for acceptance (passes all automated checks).

## Test results

Overall results with link to a copy or excerpt of the logs (before/after
refactoring).

## UML class diagram and its description

### Key changes/classes affected

![UML diagram](uml.png)

Optional (point 1): Architectural overview.

Optional (point 2): relation to design pattern(s).

## Overall experience

What are your main take-aways from this project? What did you learn?

How did you grow as a team, using the Essence standard to evaluate yourself?

Optional (point 6): How would you put your work in context with best software engineering practice?

Optional (point 7): Is there something special you want to mention here?
