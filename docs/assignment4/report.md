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

1. **Clone the repository** (~1 min)

   ```
   git clone git@github.com:DD2480-2026-Group-8/rich-Assignment-4.git
   cd rich-Assignment-4
   ```

2. **Install Poetry** (~1 min)
   Rich uses [Poetry](https://python-poetry.org/) for packaging and dependency management, as documented in `CONTRIBUTING.md`. We installed it with `pip3 install poetry`. Poetry version 2.3.2 was installed; Python 3.12.1 was already available.

3. **Create virtual environment and install dependencies** (~1 min)

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   poetry install
   ```

   Poetry installed 25 packages (pytest, black, mypy, pygments, markdown-it-py, etc.) and the Rich project itself in editable mode. No errors or manual intervention required.

4. **Run the test suite** (~10 s)

   ```
   TERM=unknown pytest tests/ -v --tb=short
   ```

   Result: **952 passed, 25 skipped** in 5.5 seconds. All 25 skips are platform-specific (Windows-only tests) or optional-dependency tests. No failures.

5. **Run tests with coverage** (~10 s)
   ```
   pytest tests/ --cov=rich --cov-report=term-missing -q
   ```
   Result: **95% overall coverage**. The file relevant to our issue (`rich/progress.py`) has 92% coverage.

### Quality of onboarding documentation

The project's `CONTRIBUTING.md` provides clear instructions: install Poetry, create a fork, run `poetry install`, then use `make test` / `make typecheck` / `make format-check`. The `Makefile` wraps common commands. The README is aimed at end users (install with `pip`, usage examples) and does not describe developer setup, but `CONTRIBUTING.md` fills that gap well.

Compared to Assignment 3, setup was faster because we already knew the project structure and tooling. The only new step was installing Poetry (which was not on the system), which took under a minute.

### Existing CI

The project already has a GitHub Actions workflow (`.github/workflows/pythonpackage.yml`) that runs on pull requests. But added also so it is triggered on push to the master branch.

## Effort spent

For each team member, how much time was spent in

1. plenary discussions/meetings;

- Filip: Approx 3 hours understanding the project. Includes discussions with the group if we should continue with the same project, looking for suitable issue and discussing the approach.

- Anna:

- Jingze:

- Louisa:

- Erik:

2. discussions within parts of the group;

- Filip:

- Anna:

- Jingze:

- Louisa:

- Erik:

3. reading documentation;

- Filip: Spending approx 1 hour on the documentation. We had the same repo as Assignment 3, but was making sure that we could use similar approach.

- Anna:

- Jingze:

- Louisa:

- Erik:

4. configuration and setup;

- Filip:

- Anna:

- Jingze:

- Louisa:

- Erik:

5. analyzing code/output;

- Filip:

- Anna:

- Jingze:

- Louisa:

- Erik:

6. writing documentation;

- Filip:

- Anna:

- Jingze:

- Louisa:

- Erik:

7. writing code;

- Filip:

- Anna:

- Jingze:

- Louisa:

- Erik:

8. running code?

- Filip:

- Anna:

- Jingze:

- Louisa:

- Erik:

For setting up tools and libraries (step 4), enumerate all dependencies
you took care of and where you spent your time, if that time exceeds
30 minutes:

No dependency took more than 30 minutes. Poetry and all 25 project packages via `poetry install` were the only installs needed. That part of the set up took less than 30 minutes. However the overall approach, creating a coverage branch for testing, did require some thought process before starting with the issue. Detailed documentation can be seen in setup experience section.

## Overview of issue(s) and work done.

Title:

URL:

Summary in one or two sentences

Scope (functionality and code affected).

## Requirements for the new feature or requirements affected by functionality being refactored

Optional (point 3): trace tests to requirements.

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

Optional (point 1): Architectural overview.

Optional (point 2): relation to design pattern(s).

## Overall experience

What are your main take-aways from this project? What did you learn?

How did you grow as a team, using the Essence standard to evaluate yourself?

Optional (point 6): How would you put your work in context with best software engineering practice?

Optional (point 7): Is there something special you want to mention here?
