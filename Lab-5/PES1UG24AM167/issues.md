# Issues found in student_grade_system.py

Line numbers refer to the original file. Tool and code are in brackets.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605, High) | Security | 60 | `os.system("echo ... " + filename)` passes the filename to a shell. A filename like `x; rm -rf ~` would run as a command. | Removed the shell call and used `print()` to show the message. |
| Weak MD5 hash (Bandit B324, High) | Security | 49 | MD5 is broken and should not be used to hash identifiers. | Switched to `hashlib.sha256`. |
| Use of eval (Bandit B307 Medium, Pylint W0123) | Security | 44 | `eval(gpa_expr)` runs any Python expression passed in, so a caller could execute arbitrary code. | Replaced the string expression with a numeric `scale_divisor` argument (default 20.0). GPA is now `avg_score / scale_divisor`, so the output (4.35) is the same. |
| Hardcoded secret, printed to screen (Bandit B105) | Security | 64, 72 | The portal token is written in the source and then printed in plain text. | Read it from the `GRADE_PORTAL_TOKEN` environment variable and only print whether it is configured. |
| Insecure random PIN (Bandit B311) | Security | 53 | `random` is predictable, so it should not generate PINs. | Used `secrets.randbelow(9000) + 1000`, which still gives a 4-digit PIN. |
| Bare except with pass (Bandit B110, Pylint W0702, Flake8 E722) | Bug | 26-27 | Every error is swallowed, so a wrong student id fails silently. | Catch only `KeyError` and return `False`; return `True` on success. |
| Mutable default argument (Pylint W0102) | Bug | 15 | `grade_list=[]` is created once and shared across every call, so log entries pile up between calls. | Default changed to `None` and a new list is created inside the function. |
| Unused variable grace_marks (Pylint W0612, Flake8 F841) | Bug (logic) | 31 | Grace marks are defined but never applied, so the pass check ignores them. | Made it a parameter and applied it: `avg + grace_marks >= pass_threshold`. |
| Unused import json (Pylint W0611, Flake8 F401) | Quality | 6 | `json` was imported but the grade sheet was written with `str(dict)`, which is not a readable or reloadable format. | Export now uses `json.dump(..., indent=2)` to `grade_sheet.json`. |
| File opened without with / encoding (Pylint R1732, W1514) | Quality | 57-59 | The file is not closed if writing fails, and the encoding depends on the system. | Used `with open(filename, "w", encoding="utf-8")`. |
| Marks above 100 accepted | Bug (logic, not flagged by tools) | 16 | Only negative marks were rejected, so a mark of 150 would be stored. | Check `0 <= mark <= 100`. |
| Attendance can go past 100 | Bug (logic, not flagged by tools) | 25 | Attendance is a percentage, but days are added to it without any limit. | Reject negative values and cap the result at 100. |
| Division by zero on empty marks | Bug (logic, not flagged by tools) | 34, 43 | A student with no marks would crash both average calculations. | Return `False` / `0.0` when the marks list is empty. |
| Comparison to None (Pylint C0121, Flake8 E711) | Style | 32 | `== None` instead of `is None`. | Changed to `is None`. |
| Function name not snake_case (Pylint C0103) | Style | 15 | `addGrade` breaks PEP 8 naming. | Renamed to `add_grade`. |
| Unneeded if/else (Pylint R1703, R1705) | Style | 35-38 | `if ...: return True else: return False`. | Return the condition directly. |
| Old-style % formatting (Pylint C0209) | Style | 19 | String built with `%`. | Used an f-string. |
| Missing docstrings (Pylint C0116) | Style | 15, 23, 30, 41, 48, 52, 56, 63 | No function had a docstring. | Added a docstring to each function. |
| Lines too long (Flake8 E501) | Style | 19, 34 | Lines over 79 characters. | Shortened by splitting the expression and using a local `marks` variable. |
| Missing final newline (Pylint C0304, Flake8 W292) | Style | 75 | File did not end with a newline. | Added one. |
| main() runs on import | Quality | 75 | `main()` was called at module level, so importing the file ran the demo and wrote a file. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.51/10 | 10.00/10 |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | No issues |
| Flake8 | 8 issues | No issues |

The program still runs and gives the same results for passing status and GPA. The grade sheet is now saved as JSON.
