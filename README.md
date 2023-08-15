# HyperX

A smart clinic Disease Analysis System for Accra Technical University

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Getting Started

For local development you should install first:

1. Docker
2. Docker-compose

## Setting up the project on a local server

1. Open the main directory
2. Build the stack
   ```docker-compose -f local.yml build```
3. Run ```docker-compose -f local.yml up```

## Next Steps

### Import PostgreSQL Database

If you have access to a dumb database, we recommend following the next article

- https://davejansen.com/how-to-dump-and-restore-a-postgresql-database-from-a-docker-container/

## Migrations

Generate migrations
```docker-compose -f local.yml run --rm django python manage.py makemigrations```

Run migrations
```docker-compose -f local.yml run --rm django python manage.py migrate```

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

  ```$ python manage.py createsuperuser ```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.


#### Running tests with pytest

```$ pytest```




