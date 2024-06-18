# Setup of Project

1. clone the repo to your local machine

```bash
git clone https://github.com/Ezi-code/eventplanner.git
```

2. chanage directory into the projects directory from your teminal(mac or linux) or command prompt(windows)

```bash
cd eventplanner
```

3. install requirements

```bash
pip install -r requirements.txt
```

- make migrations by runniing

```bash
python manage.py makemigrations
```

and

```bash
python manage.py migrate
```

to create the database tables

- run

```bash
python manage.py createsuperuser
```

and follow the prompt to create an admin accounts.

4. start django server

```bash
python manage.py runserver
```

5. open the app in your browser by visiting

```bash
localhost:8000
```

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

# Google Calendar API integration

- With google calndar api integrated into this project, you need to enble google calendar api and on the google developer cloud console and create credentials. there is a walk-through on the google developer home page that will guide you through the process.

- Save your downloaded credentials file in the main app folder and and rename the file as `creds.json`, this will allow django to automatically locate the file and use if for api authentication and verification when creating calendar events from the app.
