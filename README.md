# Unspoken

An anonymous confession and kindness platform built with Django.

## Features

- Anonymous post submissions with content moderation
- Kindness voting system with weekly highlights
- Automatic expiry and cleanup of old posts
- Admin moderation queue

## Tech Stack

- **Backend**: Django 6.0, Django REST Framework
- **Task Queue**: Celery + Redis
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Static Files**: WhiteNoise

## Local Development

### Prerequisites

- Python 3.13+
- Redis

### Setup

```bash
# Clone the repository
git clone https://github.com/rajmohan-14/unspoken.git
cd unspoken

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
# Edit .env and set your SECRET_KEY, DEBUG=True, and HMAC_SECRET

# Apply migrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

In separate terminals, start Celery:

```bash
# Celery worker
celery -A core worker -l info

# Celery beat scheduler
celery -A core beat -l info
```

The app will be available at http://localhost:8000.

## Deployment with Docker

### Prerequisites

- Docker and Docker Compose

### Steps

```bash
# Copy and configure environment file
cp .env.example .env
# Edit .env and set DEBUG=False, a strong SECRET_KEY, and HMAC_SECRET

# Build and start all services
docker compose up --build -d

# Apply migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser
```

The app will be available at http://localhost:8000.

## Deployment on Heroku / Railway

### Prerequisites

- Heroku CLI or Railway CLI
- Redis add-on (Heroku Redis or Railway Redis)
- PostgreSQL add-on (Heroku Postgres or Railway PostgreSQL)

### Environment Variables

Set these in your hosting platform's dashboard:

| Variable | Description |
|---|---|
| `SECRET_KEY` | A long, random Django secret key |
| `DEBUG` | Set to `False` in production |
| `HMAC_SECRET` | Secret for HMAC token signing |
| `DATABASE_URL` | PostgreSQL connection URL (set automatically by add-on) |
| `CELERY_BROKER_URL` | Redis connection URL (set automatically by add-on) |
| `CELERY_RESULT_BACKEND` | Same as `CELERY_BROKER_URL` |
| `ALLOWED_HOSTS` | Comma-separated list of your domain(s) |

### Heroku

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql  # check https://elements.heroku.com/addons/heroku-postgresql for current plans
heroku addons:create heroku-redis:mini
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set HMAC_SECRET="your-hmac-secret"
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Environment Variables Reference

See [`.env.example`](.env.example) for all available environment variables.
