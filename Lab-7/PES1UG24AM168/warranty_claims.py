"""Robust warranty-claims functions for Lab 7: Fuzz Testing."""

import math


def parse_claim(text):
    """Parse a warranty claim string in 'plan:months' format.

    Returns (TitleCasePlan, float_months) for valid input, or None for invalid input.
    """
    if not isinstance(text, str):
        return None

    parts = text.split(":")
    if len(parts) != 2:
        return None

    plan = parts[0].strip().title()
    if not plan or not any(ch.isalpha() for ch in plan):
        return None

    try:
        months = float(parts[1].strip())
    except ValueError:
        return None

    if not math.isfinite(months) or months < 0:
        return None

    return plan, months


def age_average(ages_csv):
    """Calculate the integer floor average of comma-separated non-negative product ages.

    Returns an int for valid input, or None for invalid input.
    """
    if not isinstance(ages_csv, str) or not ages_csv.strip():
        return None

    parts = [part.strip() for part in ages_csv.split(",")]
    if not parts or any(part == "" for part in parts):
        return None

    try:
        values = [int(part) for part in parts]
    except ValueError:
        return None

    if any(value < 0 for value in values):
        return None

    return sum(values) // len(values)


def payable_charge(text):
    """Calculate the payable repair charge after 18% tax and discount from 'charge|discount'.

    Returns max(charge * 1.18 - discount, 0.0) for valid input, or None for invalid input.
    """
    if not isinstance(text, str):
        return None

    parts = text.split("|")
    if len(parts) != 2:
        return None

    try:
        charge = float(parts[0].strip())
        discount = float(parts[1].strip())
    except ValueError:
        return None

    if not (math.isfinite(charge) and math.isfinite(discount)):
        return None

    if charge < 0 or discount < 0:
        return None

    total = charge * 1.18 - discount
    if not math.isfinite(total):
        return None

    return max(total, 0.0)


def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
