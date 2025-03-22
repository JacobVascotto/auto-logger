"""
Auto-Logger | Python Script

Tracks user inputs based on identity and role (IT Admin or IT User).
Allows up to 5 entries (or early exit with 999) and logs all actions to 'log.txt'.
Invalid entries are flagged with full metadata.
"""

import time
from datetime import datetime

# Define valid roles and their corresponding passwords
# This dictionary maps each accepted role to its required password
VALID_ROLES = {
    "IT Admin": "Admin",
    "IT User": "User"
}

# Define the valid selection options users can choose from
VALID_OPTIONS = {
    "1": "Report System Issue",
    "2": "Request Software Installation",
    "3": "Log Outage",
    "4": "Submit Ticket",
    "5": "Other"
}

# Constants used throughout the script
MAX_ENTRIES = 5           # Maximum number of inputs a user can make per session
EXIT_CODE = "999"         # Code to immediately exit the session
LOG_FILE = "log.txt"      # File where all user activity is recorded

# Writes a line of text to the log file
# Called from both login() and selection_loop()
def log_entry(content):
    with open(LOG_FILE, "a") as file:
        file.write(content + "\n")

# Gets the current date and time as a formatted string
# Used to timestamp log entries and invalid flags
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Wrapper for input() that checks for the global exit code
# Ensures that at any input point, entering 999 exits the program cleanly
def prompt_input(prompt):
    value = input(prompt)
    if value == EXIT_CODE:
        print("Session exited by user.")
        exit()
    return value

# Handles the user login process
# Validates both the role and the password tied to it
# Returns name and role if authenticated successfully
def login():
    while True:
        name = prompt_input("Enter your name (or 999 to quit): ").strip()
        role = prompt_input("Enter your role [IT Admin / IT User] (or 999 to quit): ").strip()

        # Checks whether the role entered is supported
        if role not in VALID_ROLES:
            print("Invalid role. Please try again.\n")
            continue

        # Password prompt based on the role
        password = prompt_input(f"Enter password for {role}: ").strip()

        # If the password matches the expected one, allow access
        if password == VALID_ROLES[role]:
            print("Access granted.\n")
            return name, role
        else:
            print("Incorrect password. Restarting login...\n")

# Main loop to accept up to MAX_ENTRIES inputs from the authenticated user
# Records both valid and invalid inputs to the log
# All data is logged along with who entered it and when
def selection_loop(name, role):
    # Log session header information
    log_entry("\n=== New Session ===")
    log_entry(f"User: {name}")
    log_entry(f"Role: {role}")
    log_entry(f"Timestamp: {get_timestamp()}\n")

    count = 0
    while count < MAX_ENTRIES:
        # Print menu options to the user
        print("\nSelect an option:")
        for key, val in VALID_OPTIONS.items():
            print(f"{key}. {val}")

        # Take the user's selection
        choice = prompt_input("Enter your choice (or 999 to quit): ").strip()

        # Check if the input matches a valid option
        if choice in VALID_OPTIONS:
            log_entry(f"[Entry {count + 1}] Valid Option: {VALID_OPTIONS[choice]} ({choice})")
        else:
            # Invalid option entered, log it with full details
            log_entry(f"[Entry {count + 1}] ⚠️ INVALID ENTRY: '{choice}'")
            log_entry(f"Flagged User: {name}, Role: {role}, Time: {get_timestamp()}")

        count += 1

    # Indicate that the session has ended after reaching the input cap
    log_entry("Session ended after 5 entries.\n====================")

# Entry point of the script
# Starts by logging the user in and then entering the input loop
if __name__ == "__main__":
    name, role = login()              # Collect and validate user credentials
    selection_loop(name, role)        # Begin interaction and logging session
