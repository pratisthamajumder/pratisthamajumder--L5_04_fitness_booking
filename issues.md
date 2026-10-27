# Issues Found in `gym_system.py`

Line numbers refer to the **original** starter file. Issues are ordered by severity: high and medium first.

## Results summary

| Tool   | Before                                | After               |
|--------|---------------------------------------|---------------------|
| Bandit | 1 issue (High severity, High confidence) | No issues identified |
| Flake8 | 10 issues                             | 0 issues            |
| Pylint | 6.60/10                               | 10.00/10            |

## Issues flagged by the tools

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 1 | Shell command injection | Security (High) | Bandit B605 (CWE-78) | 36 | `os.system("rm -f " + prefix + "*.json")` builds a shell command from a string. A malicious `prefix` such as `"x; del *"` would run extra commands. It also fails on Windows (`'rm' is not recognized`). | Removed the shell entirely: `glob.glob(glob.escape(prefix) + "*.json")` finds the files and `os.remove()` deletes them. This is safe and works on every OS. |
| 2 | Mutable default argument | Bug (Medium) | Pylint W0102 | 8 | `attendance_log=[]` is created once and shared by every call, so log entries leak between unrelated bookings. | Default to `None` and create a new list inside the function. |
| 3 | Bare `except` | Bug (Medium) | Flake8 E722, Pylint W0702 | 21 | `except:` catches every error, including typos and `KeyboardInterrupt`, and hides them behind "Nothing to cancel". | Catch only the expected errors: `except (KeyError, ValueError):` (unknown class, member not booked). |
| 4 | File opened without `with` or encoding | Bug (Medium) | Pylint R1732, W1514 | 32 | `open()` is never closed, so the JSON may not be fully written. With no encoding, the output depends on the OS default. | `with open(file, "w", encoding="utf-8") as f:` |
| 5 | Missing blank lines | Style (Low) | Flake8 E302 / E305 | 8, 18, 24, 27, 31, 35, 38, 42, 58 | PEP 8 requires 2 blank lines around top-level functions. | Added 2 blank lines between all top-level definitions. |
| 6 | Function name not snake_case | Style (Low) | Pylint C0103 | 27 | `addMembers` breaks the Python naming convention. | Renamed to `add_members` and updated the callers. |
| 7 | Old-style `%` string formatting | Style (Low) | Pylint C0209 | 15 | `"%s -> %s" % (...)` is harder to read. | Replaced with an f-string: `f"{member_id} -> {class_name}"`. |
| 8 | Iterating dict keys then indexing | Style (Low) | Pylint C0206 | 39–40 | `for c in rosters: ... rosters[c]` does a needless lookup. | `for class_name, members in rosters.items():` |
| 9 | Missing docstrings | Style (Low) | Pylint C0114 / C0116 | 1, 8, 18, 24, 27, 31, 35, 38, 42 | There are no module or function docstrings. | Added a module docstring and a docstring for every function. |
| 10 | Code runs on import | Practice (Low) | — | 58 | `main()` runs as soon as the file is imported. | Wrapped it in `if __name__ == "__main__":`. |

## Logic bugs found by running the program (not flagged by any tool)

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 11 | Off-by-one capacity check | Bug (High) | 11 | `len(roster) > capacity` allows one extra booking. Yoga (capacity 3) got 4 members and HIIT (capacity 2) got 3. | Changed `>` to `>=`. |
| 12 | Negative capacity accepted | Bug (Medium) | 24–25, 49 | `set_capacity("Spin", -2)` was accepted, so Spin printed "Class full" 3 times with nobody in it. | `set_capacity` raises `ValueError` for negative seats, and `main` catches it and reports it. |
| 13 | Unknown class accepted | Bug (Medium) | 9–11, 48 | Pilates has no capacity entry, but M5 was still booked into it. | `book_class` rejects any class that isn't in `class_capacity`. |
| 14 | Crash on invalid input | Bug (Medium) | 52–53 | `int(n)` raises `ValueError` for input like `abc`, and negative numbers were accepted. | Added `read_guest_count()`, which falls back to the default for empty, non-numeric or negative input. |
| 15 | Inconsistent member ID type | Bug (Low) | 47 | Member `55` is an `int` while every other ID is a string. | Changed it to `"M6"`. |
| 16 | Duplicate booking | Bug (Low) | 14 | The same member could be booked twice into one class. | `book_class` rejects a member who is already on the roster. |
