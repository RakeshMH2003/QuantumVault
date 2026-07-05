@echo off
TITLE QuantumVault — Building Quantum-Resistant Cybersecurity System
COLOR 0A
cd /d "%~dp0"
echo.
echo  ========================================================
echo    QuantumVault — Quantum-Resistant Cybersecurity System
echo  ========================================================
echo.
if not exist "venv\Scripts\python.exe" (
  echo  Creating virtual environment...
  python -m venv venv
)
call venv\Scripts\activate.bat
echo  Installing dependencies...
pip install flask flask-sqlalchemy flask-login flask-bcrypt psycopg2-binary cryptography --quiet
echo.
set PG_USER=qrc_user
set PG_PASS=qrc_admin_2026
set PG_HOST=localhost
set PG_PORT=5432
set PG_DB=qrc_vault
set SECRET_KEY=quantumvault-ultra-secret-2026
echo  Starting QuantumVault server...
echo.
echo  ========================================================
echo   Open browser:  http://127.0.0.1:5000
echo   Admin login:   admin / Admin@2026
echo  ========================================================
echo.
python app.py
pause
