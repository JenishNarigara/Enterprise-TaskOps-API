# Enterprise TaskOps API 🚀

A high-performance, asynchronous RESTful API built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL** designed for enterprise-grade project management and multi-employee task assignment.

---

## 🌟 Key Features

- **JWT Authentication & Security:** Secure token-based authentication using jose with bcrypt password hashing.

- **Role-Based Access Control (RBAC):** Granular permissions distinguishing between **Manager** (Full CRUD, project management, task assignments) and **Employee** (View assigned tasks, update task execution status).

- **Advanced Database Architecture:** 
  * Implements a **Many-to-Many (M:N)** relationship using a composite key junction table (`task_assignees`) with `ON DELETE CASCADE`.
  * Optimized bidirectional navigation via SQLAlchemy `backref` (`assigned_tasks`) eliminating manual SQL joins.

- **Production-Ready Exception Handling:** Clean FastAPI HTTP exception handling for 401 (Unauthorized), 403 (Forbidden), and 404 (Not Found) statuses.

- **Interactive OpenAPI/Swagger UI:** Customized Swagger UI with categorized endpoints and detailed request/response schemas.


---

## 🛠️ Tech Stack

- **Language:** Python 3.13+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL / Supabase
- **Authentication:** jose, Passlib (Bcrypt)
- **Data Validation:** Pydantic v2


---

## 📁 Database Schema Highlights

- `users` — Stores account credentials, roles (`manager`, `employee`), and profile data.
- `projects` — Tracks projects owned and managed by managers.
- `tasks` — Core task entities linked to specific projects.
- `task_assignees` — Junction table storing composite keys `(task_id, user_id)` mapping multi-employee assignments.


---

## 🛣️ API Endpoints Overview

### 👤 Users
> Operations for user registration, login, profile, and authentication.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/users/create` | Create Account | ❌ |
| `POST` | `/users/login` | Login Account | ❌ |
| `PUT` | `/users/forgot` | Forgot Password | ❌ |

---

### 📂 Projects
> Manager-level project creation, viewing, updating, and deletion.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/projects/` | View All Projects | 🔒 |
| `GET` | `/projects/{project_id}` | View Specific Project | 🔒 |
| `POST` | `/projects/create` | Create Project | 🔒 |
| `PUT` | `/projects/{project_id}/update` | Edit Project | 🔒 |
| `DELETE` | `/projects/{project_id}/delete` | Delete Project | 🔒 |

---

### 📋 Task
> Task operations, multi-employee assignments, status updates, and employee views.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/task/{task_id}/status` | Check Task Status | 🔒 |
| `GET` | `/task/{project_id}` | View All Tasks | 🔒 |
| `GET` | `/task/` | Specific Status Tasks | 🔒 |
| `GET` | `/task/my-tasks/` | Employee Tasks | 🔒 |
| `POST` | `/task/create` | Create Task | 🔒 |
| `POST` | `/task/{task_id}/assign` | Assign Task | 🔒 |
| `PUT` | `/task/{task_id}/update` | Edit Task | 🔒 |
| `PUT` | `/task/{task_id}/update-status` | Update Task Status | 🔒 |
| `DELETE` | `/task/{task_id}/delete` | Delete Task | 🔒 |

---

### ⚙️ General
> API health check and root endpoint.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Home | ❌ |


---

## ⚙️ Local Setup & Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/JenishNarigara/Enterprise-TaskOps-API.git](https://github.com/JenishNarigara/Enterprise-TaskOps-API.git)
   cd Enterprise-TaskOps-API
