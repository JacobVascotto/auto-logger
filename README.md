Auto-Logger

A professional, terminal-based Python application that captures user actions through secure login and structured logging. Built to demonstrate real-world concepts in authentication, access control, and input validation across multiple IT disciplines.

🔐 Features

Login System with Role-Based AccessSecure authentication for IT Admin and IT User roles. Admins have enhanced capabilities, including access to system usage insights.

Detailed Entry LoggingTracks up to 5 user inputs per session. Logs include timestamps, role, and user identity, and are saved to log.txt.

Admin-Only InsightsAdmin users can:

View the full log file at login

Enter AdminOnly to view an interactive analytics menu

Access usage summaries at the end of a session

Security & ValidationLockout mechanism after failed login attempts, back command support, and full validation for all input prompts.

🚀 How to Run

Tested with Python 3.13.1 using Visual Studio Code on Windows.

Ensure Python 3.6+ is installed.

Clone or download this repository.

Open your terminal and run:

python main.py

Follow prompts to authenticate, make selections, and explore features.

🗂️ File Structure

Auto-Logger/
├── main.py         # Main application logic
├── log.txt         # Automatically generated session log
├── README.md       # Project overview and documentation

📝 Notes & Considerations

The log.txt file is created on first run in the same directory.

Admin-only commands become available post-login and post-session.

Session ends after 5 valid entries or with manual exit code 999.

This script runs entirely in the terminal and does not require external libraries.

💼 Real-World Applications

Auto-Logger maps directly to real-world scenarios in the following IT domains:

Cybersecurity — Role-based access, credential verification, and input validation simulate secure system interactions.

Systems Administration — Logging behavior, timestamps, and tracking reflect practices used in system auditing.

Software Development — Emphasizes readable, modular code and practical user interaction handling.

Data Analytics — Admin features show how entry data can be organized and summarized for interpretation.

Its structure makes it a valuable demonstration of practical scripting, with room to expand into database use, error reporting, or dashboard integration.

🤖 AI Assistance

This project was developed with the aid of ChatGPT to streamline development, clarify logic, and accelerate testing workflows. While the ideas and direction were entirely my own, ChatGPT provided implementation support and helped speed up development — much like referencing existing documentation or debugging resources. The use of AI was primarily for efficiency and clarity, not for creative generation or project design.

🙏 Acknowledgments

Created with implementation support from ChatGPT (OpenAI). All core design decisions are original, while logic was thoughtfully constructed with assistance.

📫 Contact

This project was created for professional demonstration purposes.  
For questions or further discussion, feel free to contact me:

📧 jacob.vascottobus@gmail.com
