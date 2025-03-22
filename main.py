# Auto-Logger System
# Created with help from ChatGPT (OpenAI) for implementation support. ReadMe has more details.
# Purpose: A terminal-based logging system with role-based access control, input tracking, and admin-specific tools.
# Considerations:
# - The log file (log.txt) will be created automatically in the current working directory.
# - The program supports up to 5 inputs per session before closing.
# - Admins have extra privileges such as viewing logs and summaries.
# - Use Python 3.6+ to ensure compatibility (for f-string support).
# - Make sure you have write permissions to the directory where the script runs.

import time
from datetime import datetime
import getpass

# === Constants ===
EXIT_CODE = "999"  # Exit trigger value
ADMIN_STATS_TRIGGER = "AdminOnly"  # Admin-only summary trigger
LOG_FILE = "log.txt"  # Output log file
LOCKOUT_DURATION = 10  # Lockout duration in seconds

# === User Credentials ===
USER_CREDENTIALS = {
    "Alice": ("IT Admin", "Admin123"),
    "Charlie": ("IT Admin", "RootAccess"),
    "Bob": ("IT User", "User456"),
    "Dana": ("IT User", "EntryLevel"),
    "Elliot": ("IT User", "StandardUser")
}

# === Valid Menu Options ===
VALID_OPTIONS = {
    "1": "Report System Issue",
    "2": "Request Software Installation",
    "3": "Log Outage",
    "4": "Submit Ticket",
    "5": "Other"
}

# === Logging Helper ===
def log_entry(content):
    """Appends a new log line to the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(content + "\n")

def get_timestamp():
    """Returns the current timestamp formatted as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def show_admin_summary(prompt_message=True):
    """Displays total option usage counts across all sessions."""
    stats = {val: 0 for val in VALID_OPTIONS.values()}
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                for val in VALID_OPTIONS.values():
                    if f"] {val}" in line:
                        stats[val] += 1
    except FileNotFoundError:
        print("Log file not found.")
        return

    print("\n--- Admin Overview: Total Entries for All Options ---")
    for option, count in stats.items():
        print(f"{option}: {count} total entries")
    print("----------------------------------------------------")
    if prompt_message:
        input("\nPress Enter to return to the session menu...")

# === Main Function ===
def main():
    print("=== Welcome to the Auto-Logger System ===")

    # === Login ===
    name = input("Enter your name (or 999 to quit): ").strip()
    if name == EXIT_CODE:
        print("Exiting program.")
        return

    while name not in USER_CREDENTIALS:
        print("Name not recognized. Try again.")
        name = input("Enter your name (or 999 to quit): ").strip()
        if name == EXIT_CODE:
            print("Exiting program.")
            return

    role, correct_password = USER_CREDENTIALS[name]
    attempts = 0
    while True:
        password = getpass.getpass(f"Enter password for {role}: ").strip()
        if password == correct_password:
            break
        else:
            attempts += 1
            if attempts == 2:
                print("WARNING: One more failed attempt will result in lockout.")
            elif attempts >= 3:
                print("Too many failed attempts. You are temporarily locked out.")
                log_entry(f"LOCKOUT TRIGGERED | User: {name} | Time: {get_timestamp()}")
                time.sleep(LOCKOUT_DURATION)
                attempts = 0
            else:
                print("Incorrect password. Try again.")

    # === Start Session ===
    log_entry(f"\n=== New Session ===\nUser: {name}\nRole: {role}\nTimestamp: {get_timestamp()}")

    if role == "IT Admin":
        print("\nAdmin Access Granted.")
        while True:
            view = input("Would you like to view the log file? (yes/no): ").lower().strip()
            if view in ["yes", "no"]:
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")

        if view == "yes":
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    print("\n=== Full Log ===")
                    print(f.read())
                    input("\nPress Enter to continue to session menu...")
            except FileNotFoundError:
                print("Log file not found.")

    print("\nPlease select options (1-5). Enter 999 to end session.")
    if role == "IT Admin":
        print(f"Type '{ADMIN_STATS_TRIGGER}' to view summary during the session.")

    entry_count = 0
    while entry_count < 5:
        print("\nSelect an option:")
        for key, val in VALID_OPTIONS.items():
            print(f"{key}. {val}")
        choice = input("Enter your choice (or 999 to quit): ").strip()

        if choice == EXIT_CODE:
            log_entry("Session ended early by user.")
            break
        elif choice == ADMIN_STATS_TRIGGER and role == "IT Admin":
            show_admin_summary(prompt_message=True)
            continue
        elif choice in VALID_OPTIONS:
            entry_count += 1
            log_entry(f"[Entry {entry_count}] {VALID_OPTIONS[choice]}")
        else:
            print("Invalid option. Please enter a number from 1 to 5 or 999 to quit.")
            continue

    log_entry(f"Session ended after {entry_count} entr{'y' if entry_count == 1 else 'ies'}.")
    log_entry("====================")

    # Prompt Admin to access AdminOnly summary after session ends
    if role == "IT Admin":
        print("\nSession limit reached.")
        while True:
            followup = input("Would you like to view the AdminOnly summary? (yes/no): ").strip().lower()
            if followup == "yes":
                show_admin_summary(prompt_message=False)
                break
            elif followup == "no":
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")

if __name__ == "__main__":
    main()
