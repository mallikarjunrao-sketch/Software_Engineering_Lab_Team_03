# Lab 7 – Fuzz Testing (Parking Fee)

This folder follows the supplied Lab 7 README: test and fix the buggy parking-fee
application using Hypothesis. It is separate from Lab 6 (Code and Branch Coverage).

## Files
- `parking_fee.py` – validated application functions.
- `test_parking_fee.py` – Hypothesis fuzz tests, generated valid-input properties,
  and explicit invalid-input tests.

## Setup (Windows CMD)
Run these commands from this folder:

```cmd
python -m pip install hypothesis pytest
```

## Run the fuzz tests

```cmd
python -m pytest -v
```

Hypothesis generates many inputs for each `@given` test. The three
`*_no_crash` tests retain the intent of the supplied starter scaffold:
arbitrary text and `None` must either produce a valid result or be rejected
cleanly with `ValueError`; unexpected exceptions are test failures.

## Input assumptions used
The provided Lab 7 README refers to a handout but does not include it. The
implementation therefore makes the following explicit assumptions based on
the starter application:
- `minutes_parked` accepts same-day 24-hour times in `HH:MM-HH:MM` format.
  An exit earlier than entry is rejected (overnight parking is not specified
  in the supplied starter code).
- `hourly_rate` accepts bike, car, and truck, ignoring case and surrounding
  whitespace.
- `format_plate` accepts Indian-style `LLDDLLDDDD` registration strings and
  returns `LL DD LL DDDD` in uppercase.

If your faculty handout specifies different input rules, follow that handout.
