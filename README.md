
---

# MWECAU Election Platform - Backend Development Guide

Backend API for the MWECAU Election Platform using Django and Django REST Framework.

## Table of Contents

* [Overview](#overview)
* [Technology Stack](#technology-stack)
* [Getting Started](#getting-started)
* [Development Workflow](#development-workflow)
* [Project Structure](#project-structure)
* [Creating New Features](#creating-new-features)
* [Database Operations](#database-operations)
* [API Development](#api-development)
* [Testing Guide](#testing-guide)
* [Git Workflow](#git-workflow)
* [Troubleshooting](#troubleshooting)

## Overview

Backend development guide for the MWECAU Election Platform.

## Technology Stack

* **Django 4.2+**
* **Django REST Framework**
* **Python 3.8+**
* **PostgreSQL/MySQL/SQLite**
* **Git**

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/mwecau-ict-club/mwecau_election_platform.git
   cd mwecau_election_platform/src/backend
   ```

2. Set up virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   cp .env.example .env
   nano .env
   ```

5. Run migrations and create superuser:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Development Workflow

1. **Activate environment:**

   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Pull latest changes:**

   ```bash
   git pull origin main
   ```

3. **Start development server:**

   ```bash
   python manage.py runserver
   ```

4. **Check for updates and apply migrations:**

   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

## Project Structure

```
/                        # Root directory
├──src
│   ├── core
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── __pycache__
│   │   │   └──....
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── election
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── ...
│   │   ├── models.py
│   │   ├── __pycache__
│   │   │   └── ... 
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── __init__.py
│   ├── manage.py
│   ├── media
│   │   └── candidate_images
│   │       └── ...
│   ├── mw_es
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── static
│   └── templates
│       └── index.html
├── requirements.txt
├── ...........
├── ...........
└── README.md

```

## Creating New Features

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Define models in `models.py`.**

3. **Create migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Define views in `views.py`.**

5. **Add URLs in `urls.py`.**

6. **Register models in `admin.py` (optional).**

## Database Operations

* Create migration files:

  ```bash
  python manage.py makemigrations
  ```

* Apply migrations:

  ```bash
  python manage.py migrate
  ```

* Backup database:

  ```bash
  python manage.py dumpdata > backup.json
  ```

* Restore from backup:

  ```bash
  python manage.py loaddata backup.json
  ```

## API Development

1. **Test API with curl:**

   ```bash
   curl -H "Authorization: Token your-token" http://localhost:8000/api/elections/
   ```

2. **Test API with Python `requests`:**

   ```python
   import requests
   response = requests.get('http://localhost:8000/api/elections/', headers={'Authorization': 'Token your-token'})
   print(response.json())
   ```

## Testing Guide

* Write tests in `tests.py`:

  ```python
  from django.test import TestCase
  from rest_framework.test import APITestCase
  from .models import YourModel

  class YourModelTestCase(APITestCase):
      def test_create_model(self):
          # Test creation of a model instance
  ```

* Run tests:

  ```bash
  python manage.py test
  ```

## Git Workflow

1. **Check the status:**

   ```bash
   git status
   ```

2. **Add changes:**

   ```bash
   git add .
   ```

3. **Commit changes:**

   ```bash
   git commit -m "feat: add feature-name"
   ```

4. **Push changes:**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub after pushing.

## Troubleshooting

1. **Migration conflicts:**

   ```bash
   python manage.py migrate your_app zero
   python manage.py makemigrations your_app
   python manage.py migrate
   ```

2. **Port already in use:**

   ```bash
   python manage.py runserver 8001
   ```

3. **Virtual environment issues:**

   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Database locked (SQLite):**

   ```bash
   rm db.sqlite3
   python manage.py migrate
   ```

### Getting Help

* **Email**: [mwecauictclub@gmail.com](mailto:mwecauictclub@gmail.com)
* **GitHub Issues**: [Create an issue](https://github.com/mwecau-ict-club/mwecau_election_platform/issues)

---
