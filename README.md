# Weather - Flask
Weather API Repository

## Readme Contents
Project Question
- Platform:
Project (Weather API)
- User story:
As an API user I want to get min, max, average and median temperature and humidity for given city and period of time and store the data in a database.
- Requirements for submission:
- Fork this Repository to get started.
- Use git for version control. 
- Publish your final codebase on a public GitHub repository or send us a compressed codebase with your answers, please avoid using 'Yoyo Wallet' in repo name or description
- On completion email the details to wasim@opencitieslab.org

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

# Green Field flask template

## Technical Specs for QA
* Python 3.10.8
* postgresql 12.6.*

## Backend Setup
### Setting up a virtual environment with Python and pip
* clone the repo
* install a virtual env and activate it: `virtualenv --no-site-packages env; source env/bin/activate`
* install requirements: `pip install -r requirements.txt`

### Setting up a virtual anaconda environment with Python and pip
* clone the repo
* install a virtual conda env: `conda create -n datastories`
* activate the conda env: `source activate datastories`  
_for the VS Code IDE, make sure the new environment is set as the python interpreter_
* install requirements: `pip install -r requirements.txt`  
  _If errors are thrown, comment out the package in package.json, and handle afterwards individually. Uncomment package when committing back into repo_

### Setting up the Database with PostgreSQL
Setup the PostgreSQL database (minimum version 12.*)
```
psql -U postgres
=# CREATE USER stories WITH PASSWORD 'stories';
=# CREATE DATABASE stories;
=# GRANT ALL PRIVILEGES ON DATABASE stories TO stories;
=# \q
```

### Deploying database changes
* datastories App uses Flask-Migrate (which uses Alembic) to handle database migrations.
  
