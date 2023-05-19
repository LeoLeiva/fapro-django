# fapro-django

## Usage for local development with Docker

Previous requirements:

- Have docker-compose installed with pip.
- Have ports 8000 free.

Steps to install

1. Create django local settings

```
cp faprodjango/config/settings/local_example.py faprodjango/config/settings/local.py
```

2. Create .env file that contains the environments variables

```
cp env.local .env
```

3. Run project

```
docker-compose up --build
```

## Testing

Running `pytest` on the main directory runs unit and bdd tests.

    pytest

Or individually

    pytest uf/tests/test_view.py::{your class}  # Only unit tests

coverage
```
pytest --cov
```

##### Access to the Swagger interface

```
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```
