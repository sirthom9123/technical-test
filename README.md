# Weather - Flask
Weather API Repository

## Readme Contents
Project Question
- Platform:
Project (Weather API)
- User story:
As an API user I want to get min, max, average and median temperature and humidity for given city and period of time
- Requirements:
Use git for version control publish on GitHub or send us a compressed repo (I will set up a repository for each candidate) if making publicly available, please avoid using 'Yoyo Wallet' in repo name or description
- Functionality:
- Create locally running RESTful web API;
- Use the flask-framework provided on this repo, create an API that accepts a request with 'city' and 'period' args;
- Fetches weather data for that location and period of time from some public API e.g. Yahoo! Weather;
- Stores the data in Local Postgres database (Simple Weather table to be setup in the models folder)
- Computes min, max, average and median temperature and humidity for that location and period and returns that to the user;
- Extra goals:
Provide a view which renders a bar chart for the requested data; e.g. Daily average temperature over the last 7 days
- Additional Notes:
Optimize and fix any errors so the code works on local

## Backend Setup
### Setting up a virtual environment with Python 3.6 and pip
* clone the repo
* install a virtual env and activate it: `virtualenv --no-site-packages env; source env/bin/activate`
* install requirements: `pip install -r requirements.txt`

### Development credentials for Local use only
* Copy 'example.development.cfg' file from the config folder
* Paste in the same config folder and rename the new file 'development.cfg'
* Update any local credentials in this new file if required

### Setting up the Database with PostgreSQL
Setup the PostgreSQL database (minimum version 9.6.*)
```
psql -U postgres
=# CREATE USER weather WITH PASSWORD 'weather';
=# CREATE DATABASE weather;
=# GRANT ALL PRIVILEGES ON DATABASE weather TO weather;
=# \q
```
Construct your db app-side:
```
from weather.models import db
from weather.models.seeds import seed_db
run 'python rebuild_db.py'
```

### Command to Start up your application
```
run 'python app.py runserver'
```