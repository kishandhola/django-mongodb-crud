# Django MongoDB CRUD Application

This project is a simple Django application that demonstrates CRUD (Create, Read, Update, Delete) operations using MongoDB as the database. The application also includes pagination for listing users.

## Features

- Create a new user
- Read/list all users with pagination
- Update an existing user
- Delete a user

## Setup Instructions

### Prerequisites

- Python 3.x
- MongoDB
- Virtualenv (optional, but recommended)

### Installation Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kishandhola/django-mongodb-crud.git
   cd django-mongodb-crud

    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    pip install -r requirements.txt

    python manage.py migrate

    python manage.py runserver
   ```

Main page: http://127.0.0.1:8000/
Add user: http://127.0.0.1:8000/add
Edit user: http://127.0.0.1:8000/edit/{id}


django_mongo/
├── djangocrud/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── templates/
│   │   ├── list-data.html
│   │   └── index.html
├── manage.py
└── README.md

Let me know if there's anything else I can help you with!