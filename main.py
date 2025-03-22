"""
Auto-Logger | Python Script Logic and Programming Assisted by ChatGPT

Tracks user inputs based on identity and role (IT Admin or IT User).
Allows up to 5 entries (or early exit with 999) and logs all actions to 'log.txt'.
Invalid entries are flagged with full metadata.
Displays total usage count per option at the end of each session.
Persistent analytics are stored separately in 'analytics.json' and used for admin insights.

Password Info:
Admins:
- Alice: Admin123
- Charlie: RootAccess
Users:
- Bob: User456
- Dana: EntryLevel
- Elliot: StandardUser

Type 'back' to return to the previous menu where applicable.
"""

import time
from datetime import datetime
import os
import random
import json
import getpass

# === USER SETUP ===
USER_CREDENTIALS = {
    "Alice": ("IT Admin", "Admin123"),
    "Charlie": ("IT Admin", "RootAccess"),
    "Bob": ("IT User", "User456"),
    "Dana": ("IT User", "EntryLevel"),
    "Elliot": ("IT User", "StandardUser")
}

VALID_OPTIONS = {
    "1": "Report System Issue",
    "2": "Request Software Installation",
    "3": "Log Outage",
    "4": "Submit Ticket",
    "5": "Other"
}

MAX_ENTRIES = 5
EXIT_CODE = "999"
BACK_CODE = "back"
LOG_FILE = "log.txt"
STATS_FILE = "analytics.json"
RANDOM_NAMES = list(USER_CREDENTIALS.keys())
usage_counts = {key: 0 for key in VALID_OPTIONS}
OPTION_LABEL_TO_KEY = {v.lower(): k for k, v in VALID_OPTIONS.items()}
LOCKOUT_THRESHOLD = 3
LOCKOUT_DURATION = 10

def load_analytics():
    stats = {val: 0 for val in VALID_OPTIONS.values()}
    flags = {user: 0 for user in USER_CREDENTIALS}
    failed_logins = {user: 0 for user in USER_CREDENTIALS}
    lockouts = {user: 0 for user in USER_CREDENTIALS}
    current_user = None

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("User:"):
                    current_user = line.strip().split("User:")[1].strip()
                for val in stats:
                    if f"VALID ENTRY: '{val}'" in line:
                        stats[val] += 1
                if "INVALID ENTRY" in line and current_user:
                    flags[current_user] += 1
                if "FAILED LOGIN" in line:
                    parts = line.split("User:")
                    if len(parts) > 1:
                        user = parts[1].split("|")[0].strip()
                        if user in failed_logins:
                            failed_logins[user] += 1
                if "LOCKOUT TRIGGERED" in line:
                    parts = line.split("User:")
                    if len(parts) > 1:
                        user = parts[1].split("|")[0].strip()
                        if user in lockouts:
                            lockouts[user] += 1

    return {"entries": stats, "flags": flags, "failed_logins": failed_logins, "lockouts": lockouts}

def save_analytics(overall_stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(overall_stats, f, indent=4)

def log_entry(content):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(content + "\n")

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def prompt_input(prompt):
    value = input(prompt).strip()
    if value.lower() == BACK_CODE:
        return BACK_CODE
    if value == EXIT_CODE:
        print("Session exited by user.")
        exit()
    return value

def login():
    failed_attempts = {}

    while True:
        print("\nSelect your user ID:")
        for idx, name in enumerate(RANDOM_NAMES, start=1):
            print(f"{idx}. {name}")
        name_choice = prompt_input("Enter a number (1–5) to select your name (or 999 to quit): ")

        if name_choice == BACK_CODE:
            print("Returning to main menu...\n")
            continue

        if not name_choice.isdigit() or name_choice not in [str(i) for i in range(1, 6)]:
            print("Invalid selection. Please enter a number between 1 and 5.\n")
            continue

        name = RANDOM_NAMES[int(name_choice) - 1]
        expected_role, expected_password = USER_CREDENTIALS[name]
        fail_count = failed_attempts.get(name, 0)

        while True:
            if fail_count >= LOCKOUT_THRESHOLD:
                print("\nToo many failed attempts. You have been locked out for 10 seconds.")
                log_entry(f"LOCKOUT TRIGGERED | User: {name} | Time: {get_timestamp()}")
                time.sleep(LOCKOUT_DURATION)
                failed_attempts[name] = 0
                fail_count = 0

            print(f"\nRole assigned: {expected_role}")
            if fail_count == 2:
                print("⚠️  Warning: One more failed attempt will result in a lockout.")
            password = getpass.getpass(f"Enter password for {name} (or type 'back' to go back): ")

            if password.lower() == BACK_CODE:
                print("Returning to name selection...\n")
                break

            if password == expected_password:
                print("Access granted.\n")
                return name, expected_role
            else:
                fail_count += 1
                failed_attempts[name] = fail_count
                print("Incorrect password.")
                log_entry(f"FAILED LOGIN | User: {name} | Time: {get_timestamp()}")
            # === MAIN FUNCTIONALITY LOOP ===
def selection_loop(name, role):
    analytics = load_analytics()
    stats = analytics["entries"]
    flags = analytics["flags"]
    failed_logins = analytics["failed_logins"]
    lockouts = analytics["lockouts"]

    log_entry("\n=== New Session ===")
    log_entry(f"User: {name}")
    log_entry(f"Role: {role}")
    log_entry(f"Timestamp: {get_timestamp()}\n")

    if role == "IT Admin":
        while True:
            print("\nAdmin Access: Choose one of the following options:")
            print("1. View full log")
            print("2. View summary only")
            print("3. Continue without viewing")

            admin_choice = prompt_input("Enter 1, 2, or 3: ")

            if admin_choice == EXIT_CODE:
                break

            if admin_choice == "1":
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    print("\n--- Full Log ---\n")
                    print(f.read())
            elif admin_choice == "2":
                print("\n--- Analytics Summary ---\n")
                for k, v in stats.items():
                    print(f"{k}: {v} total entries")
                print("\n--- Flagged Entries ---")
                for user, count in flags.items():
                    print(f"{user}: {count} flagged entries")
                print("\n--- Failed Login Attempts ---")
                for user, count in failed_logins.items():
                    print(f"{user}: {count} failed logins")
                print("\n--- Lockouts ---")
                for user, count in lockouts.items():
                    print(f"{user}: {count} lockouts")
            elif admin_choice == "3":
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                continue

            follow_up = prompt_input("Would you like to choose another admin option? (yes/no): ").lower()
            if follow_up != "yes":
                break

    count = 0
    while count < MAX_ENTRIES:
        print("\nSelect an option:")
        for key, val in VALID_OPTIONS.items():
            print(f"{key}. {val}")

        choice = prompt_input("Enter your choice (1-5 or option name, or 999 to quit): ")
        choice_key = choice if choice in VALID_OPTIONS else OPTION_LABEL_TO_KEY.get(choice.lower())

        if not choice_key or choice_key not in VALID_OPTIONS:
            print("Invalid option. Please enter a number 1–5 or the exact option name.")
            log_entry(f"[Entry {count + 1}] INVALID ENTRY: '{choice}'")
            log_entry(f"Flagged User: {name}, Role: {role}, Time: {get_timestamp()}")
        else:
            action = VALID_OPTIONS[choice_key]
            usage_counts[choice_key] += 1
            log_entry(f"[Entry {count + 1}] VALID ENTRY: '{action}'")
            log_entry(f"User: {name}, Role: {role}, Action: {action}, Time: {get_timestamp()}")

        count += 1

    log_entry("\n--- Option Usage Summary ---")
    for key, val in VALID_OPTIONS.items():
        log_entry(f"{val}: {usage_counts[key]} time(s)")
    log_entry("Session ended after 5 entries.\n====================")

# === PROGRAM ENTRY POINT ===
if __name__ == "__main__":
    name, role = login()
    selection_loop(name, role)
    save_analytics(load_analytics())
