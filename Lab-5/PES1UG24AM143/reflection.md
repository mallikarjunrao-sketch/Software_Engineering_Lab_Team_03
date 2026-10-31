# Reflection: Lab 5 Static Code Analysis

Note: edit these to match the exact questions in your handout/Teams post if they differ.

**1. Which issues were the easiest and hardest to fix?**
Easiest: Flake8 style issues and Pylint renames/docstrings, which are mechanical. Hardest: replacing pickle, because the fix changes the storage format (`json`), so I had to check that playlists (lists of strings) still round-trip correctly. The mutable default argument was also subtle, since the program still "worked" in the demo.

**2. Did the tools report any false positives?**
B311 (`random`) is arguably a false positive here, because picking a random song is not security-sensitive. I still switched to `secrets.choice` to clear the report, but in a real project `# nosec` with a justification would also be reasonable. B403 simply flags importing pickle, so it disappeared along with B301.

**3. How could static analysis be integrated into a real workflow?**
Run Flake8, Pylint and Bandit as pre-commit hooks and in a CI pipeline (for example GitHub Actions) so pull requests fail on new high/medium findings, with a Pylint score threshold such as 9.5.

**4. What tangible improvements did you see?**
Pylint went from 4.57/10 to 10.00/10, Bandit from 4 findings (2 Medium) to 0, and Flake8 from 7 to 0. The code is safer (no SQL injection or unsafe deserialization), more robust (no shared mutable state or swallowed exceptions), and more readable (PEP 8 names, docstrings, importable without side effects).
