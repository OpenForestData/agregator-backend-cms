# agregator backend cms

## Single command build script

The main part of app is `core` application. This app allows us to easily build solution. 
Building script is created based on django framework commands. This means you can build whole app, but also, perform each of the commands. 

There are 5 commands: 

1. buildapp 
2. cleardatabase
3. initializedata
4. removemigrations


### buildapp
Builds entire solution, run tests, `deletes db(!)`. 
To perform building script you need provide single argument: profile.
The building script need to be run with "settings" profile:


    python manage.py buildapp --profile settings
    

#### cleardatabase
Deletes all tables in Postgres or MySQl DB, in case of using Sqlite, deletes file.
 
    python manage.py cleardatabase
    
    
#### removemigrations
Deletes all migration files in entire solution. 

    python manage.py removemigrations

#### initializedata
Runs intitialization script, to seed db, and perform any other action. You can easily add functions to initializedata. Consider, that each app should have their own initializedata function, and only those functions should be in script. One App - one line to perform. 
 
    python manage.py initializedata

## Environment settings

Environment settings can be easily customized in `.env` file in root of application. 
