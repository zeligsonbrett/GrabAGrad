#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model.database_connection import connect_engine, get_uri
from model.endpoints import query_all_grads
import pandas as pd

app = Flask(__name__)
engine = connect_engine()

query_text = 'SELECT name FROM GRADUATES'
with engine.connect() as connection:
    print('This code here accessed')
    result = connection.execute("SELECT name FROM GRADUATES")
    for row in result:
        print(row['name'])

#result = pd.read_sql(query_text, engine)
#print(result)


@app.route('/')
def index():
    return "<h1 style='color: red'>hello World</h1>"


@app.route('/see_grads')
def db_query():
    graduates = query_all_grads(engine)
    return graduates
