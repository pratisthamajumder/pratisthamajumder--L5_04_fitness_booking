# Reflection: Lab 5 Static Code Analysis

**Name:** Pratistha Majumder
**Program:** `gym_system.py` (Fitness Club Class Booking Ledger)

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the style issues from Flake8 and Pylint: adding blank lines (E302/E305), renaming `addMembers` to `add_members`, switching to an f-string, and adding docstrings. They were mechanical, the tool told me the exact line, and they could not change how the program behaved.

The hardest was the Bandit B605 finding. Recognising the problem was easy, because `os.system` with a string-built command is a classic injection risk. Replacing it took more thought, because I had to keep the same behaviour (delete `old_*.json` files) without a shell. I used `glob.glob(glob.escape(prefix) + "*.json")` with `os.remove()`. As a bonus, this also fixed the `'rm' is not recognized` error I saw when running the program on Windows.

The logic bugs were also hard, because no tool reported them. I only found them by reading the output carefully. Yoga showed 4 members although its capacity is 3, Pilates accepted a booking although it isn't a real class, and Spin was "full" with nobody in it. Tracing these back to the off-by-one `>` check and the missing input validation took real debugging.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

There were no true false positives, since every finding pointed at something real. Some findings were low priority rather than wrong. For example, the missing-docstring warnings (C0114/C0116) make up a large share of the Pylint penalty. They improve readability, but they are not bugs. I added the docstrings anyway, because they make the code easier for others to understand.

The opposite problem, **false negatives**, mattered much more. All three tools passed code that was still clearly wrong: the off-by-one capacity check, negative capacity, unknown classes, and a crash on non-numeric input. After my tool-only fixes, Pylint gave 10.00/10, yet the program still overbooked classes. A perfect score does not mean correct code.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **While coding:** enable Pylint and Flake8 in the editor (for example, the VS Code Python extension) so issues show up immediately instead of after the fact.
- **Before each commit:** run the tools automatically with a pre-commit hook, so badly formatted or insecure code never enters the repository.
- **In CI:** run Pylint, Flake8 and Bandit in a GitHub Actions workflow on every push and pull request. Fail the build on any Bandit high or medium finding, any Flake8 error, or a Pylint score below an agreed threshold (for example, 9.5).
- **Alongside tests:** static analysis does not replace unit tests. The logic bugs I found here would be caught by simple tests, such as "a class with capacity 3 never holds 4 members".

## 4. What tangible improvements did you observe in code quality, readability, or robustness after applying the fixes?

- **Security:** the shell-injection risk is gone, and Bandit went from 1 high-severity issue to none.
- **Robustness:** the export file is now always closed properly, specific exceptions replace the bare `except`, invalid input no longer crashes the program, and the shared mutable default list can no longer leak data between calls.
- **Correctness:** every class now respects its capacity (Yoga 3/3, HIIT 2/2), unknown classes and negative capacities are rejected, and member IDs are consistent strings.
- **Portability:** the program now runs on Windows as well as Linux and macOS.
- **Readability:** with consistent spacing, snake_case names, f-strings and docstrings, the code is easier to read. Flake8 went from 10 issues to 0, and Pylint went from 6.60/10 to 10.00/10.
