#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
from model.endpoints import query_all_grads
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1 style='color: red'>hello World</h1>"


@app.route('/see_grads')
def see_grads():
    # engine = create_engine()
    graduates = query_all_grads()
    try:
        graduates = query_all_grads()
    except Exception as ex:
        # Note, error.html doesn't exist yet, we need to decide if we
        # want something like this
        html = render_template('error.html', error=str(ex))
        return make_response(html)

    # Note, we need an HTML file that will receive a list of graduate
    # objects (see graduates.py), and then can display relevant info for
    # these graduates. This should be similar to code in A3.
    # someHTMLfileName.html would have fields inputted into it like this
    # but with better formatting
    # <strong>Name:</strong> {{graduate.get_course_name()}}<br>
    html = render_template('someHTMLfileName.html',
                           grads=graduates)
    response = make_response(html)
    return response
