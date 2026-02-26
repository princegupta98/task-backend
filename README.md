"# task-backend" 

FastAPI + PostgreSQL + SQLAlchemy + JWT

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create PostgreSQL database
createdb task_manager_db

# 3. Update .env with your DB credentials

# 4. Run the server
uvicorn app.main:app --reload
```

## Docs
Visit http://localhost:8000/docs for the interactive Swagger UI.

## API Overview

| Method | Endpoint 	| Auth | Description |
|--------|----------	|------|-------------|
| POST 	 | /auth/register | ❌ | Register new user |
| POST	 | /auth/login  | ❌ | Login, get JWT token |
| GET	 | /auth/me 	| ✅ | Get current user |
| GET	 | /projects/ | ✅ | List your projects |
| POST	 | /projects/ | ✅ | Create a project |
| GET	 | /projects/{id} | ✅ | Get project + tasks |
| PUT	 | /projects/{id} | ✅ | Update project |
| DELETE | /projects/{id} | ✅ | Delete project |
| GET	 | /projects/{id}/tasks/ | ✅ | List tasks in project |
| POST	 | /projects/{id}/tasks/ | ✅ | Create task |
| PUT	 | /projects/{id}/tasks/{task_id} | ✅ | Update/complete task |
| DELETE | /projects/{id}/tasks/{task_id} | ✅ | Delete task |

## Task Status Enum
- `todo` (default)
- `in_progress`
- `done`