# ALX Prodev - Python & MySQL Seed Project

This project demonstrates how to set up a MySQL database using **Python**, seed it with sample data from a CSV file, and manage it via Docker.

---

## Features
- Connects to MySQL using Python (`mysql-connector-python`)
- Creates a database: **ALX_prodev**
- Creates a table: **user_data**
- Loads sample data from `user_data.csv`
- Supports `.env` for environment variables

---

## Requirements
- Docker & Docker Compose
- Python 3.9+ with `venv`

---
## 2. Configure environment

Create a .env file in the root directory:
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=ALX_prodev
```
## 3. Start MySQL with Docker
```
docker run --name mysql-prodev \
  -e MYSQL_ROOT_PASSWORD=yourpassword \
  -p 3306:3306 \
  -d mysql:8.0
```

## 4. Create virtual environment & install dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```