# Setup of Project

1. clone the repo to your local machine `git clone https://github.com/Ezi-code/eventplanner.git`
2. cd into the projects directory `cd eventplanner`
3. install requirements `pip install -r requirements.txt`

- make migrations by runniing `python manage.py makemigrations` and `python manage.py migrate` to create the database tables
- run `python manage.py createsuperuser` and follow the prompt to create an admin accounts.

4. start django server `python manage.py runserver`
5. open the app in your browser by visiting `localhost:8000`

## Credentials for testing

login to `localhost:8000/admin` with:

- username: root
- password: asdf
- emial: <root@demo.com>
