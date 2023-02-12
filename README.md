# How to start the project

## 1. Create venv and activate Venv:
```console
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Start project:
```console
python manage.py makemigrations authentication
python manage.py migrate
python manage.py runserver
```
