# Lab 5: Static Code Analysis — Reflection (`hotel_booking_system.py`)

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

- **Easiest Issues to Fix:**
  The easiest issues to fix were the **PEP 8 formatting and simple cleanup warnings** reported by **Flake8** and **Pylint**:
  - Removing the unused import `import math` (`F401` / `W0611`) on line 6 and the unused local variable `cleaning_deposit = 25.0` (`F841` / `W0612`) on line 31.
  - Replacing `== None` with `is None` (`E711` / `C0121`) on line 32, converting `%` formatting to an f-string (`C0209`) on line 19, and adding a trailing newline at the end of the file (`W292` / `C0304`).
  - **Why:** These fixes were purely local and mechanical—the tools pinpointed the exact line and column numbers, and applying them required no changes to function signatures or program control flow.

- **Hardest Issues to Fix:**
  The hardest issues to fix were the **logical state bug (`W0102: dangerous-default-value`)** and the **dynamic expression evaluation vulnerability (`B307` / `W0123: eval-used`)**:
  - **Mutable Default Argument (`booking_log=[]` in `bookRoom`):** Because Python evaluates default arguments only once at function definition time, every call to `bookRoom()` that omitted `booking_log` mutated the exact same underlying list across unrelated bookings. Fixing it required changing the signature default to `booking_log=None` and initializing a new list inside the function body (`if booking_log is None: booking_log = []`).
  - **Replacing `eval(rate_expr)` in `compute_seasonal_rate()`:** Originally, `compute_seasonal_rate("101", "base_price * 1.25")` relied on `eval()` dynamically accessing the local variable `base_price` inside its string expression (which also caused Pylint and Flake8 to think `base_price` was unused). Refactoring this safely required redesigning the calculation to use explicit floating-point multiplication (`base_price * float(rate_multiplier)`) while maintaining compatibility with callers passing either a numeric multiplier (`1.25`) or a string multiplier expression.

---

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, there were two notable examples of **context-dependent or apparent false positives** across the tools:

1. **"Unused variable `base_price`" (`W0612` in Pylint / `F841` in Flake8) on Line 41:**
   In the original `compute_seasonal_rate(room_num, rate_expr)` function:
   ```python
   base_price = room_inventory[room_num]["price"]
   final_price = eval(rate_expr)
   ```
   Both Pylint and Flake8 flagged `base_price` as an unused local variable because static AST analysis cannot inspect runtime strings passed to `eval("base_price * 1.25")`. In reality, removing `base_price` while keeping `eval(rate_expr)` would have crashed the program with a `NameError` at runtime! Once `eval()` was replaced with explicit arithmetic (`base_price * float(rate_multiplier)`), `base_price` was directly referenced in the AST and the warning disappeared naturally.

2. **Cryptographic PRNG Warning (`B311` in Bandit) on Line 51:**
   Bandit flagged `random.randint(1000, 9999)` in `generate_booking_ref()` because `random` is not cryptographically secure. If a 4-digit booking reference is only used for human-friendly display rather than as a security token, flagging `random.randint` can be considered overly strict. However, switching to `secrets.randbelow(9000) + 1000` resolved the warning and prevented predictable booking ID enumeration at zero extra complexity.

---

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate **Flake8**, **Pylint**, and **Bandit** across three layers of the software development lifecycle:

1. **IDE / Editor Integration (Real-Time Feedback):**
   Configure the code editor (e.g., VS Code) to run **Flake8** and **Pylint** on save so developers immediately see PEP 8 formatting violations, unused variables, and missing docstrings while writing code.
2. **Local Git `pre-commit` Hooks (Pre-Commit Gate):**
   Use the `pre-commit` framework to automatically run `flake8` and `bandit` on staged Python files before every `git commit`. This blocks accidental commits containing hardcoded secrets (`B105`), shell injections (`B605`), or syntax/style errors before they ever enter version control.
3. **CI/CD Pipeline Gatekeeper (GitHub Actions / GitLab CI):**
   Add an automated static analysis stage in the Continuous Integration pipeline on every pull request:
   - Fail the build if **Bandit** reports any Medium or High severity vulnerabilities (`bandit -r . -ll`).
   - Fail the build if **Flake8** reports any PEP 8 / syntax violations.
   - Enforce a minimum **Pylint** quality threshold (`pylint --fail-under=9.5 hotel_booking_system.py`) before code can be merged into `main`.

---

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Applying the fixes raised the **Pylint score from 5.32/10 to 10.00/10**, reduced **Bandit security findings from 6 to 0**, and reduced **Flake8 violations from 7 to 0**, yielding major improvements in four areas:

- **Security:**
  - Eliminated remote code execution (`eval()` -> explicit float arithmetic) and OS command injection (`os.system()` -> `print()`).
  - Upgraded guest ID hashing from broken MD5 (`B324`) to SHA-256 (`hashlib.sha256`).
  - Replaced predictable random booking references (`random.randint`) with cryptographically secure generation (`secrets.randbelow`).
  - Removed the hardcoded admin token (`B105`) in favor of `os.getenv("HOTEL_SECRET_KEY")`.
- **Correctness & Bug Prevention:**
  - Fixed the mutable default argument `booking_log=[]` (`W0102`), preventing booking logs from leaking across independent calls to `book_room()`.
- **Robustness & Resource Safety:**
  - Replaced the bare `except: pass` in `cancel_booking()` with `except KeyError: return False`, ensuring real runtime exceptions (`KeyboardInterrupt`, `TypeError`, etc.) are not silently swallowed.
  - Replaced manual `open()` / `close()` in `export_room_ledger()` with a `with open(..., encoding="utf-8")` context manager so the file handle is guaranteed to close even if an I/O error occurs.
  - Fixed stdout ordering: previously `os.system("echo ...")` flushed before Python's buffered `print()` calls, causing the ledger export message to appear at the top of the output instead of in sequence.
- **Readability & Maintainability:**
  - Standardized function naming to `snake_case` (`book_room`), simplified boolean returns (`return not room_inventory[room_num]["is_booked"]`), removed dead code (`math`, `cleaning_deposit`), added clear docstrings to all functions, and added an `if __name__ == "__main__":` guard so the module can be safely imported without side effects.
