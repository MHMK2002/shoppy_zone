# Shoppy Zone

Shoppy Zone is a Django-based study project that provides a RESTful API for user authentication and account management. It uses Django REST Framework (DRF) and Simple JWT for token-based authentication.

## Features

- User signup functionality.
- Token-based authentication using JWT.
- PostgreSQL database integration.

## Requirements

- Python 3.12+
- Django 4.2
- Django REST Framework
- Simple JWT
- PostgreSQL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MHMK2002/shoppy_zone
   cd shoppy_zone
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Update the database credentials in `shoppy_zone/settings.py` under the `DATABASES` section.
   - Apply migrations:
     ```bash
     python manage.py migrate
     ```
