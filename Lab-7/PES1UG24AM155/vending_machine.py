"""Robust vending-machine functions for Lab 7: Fuzz Testing."""


def parse_coins(coins_csv):
    """Parse comma-separated coin values.

    Returns a list of integers, or [] for invalid input.
    """
    if not isinstance(coins_csv, str) or not coins_csv.strip():
        return []

    try:
        parts = [part.strip() for part in coins_csv.split(",")]
        if any(part == "" for part in parts):
            return []
        return [int(part) for part in parts]
    except ValueError:
        return []


def slot_position(code):
    """Convert a slot such as B7 to zero-based (row, column).

    Returns None for invalid input.
    """
    if not isinstance(code, str):
        return None

    code = code.strip().upper()
    if len(code) < 2 or not ("A" <= code[0] <= "Z"):
        return None

    try:
        column_number = int(code[1:])
    except ValueError:
        return None

    if column_number < 1:
        return None

    return ord(code[0]) - ord("A"), column_number - 1


def change_due(payment):
    """Calculate the number of five-unit coins in the change.

    Input format: 'paid/price'. Returns a result string, or None if invalid.
    """
    if not isinstance(payment, str):
        return None

    parts = payment.split("/")
    if len(parts) != 2:
        return None

    try:
        paid = int(parts[0].strip())
        price = int(parts[1].strip())
    except ValueError:
        return None

    if paid < 0 or price < 0 or paid < price:
        return None

    change = paid - price
    return f"{change // 5} five-coins"


def main():
    print("==== Running parse_coins ====")
    coins_input = input("Enter coin values as CSV (e.g. 5,10,25): ")
    print("Coins:", parse_coins(coins_input))

    print("\n==== Running slot_position ====")
    slot_input = input("Enter a slot code (e.g. B7): ")
    print("Row and Column:", slot_position(slot_input))

    print("\n==== Running change_due ====")
    payment_input = input("Enter paid/price (e.g. 200/150): ")
    print("Change Due:", change_due(payment_input))


if __name__ == "__main__":
    main()
