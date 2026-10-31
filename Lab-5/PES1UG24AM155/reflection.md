# Lab 5 Reflection

> The handout PDF does not list the four reflection questions. These are the usual ones for this lab. Replace the headings with the exact wording from your handout if it differs.

## 1. Which issues were the easiest and the hardest to fix?

The easiest were the style issues from Flake8 (blank lines, spacing, line length) and the Pylint naming warnings, because the tool tells you exactly what to change. The hardest was the `os.system` command injection. Deleting the line would have broken the function, so I had to redesign it: validate the IP address with `ipaddress` and make the request with `http.client`, which never touches a shell. The mutable default argument was also tricky, because it works fine in a short demo and only fails when the function is called many times.

## 2. Did the tools report any false positives?

Mostly no, but some warnings need judgement. Bandit flagged the XML parsing as Medium even though the XML in this program is hardcoded and not user input. It is still worth fixing, because the code could easily be reused with real input later. The hardcoded password warning (B105) was technically right about the pattern, but the constant was never used, so the right fix was to delete it. I did not hide anything with `# nosec` or `# pylint: disable`.

## 3. How would you integrate static analysis into your workflow?

I would run Flake8 and Pylint in an editor plugin while writing code, add a pre-commit hook so style and security checks run before every commit, and run all three tools in a CI pipeline (for example GitHub Actions) so a pull request cannot be merged if Bandit finds a High issue or the Pylint score drops below a set threshold.

## 4. What tangible improvements did you see in code quality, readability and security?

Pylint went from 5.44/10 to 10.00/10 and Flake8 and Bandit now report no issues. The code is easier to read thanks to consistent snake_case names and docstrings. It is also safer: no shell command injection, no unsafe XML parsing, no hardcoded secret, and no shared mutable default. The program prints exactly the same output and writes the same `bills.json` as before.
