# Enterprise TaskOps API 🚀

A high-performance, asynchronous RESTful API built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL** designed for enterprise-grade project management and multi-employee task assignment.

---

## 🌟 Key Features

* **JWT Authentication & Security:** Secure token-based authentication using jose with bcrypt password hashing.
* **Role-Based Access Control (RBAC):** Granular permissions distinguishing between **Manager** (Full CRUD, project management, task assignments) and **Employee** (View assigned tasks, update task execution status).
* **Advanced Database Architecture:** 
  * Implements a **Many-to-Many (M:N)** relationship using a composite key junction table (`task_assignees`) with `ON DELETE CASCADE`.
  * Optimized bidirectional navigation via SQLAlchemy `backref` (`assigned_tasks`) eliminating manual SQL joins.
* **Production-Ready Exception Handling:** Clean FastAPI HTTP exception handling for 401 (Unauthorized), 403 (Forbidden), and 404 (Not Found) statuses.
* **Interactive OpenAPI/Swagger UI:** Customized Swagger UI with categorized endpoints and detailed request/response schemas.

---

## 🛠️ Tech Stack

* **Language:** Python 3.13+
* **Framework:** FastAPI
* **ORM:** SQLAlchemy 2.0
* **Database:** PostgreSQL / Supabase
* **Authentication:** PyJWT, Passlib (Bcrypt)
* **Data Validation:** Pydantic v2

---

## 📁 Database Schema Highlights

* `users` — Stores account credentials, roles (`manager`, `employee`), and profile data.
* `projects` — Tracks projects owned and managed by managers.
* `tasks` — Core task entities linked to specific projects.
* `task_assignees` — Junction table storing composite keys `(task_id, user_id)` mapping multi-employee assignments.

---

## 🛣️ API Endpoints Overview

### 🔐 Users (`/users`)
* `POST /users/create` — Register a new account (Manager / Employee)
* `POST /users/login` — Authenticate and obtain Bearer JWT Token
* `GET /users/profile` — Fetch current user details
* `PUT /users/forgot` — Update account credentials

### 📂 Projects (`/projects`) — *Manager Access*
* `POST /projects/create` — Create a new project
* `GET /projects/` — List all active projects
* `GET /projects/{project_id}` — Get specific project details
* `PUT /projects/{project_id}/update` — Update project title/description
* `DELETE /projects/{project_id}/delete` — Delete a project (Cascade task deletion)

### 📋 Tasks (`/task`)
* `POST /task/create` — Create a task within a project *(Manager)*
* `POST /task/{task_id}/assign` — Multi-assign users to a task *(Manager)*
* `PUT /task/{task_id}/update` — Update task details *(Manager)*
* `DELETE /task/{task_id}/delete` — Remove a task *(Manager)*
* `GET /task/{project_id}` — View all tasks linked to a project
* `GET /task/my-tasks` — Fetch tasks assigned to logged-in user *(Employee)*
* `PUT /task/{task_id}/status` — Update task progress status *(Employee)*

---

## ⚙️ Local Setup & Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/JenishNarigara/Enterprise-TaskOps-API.git](https://github.com/JenishNarigara/Enterprise-TaskOps-API.git)
   cd Enterprise-TaskOps-API