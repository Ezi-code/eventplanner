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

# Summary Of System Features

## Creating an event

You can only create an event if you have an accounts. Registering to attend events on the other hand does not require you to have an accounts.\
When you set up to create an event, you will be presented with a form that will take the details of the event.\
A second form will be displayed after the event details form for you to create event budget.
insert `0` in fields that you have no expenses.

## Dashoard

The system have a dashboard that shows summary of your event activities.\
Use the dashboard to see your guest list, the amount generated from ticket purchase and even make changes to your events.\
Events can be managed deleted and edited from the dashboard.
