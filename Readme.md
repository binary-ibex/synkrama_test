### Project setup

create the .env file with the following keys in the project directory

```
SENDGRID_API_KEY=
SENDGRID_SENDER_MAIL=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
SECRET_KEY=
```

Install packages 

```
pip3 install -r requirements.txt
```

Migrate

```
python3 manage.py migrate
```

Runserver

```
python3 manage.py runserver
```