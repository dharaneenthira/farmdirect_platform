# FarmDirect Database Setup & Developer Guide

This document details the configuration, schema initialization, demo seeding, and test procedures for the MySQL database foundation (STEP 2A) of the FarmDirect platform (SIH26033).

---

## 1. Prerequisites & MySQL Installation

### 1.1 Install MySQL Community Server
- **Windows / macOS / Linux**: Download and install [MySQL Community Server 8.0+](https://dev.mysql.com/downloads/installer/) or install via package manager:
  ```bash
  # Ubuntu / Debian
  sudo apt update && sudo apt install mysql-server

  # macOS (Homebrew)
  brew install mysql
  brew services start mysql
  ```
- Make sure the MySQL server service is running on port `3306`.

---

## 2. Database Creation & User Privileges

1. Log into your MySQL server as the root administrator:
   ```bash
   mysql -u root -p
   ```

2. Create the database and optional dedicated user:
   ```sql
   CREATE DATABASE IF NOT EXISTS farmdirect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER IF NOT EXISTS 'farmdirect_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON farmdirect_db.* TO 'farmdirect_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

---

## 3. Environment Variables Configuration

Copy `.env.example` to `.env` in the root folder:
```bash
cp .env.example .env
```

Configure your `.env` with actual MySQL credentials:
```env
# Database Credentials
DB_HOST=localhost
DB_PORT=3306
DB_NAME=farmdirect_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```
*Note: The actual `.env` file is excluded from Git version control via `.gitignore`.*

---

## 4. Initialize Database Schema & Seed Data

### Option A: Direct MySQL Command Line Execution

1. **Initialize DDL Schema** (`users`, `farmer_profiles`, `buyer_profiles`, `admin_profiles`, `audit_logs`):
   ```bash
   mysql -u root -p farmdirect_db < database/schema.sql
   ```

2. **Seed Demo Data** (Farmer, Buyer, Admin users with Werkzeug hashed passwords and profiles):
   ```bash
   mysql -u root -p farmdirect_db < database/seed.sql
   ```

### Option B: Automatic Table Creation via Flask SQLAlchemy

If running without pre-existing tables, SQLAlchemy will automatically build the tables on server startup:
```python
from backend.db.session import init_db
init_db()
```

---

## 5. Demo Credentials

The `seed.sql` script creates three pre-configured accounts:

| Role | Full Name | Phone / Email | Password | Profile Status |
| :--- | :--- | :--- | :--- | :--- |
| **Farmer** | Ramesh Kumar | `+919876543210` / `farmer.ramesh@example.com` | `FarmerPass2026!` | Verified (Green Valley Organic Farm) |
| **Buyer** | Agro Wholesale Corp | `+919876543211` / `buyer.agro@example.com` | `BuyerPass2026!` | Verified (Agro Wholesale Corp Pvt Ltd) |
| **Admin** | System Administrator | `+919876543212` / `admin.portal@example.com` | `AdminPass2026!` | Operations Oversight |

*Note: All passwords are securely stored as Werkzeug PBKDF2/scrypt hashes, never plain text.*

---

## 6. Running the Flask Backend

1. Install Python backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Run the application:
   ```bash
   python backend/app.py
   ```

3. Test backend & database status:
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```
   **Expected Response**:
   ```json
   {
     "status": "success",
     "backend": "running",
     "database": "connected"
   }
   ```

---

## 7. Running Pytest Suite

Run all automated unit tests (which run safely using an in-memory SQLite test configuration without needing MySQL):
```bash
python -m pytest tests/
```
