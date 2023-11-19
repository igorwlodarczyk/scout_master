# scout_master

## Setup

```shell
python3 -m venv venv
pip install -r requirements.txt
```

Inside **'src'** directory create **'.env'** file with following structure:
```dotenv
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

To get DB_NAME, DB_USER and DB_PASSWORD follow instructions in this [link](https://docs.netbox.dev/en/stable/installation/1-postgresql/?fbclid=IwAR1Ck6rWGHawq-GhOJhWL_U95JshOHlvjkRtiC3MC-YZyZ_jFmoMsZrhviA).

For SECRET_KEY use Django built-in function to generate keys.
```shell
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

To test configuration run these commands (you need to be inside **'src'** directory):
```shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py create_groups
python3 manage.py runserver
```