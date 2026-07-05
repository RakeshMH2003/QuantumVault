# Quantum-Resistant Cybersecurity System

A comprehensive web application demonstrating secure authentication, data storage, and post-quantum cryptographic concepts. Built with Flask, SQLite, and Vanilla HTML/CSS/JS.

## Features
- **Secure Authentication**: Utilizing bcrypt for password hashing and robust session management.
- **Post-Quantum Cryptography**: A modular encryption architecture designed to integrate `liboqs` (CRYSTALS-Kyber). Includes a fully functional AES-256-GCM fallback for immediate usage on systems without complex C-compilers.
- **Role-Based Access Control**: Admin dashboards for system oversight vs regular user vaults.
- **Activity Logging**: Comprehensive audit trails of user actions and IP addresses.
- **Modern UI/UX**: A responsive, dark cybersecurity theme utilizing glassmorphism and custom CSS styling.

## Installation & Setup

1. **Navigate to the Project Directory**
   Ensure you are in the `Quantum-Resistant-Cybersecurity-System` folder.

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   # source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Install liboqs for true Post-Quantum Crypto**
   To enable true Kyber KEM, you must build the `liboqs` C library and install the `liboqs-python` wrapper. The system will automatically detect its presence and switch algorithms. Without it, the system safely falls back to strong AES-256-GCM encryption.

5. **Run the Application**
   ```bash
   python app.py
   ```
   The SQLite database (`database.db`) will automatically initialize on the first run.
   
6. **Access the System**
   Open your browser and navigate to `http://127.0.0.1:5000`. 
   *Note: The very first user to register will automatically be granted `admin` privileges.*

## Directory Structure
- `app.py`: Main application entry point and configuration.
- `models/`: Database schema definitions (User, ActivityLog, EncryptedData).
- `routes/`: Blueprint routing logic (auth, dashboard, crypto, admin).
- `utils/`: Core logic for authentication and the modular encryption system.
- `templates/`: HTML structures using Jinja2 templating.
- `static/`: Frontend CSS (dark theme) and JavaScript.
