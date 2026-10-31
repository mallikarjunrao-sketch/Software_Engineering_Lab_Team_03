# Lab 5: Issues Found in electricity_bill.py

Tools run: Pylint (5.44/10 before), Bandit (1 High, 1 Medium, 2 Low), Flake8 (4 issues).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| OS command injection via `os.system` (B605) | Security (High) | 61-63 | `syncMeter` builds a shell command by joining `meterIp` into a string, so input like `1.2.3.4; rm -rf ~` would run extra commands | Removed `os.system` and `curl`. Validate the value with `ipaddress.ip_address()` and fetch with `http.client` (no shell involved) |
| Unsafe XML parsing with `ET.fromstring` (B314) | Security (Medium) | 18 | The standard XML parser is open to XML attacks (entity expansion) if the text is ever untrusted | Switched to `defusedxml.ElementTree` |
| Unsafe XML import (B405) | Security (Low) | 3 | Importing `xml.etree.ElementTree` is flagged for the same reason as B314 | Replaced the import with `from defusedxml import ElementTree as ET` |
| Hardcoded password (B105) | Security (Low) | 13 | `CLERK_PASSWORD = "bill-desk-demo"` is a secret stored in source code, and it is never used | Deleted the unused constant (a real secret would come from an environment variable) |
| Mutable default argument (W0102) | Bug | 42 | `extras={}` is created once and shared by every call, so changes can leak between calls | Default is now `None`, with `extras = extras or {}` inside the function |
| Unused argument `currency` (W0613) | Code quality | 50 | `averageBill(currency)` never uses its parameter | Removed the parameter and updated the call in `main()` |
| `open()` without encoding (W1514) | Code quality | 57 | File encoding depends on the operating system, so output can differ between machines | Added `encoding="utf-8"` |
| Names not in snake_case (C0103) | Style | 17-67 | `readMeters`, `calculateUnits`, `energyCharge`, `generateBill`, `averageBill`, `saveBills`, `syncMeter`, `slabUnits`, `meterId`, `taxRate`, `fileName`, `meterIp`, `xmlText` | Renamed everything to snake_case |
| Missing docstrings (C0114, C0116) | Style | 1, 17-66 | The module and all 8 functions have no docstrings | Added a short docstring to the module and each function |
| Expected 2 blank lines (E302) | Style (Flake8) | 22 | Only one blank line before `calculateUnits` | Added a second blank line |
| Whitespace before ':' (E203) | Style (Flake8) | 44 | `"meter" : meterId` | Changed to `"meter": meterId` |
| Line too long, 86 > 79 (E501) | Style (Flake8) | 72 | The `print` call in `main()` is too wide | Split the call across two lines |
| Missing whitespace around operator (E225) | Style (Flake8) | 76 | `total=sum(...)` | Changed to `total = sum(...)` |

Line numbers refer to the original file.
