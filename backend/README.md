# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

> For Linux
```bash
createdb trivia
```

> For windows
```cmd
cd into backend dir
psql trivia postgres
\i trivia.psql
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

> For Linux
```bash
psql trivia < trivia.psql
```
> For windows
```cmd
cd into backend dir
psql trivia postgres
\i trivia.psql
```

### Set up the Server/Flask

> For no windows OS

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

> For windows OS

From within the `./src` directory first ensure you are working using your created virtual environment. enter the following command in order.

```
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV: "development"
flask run
```

## Testing

To deploy the tests, run

> Linux
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
> Windows
```cmd
(form within the backend dir)
psql postgres postgres
drop database trivia_test
create database trivia_test
\c trivia_test
\i trivia.psql
python test_flaskr.py
```