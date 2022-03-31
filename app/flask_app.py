#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
import model.endpoints as ep
import controller.search as search
from controller.keys import APP_SECRET_KEY
import auth
import os

app = Flask(__name__, template_folder='./view', static_folder='./view')

try:
    app.secret_key = os.environ['APP_SECRET_KEY']
except:
    app.secret_key = APP_SECRET_KEY


@app.route('/')
def index():

    html = render_template('index.html')
    return make_response(html)


@app.route('/see_grads')
def see_grads():
    auth.authenticate()
    # engine = create_engine()
    # graduates = query_all_grads()
    search_input = request.args.get('searchbar')
    #try:
    graduates = None
    if search_input:
        graduates = search.search(search_input)
    else:
        graduates = ep.query_all_grads()
    '''except Exception as ex:
        # Note, error.html doesn't exist yet, we need to decide if we
        # want something like this

        html = render_template('error.html', error=str(ex))
        return make_response(html)
    '''

    # Note, we need an HTML file that will receive a list of graduate
    # objects (see graduates.py), and then can display relevant info for
    # these graduates. This should be similar to code in A3.
    # someHTMLfileName.html would have fields inputted into it like this
    # but with better formatting
    # <strong>Name:</strong> {{graduate.get_course_name()}}<br>
    html = render_template('search_page.html',
                           graduates=graduates)
    response = make_response(html)
    return response

@app.route('/form')
def form():
    username = auth.authenticate()

    html = render_template('form_page.html')
    return make_response(html)

# add in form one
# call add_a grad with the saerch form
# name and dept is required
# use add_a_grad variable names

@app.route('/submit')
def submit():
    username = auth.authenticate()

    # engine = create_engine()
    name = request.args.get('name')
    major = request.args.get('major')
    bio = request.args.get('bio')
    print(name, major, bio)
    try:
        ep.add_a_grad(name=name, dept=major, bio=bio)
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
    html = render_template('search_thanks.html',
                           name=name, major=major, bio=bio)
    response = make_response(html)
    return response

