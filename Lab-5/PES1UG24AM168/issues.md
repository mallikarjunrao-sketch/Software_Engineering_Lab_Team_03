# Lab 5: Static Code Analysis — Identified Issues (`hotel_booking_system.py`)

## Summary of Static Analysis Results

| Tool | Before Fixes | After Fixes |
|------|--------------|-------------|
| **Bandit** | 6 issues (2 High, 1 Medium, 3 Low) | **0 issues** (`No issues identified`) |
| **Pylint** | **5.32 / 10** (22 warnings/conventions/refactorings) | **10.00 / 10** (0 issues) |
| **Flake8** | 7 PEP 8 & Pyflakes violations | **0 violations** |

---

## Documented Issues Table (Prioritized by Severity)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak cryptographic hash (`B324`) | Security (High - Bandit) | 47 | `hashlib.md5(guest_id.encode()).hexdigest()` uses the broken MD5 algorithm (`CWE-327`), which is vulnerable to collision attacks. | Replaced `hashlib.md5(...)` with `hashlib.sha256(guest_id.encode()).hexdigest()`. |
| Shell command injection (`B605`) | Security (High - Bandit) | 58 | `os.system("echo Hotel ledger exported to: " + filename)` invokes a system shell with unsanitized string concatenation (`CWE-78`), enabling command injection if `filename` is attacker-controlled. | Removed `os.system(...)` and replaced it with Python's native `print(f"Hotel ledger exported to: {filename}")`. |
| Arbitrary code execution via `eval()` (`B307`, `W0123`) | Security / Bug (Medium - Bandit & Pylint) | 42 | `eval(rate_expr)` evaluates arbitrary Python expressions (`CWE-78`), allowing remote code execution if user input reaches `rate_expr`. Also caused `base_price` on line 41 to be flagged as unused (`W0612`, `F841`). | Removed `eval()` and refactored `compute_seasonal_rate()` to compute `base_price * float(rate_multiplier)` directly. |
| Mutable default argument (`W0102`) | Bug (Medium - Pylint) | 15 | `def bookRoom(room_num, guest_name, booking_log=[]):` uses a mutable list `[]` as a default argument, causing the same list instance to be shared across all calls that omit `booking_log`. | Changed default parameter to `booking_log=None` and initialized a fresh list (`if booking_log is None: booking_log = []`) inside `book_room()`. |
| Bare `except:` with `pass` (`B110`, `W0702`, `E722`) | Bug / Security (Low/Medium - Bandit, Pylint, Flake8) | 26–27 | `except: pass` in `cancel_booking()` catches all exceptions (including `SystemExit` and `KeyboardInterrupt`) and silently suppresses errors (`CWE-703`). | Replaced bare `except: pass` with `except KeyError: return False` and returned `True` when cancellation succeeds. |
| Insecure PRNG (`B311`) | Security (Low - Bandit) | 51 | `random.randint(1000, 9999)` uses Python's standard pseudo-random generator (`CWE-330`), which is predictable and unsuitable for generating unguessable booking references. | Replaced `random.randint(1000, 9999)` with `secrets.randbelow(9000) + 1000` using the cryptographically strong `secrets` module. |
| Hardcoded secret token (`B105`) | Security (Low - Bandit) | 62 | `hotel_secret_key = "HOTEL_ADMIN_RESERVATION_TOKEN_2026"` hardcodes a sensitive administrative token directly in source code (`CWE-259`). | Loaded the secret from environment variables via `os.getenv("HOTEL_SECRET_KEY")` and avoided printing the raw secret to stdout. |
| Resource leak & missing encoding (`R1732`, `W1514`) | Bug / Quality (Medium - Pylint) | 55–57 | `f = open(filename, "w")` opens a file without a `with` context manager (risking unclosed file handles on exception) and omits explicit `encoding`. | Refactored to `with open(filename, "w", encoding="utf-8") as ledger_file:`. |
| Singleton comparison to `None` (`C0121`, `E711`) | Style / Bug (Low - Pylint, Flake8) | 32 | `room_inventory.get(room_num) == None` uses equality `==` instead of identity `is` when comparing to the singleton `None`. | Changed comparison to `if room_inventory.get(room_num) is None:`. |
| Unused import & unused variables (`W0611`, `W0612`, `F401`, `F841`) | Code Quality (Low - Pylint, Flake8) | 6, 31, 41 | `import math` (line 6) and `cleaning_deposit = 25.0` (line 31) are never used; `base_price` (line 41) was only referenced dynamically inside `eval()`. | Removed unused `import math` and `cleaning_deposit`, and used `base_price` directly in arithmetic calculation. |
| Naming convention, f-strings, and control flow (`C0103`, `C0209`, `R1703`, `R1705`) | Style / Refactor (Low - Pylint) | 15, 19, 34–37 | `bookRoom` violates `snake_case` naming (`C0103`); `%` string formatting used instead of f-strings (`C0209`); redundant `if/else` returning boolean literals (`R1703`, `R1705`). | Renamed `bookRoom` to `book_room`, replaced `%` formatting with f-strings, and simplified lines 34–37 to `return not room_inventory[room_num]["is_booked"]`. |
| Line length, missing docstrings & final newline (`E501`, `W292`, `C0116`, `C0304`) | Style (Low - Pylint, Flake8) | 15–73 | Line 19 exceeded 79 characters (80 chars, `E501`), functions lacked docstrings (`C0116`), `main()` lacked an `if __name__ == "__main__":` guard, and file lacked a trailing newline (`W292`, `C0304`). | Wrapped lines within 79 characters, added docstrings to all functions, guarded `main()`, and added a final newline. |
