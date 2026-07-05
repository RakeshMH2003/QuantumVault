<div align="center">
  <h1>🛡️ QuantumVault</h1>
  <p><b>Military-Grade Quantum Cryptographic Security Platform</b></p>

  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-3.0.2-green.svg" alt="Flask Framework">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue.svg" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Security-Fernet_Symmetric-red.svg" alt="Fernet Security">
</div>

<hr>

## 🚀 What is QuantumVault?
QuantumVault is a cutting-edge web application designed to facilitate **secure, region-agnostic data sharing** between different entities, such as cross-company employees or disparate geographical branches. By utilizing military-grade symmetric encryption, it ensures that your sensitive text and files remain unreadable to anyone without explicit authorization.

## 🌟 How it Provides Services to Users

### 1. 🔐 Data Encryption
Users can securely log in to the application and choose to encrypt sensitive information. 
- You enter your secret data or upload sensitive files.
- QuantumVault immediately encrypts this data on the server side using the highly secure **Fernet** algorithm.
- Upon successful encryption, the system generates a **Unique QRC Code**.

### 2. 📡 Secure Cross-Company Transfer
The real power of QuantumVault lies in its transfer mechanism. 
- The user who encrypted the data takes the generated **QRC Code** and shares it securely (via secure email, physical handoff, etc.) with the intended recipient at another company or location.
- The encrypted data itself is safely stored in our PostgreSQL database and *never leaves the vault*.

### 3. 🔓 Decryption & Retrieval
The recipient, who is also an authorized user of QuantumVault:
- Logs into their own account on the platform.
- Navigates to the **Decrypt Data** section.
- Enters the shared **QRC Code**.
- The system validates the code, instantly decrypts the data in memory, and presents the secret information or provides a secure download link for the file.

### 4. 👁️ Complete Audit Trail (Admin Protection)
For maximum security and accountability, QuantumVault features a robust **Admin Control Center**.
- Every single action (Logins, Encryptions, Decryptions, Downloads) is meticulously logged.
- The system automatically captures the **Real IP Address** of the user (even bypassing proxies) and performs a real-time **Geographic Location Lookup** (City/Country).
- Administrators can review the entire transaction history to ensure no unauthorized access is occurring.

---

## 🛠️ Technology Stack
* **Frontend**: HTML5, Vanilla CSS (Custom Glassmorphism Design), Vanilla JavaScript (IntersectionObserver, Custom Cursors, 3D Tilt).
* **Backend**: Python 3, Flask Application Factory, Flask-SQLAlchemy, Flask-Login.
* **Cryptography**: `cryptography.fernet` module.
* **Database**: PostgreSQL for persistent, robust data storage.

## ⚙️ Quick Start Guide

### 1. Requirements
- Python 3.10+
- PostgreSQL Server running locally or remotely

### 2. Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/RakeshMH2003/QuantumVault.git
   ```
2. Run the automated startup script (Windows):
   ```bash
   run.bat
   ```
   *Note: This script will automatically create a virtual environment, install all dependencies from `requirements.txt`, and start the Flask server on `http://127.0.0.1:5000`.*

### 3. Default Admin Credentials
* **Username**: `admin`
* **Password**: `Admin@2026`

---
<div align="center">
  <i>Built for the next generation of cybersecurity.</i>
</div>
