"""Fitness Club Class Booking Ledger.

Books members into gym classes up to a capacity limit, handles
cancellations and exports the class rosters to a JSON file.
"""

import glob
import json
import os

# Global state
class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class if there is a free seat.

    Returns True if the booking succeeded, False otherwise.
    """
    if attendance_log is None:
        attendance_log = []
    if class_name not in class_capacity:
        print("No such class:", class_name)
        return False
    roster = rosters.setdefault(class_name, [])
    if member_id in roster:
        print("Already booked:", member_id, "in", class_name)
        return False
    if len(roster) >= class_capacity[class_name]:
        print("Class full:", class_name)
        return False
    roster.append(member_id)
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Remove a member from a class roster, if they are booked."""
    try:
        rosters[class_name].remove(member_id)
    except (KeyError, ValueError):
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set the number of seats available in a class.

    Raises ValueError if `seats` is negative.
    """
    if seats < 0:
        raise ValueError(f"Capacity cannot be negative: {seats}")
    class_capacity[class_name] = seats


def add_members(class_name, count):
    """Book `count` walk-in guests into a class."""
    for i in range(count):
        book_class("GUEST-" + str(i), class_name)


def export_roster(file="gym_schedule.json"):
    """Write all class rosters to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(rosters, f)


def clear_old_exports(prefix="old_"):
    """Delete old JSON exports whose names start with `prefix`."""
    for path in glob.glob(glob.escape(prefix) + "*.json"):
        os.remove(path)


def show_rosters():
    """Print every class and the members booked into it."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(str(m) for m in members))


def read_guest_count(prompt, default=1):
    """Ask for a whole number of guests; fall back to `default` if invalid."""
    answer = input(prompt).strip()
    if not answer:
        return default
    try:
        count = int(answer)
    except ValueError:
        print("Not a number, using", default)
        return default
    if count < 0:
        print("Guest count cannot be negative, using", default)
        return default
    return count


def main():
    """Run the booking demo."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class("M6", "HIIT")
    book_class("M5", "Pilates")
    try:
        set_capacity("Spin", -2)
    except ValueError as err:
        print(err)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    n = read_guest_count("How many walk-in guests for HIIT? (Enter for 1): ")
    add_members("HIIT", n)
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
