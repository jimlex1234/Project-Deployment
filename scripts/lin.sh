#!/bin/bash

source flaskvenv/bin/activate

cd /trivia/backend

export FLASK_APP=test_flaskr.py
export FLASK_ENV=production


flask run


cd /trivia/frontend

npm install

npm start