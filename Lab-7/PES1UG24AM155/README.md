# Lab 7 – Fuzz Testing: Vending Machine

## Files
- `vending_machine.py`: robust implementation of the three vending-machine functions.
- `test_vending_machine.py`: Hypothesis property-based/fuzz tests.

## Setup (Windows PowerShell)
Open a terminal in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install hypothesis pytest
```

If PowerShell blocks activation, run pytest using:
```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Run the tests
```powershell
python -m pytest -v
```

## Run the interactive program
```powershell
python vending_machine.py
```

## Expected behavior
- `parse_coins("5,10,25")` returns `[5, 10, 25]`; invalid input returns `[]`.
- `slot_position("B7")` returns `(1, 6)`; invalid input returns `None`.
- `change_due("200/150")` returns `"10 five-coins"`; invalid or insufficient payment returns `None`.

## Lab deliverables
1. Completed `vending_machine.py`.
2. Completed `test_vending_machine.py` with Hypothesis tests.
3. Test execution evidence: screenshot of `python -m pytest -v` showing all tests passing.
4. Short observation/report listing bugs found in the original starter code and how they were handled.
5. Conclusion explaining that Hypothesis generates many inputs automatically and helps expose unexpected-input failures.

## 4. Observations

The original vending machine program was tested using the Hypothesis library to identify potential errors caused by unexpected inputs.

The following bugs were identified in the original implementation:

| Function | Bug Identified | Solution Implemented |
|---|---|---|
| `parse_coins()` | Invalid coin values (e.g., `"5,abc,10"`) cause a `ValueError`. | Added input validation and exception handling. Invalid inputs return an empty list. |
| `slot_position()` | Empty strings may cause an `IndexError`, while invalid column values cause a `ValueError`. | Added input validation and checks for valid slot codes. Invalid inputs return `None`. |
| `change_due()` | Incorrect payment formats (e.g., `"200"` or `"abc/100"`) cause exceptions. | Added format validation and exception handling. Invalid inputs return `None`. |

### Additional Observations

- Hypothesis automatically generated different input values, including random strings and `None`.
- Both valid and invalid inputs were tested.
- Input validation and exception handling improved the robustness of the program.
- All six automated test cases passed successfully during the final execution.

## 5. Conclusion

In this lab, fuzz testing was implemented using the Python Hypothesis library and pytest framework.

Hypothesis automatically generates a large variety of inputs, including valid, invalid, empty, and unexpected values. This helps identify potential errors and unexpected-input failures that may not be detected through ordinary manual testing.

After identifying potential issues in the original vending machine implementation, input validation and exception handling were added to make the functions more robust.

The final implementation successfully passed all six automated test cases.

**Result:** Fuzz testing was successfully implemented and executed on the vending machine program using Hypothesis and pytest.