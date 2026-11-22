# Student Portal

A secure, server-rendered student account web application built with **FastAPI**, **Jinja2**, **SQLAlchemy**, and **MySQL**.

---

## Features

- **User Registration:** Validates input data, enforces minimum 8-character passwords, prevents duplicate emails, automatically assigns `student` role, and hashes passwords securely with Argon2.
- **Authentication & Login:** Authenticates credentials by verifying plain passwords against stored Argon2 hashes.
- **Session Management:** Stores session state using signed cookies via Starlette's `SessionMiddleware` (minimal payload containing only the user ID).
- **Protected Student Dashboard:** Displays authenticated student profile information (ID, Name, Email, Role) and allows logout.
- **Role-Based Access Control (RBAC):** Restricts the Admin portal strictly to users with the `admin` role, denying students with a **403 Forbidden** page.
- **Server-Side Rendering & Styling:** Rendered using Jinja2 templates, served with custom CSS including smooth hover transitions and entrance animations.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI (Python) |
| Templating Engine | Jinja2 + HTML |
| Database | MySQL |
| ORM | SQLAlchemy |
| Database Driver | PyMySQL |
| Password Hashing | `pwdlib` with Argon2 |
| Session Handling | Starlette `SessionMiddleware` |

---

## Project Structure

```text
student_portal/
├── main.py              # Application entry point, routes, middleware, and handlers
├── database.py          # Database engine, session maker, and dependency
├── models.py            # SQLAlchemy models (User model)
├── security.py          # Password hashing and verification functions
├── requirements.txt     # Python package dependencies
├── .env                 # Environment variables (credentials & secrets - ignored in Git)
├── .env.example         # Sample environment template
├── static/
│   └── style.css        # Stylesheet, transitions, and keyframe animations
└── templates/
    ├── home.html        # Landing page
    ├── register.html    # Student registration form
    ├── login.html       # Authentication form
    ├── dashboard.html   # Protected student dashboard
    ├── admin.html       # Protected admin panel
    └── access_denied.html # 403 Forbidden access denial page
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+ installed
- MySQL Server installed and running

### 2. Clone / Open Project Directory
```bash
cd student_portal
```

### 3. Create and Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv student
  .\student\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv student
  source student/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Create MySQL Database
Open your MySQL Command Line Client or MySQL Workbench and run:
```sql
CREATE DATABASE portal_db;
```

### 6. Configure Environment Variables
Create a `.env` file in the root directory (you can copy `.env.example`):
```bash
copy .env.example .env
```
Update `.env` with your actual MySQL credentials:
```env
db_user=root
db_password=your_mysql_password
secret_key=your_random_secret_key
```
> **Note:** If your password contains special characters like `@`, URL-encode it (e.g., use `%40` for `@`).

---

## Running the Application

Start the local development server with Uvicorn:

```bash
uvicorn main:app --reload
```

Once started, open your browser and navigate to:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## Assigning Admin Access

By security design, admin privileges cannot be chosen via the registration form. To test the Admin portal:

1. Register an account through `/register` (e.g., `admin@example.com`).
2. Promote the user directly in MySQL:
   ```sql
   USE portal_db;
   UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
   ```
3. Log in with that account to access the **Admin Portal** link.

