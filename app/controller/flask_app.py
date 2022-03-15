#!/usr/bin/env python
from flask import Flask
from dotenv import load_dotenv
import os
from model.database_connection import create_engine
from model.endpoints import query_all_from_table
import pandas as pd

app = Flask(__name__)

#result = pd.read_sql(query_text, engine)
#print(result)


@app.route('/')
def index():
    return "<h1 style='color: red'>hello World</h1>"


@app.route('/see_grads')
def db_query():
    engine = create_engine()
    graduates = query_all_from_table(engine, 'GRADUATES')
    graduates = graduates.replace('\n', '<br/>')
    return graduates
