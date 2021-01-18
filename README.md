
# Bramfitt Technical Challenge

  

The challenge is completed with python 3.8 using Flask, postgres and various libraries included in requirements.txt.

## Set Up

For this application, i am using a postgres database. To test application out, please create a postgres database locally and change the variable

> DATABASE

found on line 11 of app.py to:

> postgresql:///[INSER DB NAME]

_or create a local postgres DB named test_db to use the current database settings_

Then in a python prompt, run the following commands and exit:
> from app import db

> db.create_all()

To run the application from your local shell, run the following:
>python3 app.py

The application should then be running on localhost:5000. 
