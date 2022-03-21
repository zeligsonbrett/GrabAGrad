#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
from model.endpoints import query_all_grads
import pandas as pd

app = Flask(__name__)

#result = pd.read_sql(query_text, engine)
#print(result)


@app.route('/')
def index():
    return "<h1 style='color: red'>hello World</h1>"


@app.route('/see_grads')
def db_query():
    # engine = create_engine()
    graduates = query_all_grads()
    # graduates = graduates.replace('\n', '<br/>')
    # print(type(graduates))
    try:
        graduates = query_all_grads()
    except Exception as ex:
        html = render_template('error.html', error=str(ex))
        return make_response(html)

    html = render_template('regdetails.html',
                           class_details=class_details,
                           course_details=course_details)
    response = make_response(html)
    return response
