# CRM Celery Setup

## Requirements
- Redis server
- Celery
- django-celery-beat

## Setup
Install Redis:
```bash
sudo apt-get install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

## Install dependencies:
```bash
pip install -r requirements.txt
```

## Run migrations:
```bash
python manage.py migrate
```
## Start Celery worker:
```bash
celery -A crm worker -l info
```