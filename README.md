# DevOps Lab: Flask + PostgreSQL + Docker + CI/CD

![CI Pipeline](https://github.com/Sanxpher/devops-lab/actions/workflows/ci.yml/badge.svg)

A hands-on DevOps laboratory focused on containerization, infrastructure automation, and CI/CD pipelines.

## 🎯 Project Overview

This project is a RESTful API (To-Do List) built with Python and Flask, connected to a PostgreSQL database. The entire environment is containerized and orchestrated using Docker Compose, with a fully automated CI pipeline running on GitHub Actions.

## 🛠️ Tech Stack

- **Language:** Python 3.12 (Flask, SQLAlchemy)
- **Database:** PostgreSQL 16
- **Infrastructure:** Docker, Docker Compose
- **Testing:** Pytest (using in-memory SQLite for isolation)
- **CI/CD:** GitHub Actions (Automated testing and Docker image build)
- **Security:** Environment variables managed via `.env` (excluded from Git)

## 🏗️ Architecture

````text
[ Client ] --> [ Flask API (Container) ] --> [ PostgreSQL (Container) ]
                       |
                [ GitHub Actions CI ]
                       |
       [ Pytest Tests ] & [ Docker Build ]
````
## 🚀 How to Run Locally
1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Sanxpher/devops-lab.git
   cd devops-lab
   \`\`\`
2. Create a .env file with the database credentials:

POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

3. Start the containers:
   \`\`\`bash
   docker compose up -d --build
   \`\`\`

4. Test the API:

curl http://localhost:5000/health

## 🔌 API Endpoints
  
   | Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a new task |
| PATCH | `/tasks/<id>/complete` | Mark a task as completed |
| DELETE | `/tasks/<id>` | Delete a task |

## 🧪 Testing & CI/CD

The tests are located in `app/test_app.py`.

When running in the CI environment (or locally via Pytest), the application uses an in-memory SQLite database to ensure fast, isolated tests without the need for a real PostgreSQL instance.

Every push to the main branch triggers the GitHub Actions workflow (`.github/workflows/ci.yml`), which runs the tests and builds the Docker image.

## 🩺 Troubleshooting

- **PostgreSQL Driver Issues:** We use psycopg (v3) instead of psycopg2 to ensure compatibility with Python 3.12 and prevent compilation issues in lightweight Docker images.
- **Docker Cache:** If the container is not picking up code changes, run docker compose down --rmi all -v to clear the cache and volumes.
- **OneDrive Syncing:** If developing inside a OneDrive folder, Docker might fail to read files. It is recommended to move the project to a local directory outside of cloud sync.

## 🗺️ Roadmap
- [x] Phase 1: Containerization (Docker/Compose) and Database setup.
- [x] Phase 2: CI/CD Pipeline (GitHub Actions + Pytest).
- [ ] Phase 3: Kubernetes orchestration and Infrastructure as Code (IaC).
- [ ] Phase 4: DevSecOps (Security scanning) and Monitoring.
