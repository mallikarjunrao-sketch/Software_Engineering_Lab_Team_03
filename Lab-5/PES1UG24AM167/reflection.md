# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The style issues were the easiest. Adding the final newline, changing `== None` to `is None`, renaming `addGrade` to `add_grade`, splitting long lines and adding docstrings took a few seconds each. The tool tells you the exact line and what it wants, and none of these change how the program behaves.

The hardest was `eval()` in `compute_weighted_gpa`. I could not just delete it, because the function depended on it to calculate the GPA. I had to work out what the expression was meant to do (divide the average by 20) and rewrite the function so it takes a number instead of a string of code, while making sure the GPA printed was still 4.35. The unused `grace_marks` variable was also harder than it looked. Flake8 only says the variable is unused, and deleting it would have silenced the warning. Reading the function showed that the grace marks were supposed to be added to the average before the pass check, so the right fix was to apply them, not remove them.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Bandit's B105 warning on `portal_token = "ADMIN_GRADE_PORTAL_TOKEN_2026"` is close to one. Bandit flags it only because the variable name contains "token" and it is assigned a string. It cannot tell whether the value is a real credential or a placeholder. Here it was a fair warning, since the program printed the token to the screen. But the same rule would also flag something harmless like `token_type = "bearer"`.

Bandit's B311 warning on `random` is another borderline case. It is only a real problem when the number is used for security. A registration PIN counts, so I fixed it, but `random` used to shuffle a list or pick sample data would raise the same warning without any risk.

The tools also missed problems. Marks above 100 were accepted, attendance (a percentage) could go above 100, and a student with no marks would cause a division by zero. None of the three tools reported these. I found them by running the program and reading the logic.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run them at two points. First, locally before each commit, using a pre-commit hook that runs Flake8 and Bandit, so style and security problems are caught before the code leaves my machine. Second, in a CI pipeline such as GitHub Actions on every push and pull request, running all three tools and failing the build if Bandit finds a High or Medium issue or if the Pylint score drops below a set limit like 9.5. The CI step matters most in a team, because it applies the same rules to everyone and nobody can skip it. I would also add a `.pylintrc` or `setup.cfg` to the repo so the settings are shared, and turn on the tools' editor plugins so warnings show up while writing code.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The Pylint score went from 5.51 to 10.00, Bandit went from six issues (two High) to none, and Flake8 went from eight issues to none.

On security, the program no longer runs shell commands built from a filename, no longer executes code passed in as a string, and no longer keeps a token in the source or prints it.

On robustness, `add_grade` and `record_attendance` now return `True` or `False`, so a caller can tell when something fails instead of errors being swallowed. Bad input like a mark of 150 or a negative attendance value is rejected, and an empty marks list no longer crashes the program. The mutable default list is gone, so log entries do not leak between calls.

On readability, every function has a docstring, names follow PEP 8 and the pass check is one clear line. The grade sheet is now real JSON, which another program can read back. Importing the module no longer runs the demo, so the functions can be reused or tested on their own.
