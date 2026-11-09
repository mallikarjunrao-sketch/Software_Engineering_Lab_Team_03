"""Hotel room reservation and booking management module."""

import hashlib
import os
import secrets

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}


def book_room(room_num, guest_name, booking_log=None):
    """Reserve an available room for a guest and record the booking."""
    if booking_log is None:
        booking_log = []
    if room_num not in room_inventory or room_inventory[room_num]["is_booked"]:
        return False
    room_inventory[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Cancel an existing booking for the specified room number."""
    try:
        room_inventory[room_num]["is_booked"] = False
        return True
    except KeyError:
        return False


def check_room_status(room_num):
    """Return True if the specified room exists and is currently available."""
    if room_inventory.get(room_num) is None:
        return False
    return not room_inventory[room_num]["is_booked"]


def compute_seasonal_rate(room_num, rate_multiplier=1.25):
    """Calculate the seasonal room price using a numeric multiplier."""
    base_price = room_inventory[room_num]["price"]
    if isinstance(rate_multiplier, str):
        rate_multiplier = float(rate_multiplier.split("*")[-1].strip())
    final_price = base_price * float(rate_multiplier)
    return final_price


def generate_guest_hash(guest_id):
    """Generate a SHA-256 hash digest for a guest identifier."""
    return hashlib.sha256(guest_id.encode()).hexdigest()


def generate_booking_ref():
    """Generate a cryptographically secure 4-digit booking reference."""
    return secrets.randbelow(9000) + 1000


def export_room_ledger(filename="hotel_ledger.txt"):
    """Export the current room inventory ledger to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as ledger_file:
        ledger_file.write(str(room_inventory))
    print(f"Hotel ledger exported to: {filename}")


def main():
    """Run sample hotel booking operations and print the results."""
    hotel_secret_key = os.getenv("HOTEL_SECRET_KEY")
    book_room("101", "Emma Watson")
    cancel_booking("102")
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", 1.25))
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()
    print("Secret key active:", bool(hotel_secret_key))


if __name__ == "__main__":
    main()
