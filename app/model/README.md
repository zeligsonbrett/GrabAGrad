# Getting started on GrabAGrad development

## Set up a virtual environment called env
Create the environment from the GrabAGrad directory
```
python -m venv env
```
Activate the environment. Note, this should be done every time you seek to run this project.
```
source env/bin/activate
```

## Create a database access key file called .env
Create an file called ".env" and add the PostgreSQL URI in. It should be available at this link below: 
```
https://data.heroku.com/datastores/e80e2442-84b5-4758-ad29-545caa556027#administration
```
If that link didn't work, on Heroku site once within the grab-a-grad project, go to
```
resources -> Heroku Postgres -> Settings -> 
Database Credentials, click View Credentials -> copy URI string
```

Once the URI is copied to your clipboard, run this command
```
echo URI_STRING_HERE > env/.env
```

## Other To-Dos
Provided your virtual environment is activated (you should see (env) before your name on the terminal),
ensure your requirements are up-to-date.
```
pip install -r requirements.txt
```
If you update requirements, run 
```
python -m pip freeze > requriements.txt
```


