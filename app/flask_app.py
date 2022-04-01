#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
import model.endpoints as ep
import controller.search as search
import os

app = Flask(__name__, template_folder='./view', static_folder='./view')

import auth


try:
    app.secret_key = os.environ['APP_SECRET_KEY']
    # Note, CAS approved for our Heroku site, not for all sites,
    # meaning CAS doesn't work for our local tests.
    cas_enabled = True
except:
    # Note, this except clause is designed to function locally.
    from controller.keys import APP_SECRET_KEY
    app.secret_key = APP_SECRET_KEY
    cas_enabled = False


@app.route('/')
def index():

    html = render_template('index.html')
    return make_response(html)


@app.route('/see_grads')
def see_grads():
    if cas_enabled:
        auth.authenticate()

    search_input = request.args.get('searchbar')

    graduates = None
    success_msg = "Success"
    if search_input:
        success_msg, graduates = search.search(search_input)
    else:
        graduates = ep.query_all_grads()

    html = render_template('search_page.html',
                           success=success_msg, graduates=graduates)
    response = make_response(html)
    return response

@app.route('/form')
def form():
    if cas_enabled:
        username = auth.authenticate()

    html = render_template('form_page.html')
    return make_response(html)

# add in form one
# call add_a grad with the search form
# name and dept is required
# use add_a_grad variable names

@app.route('/submit')
def submit():
    if cas_enabled:
        username = auth.authenticate()

    name = request.args.get('name')
    major = request.args.get('major')
    bio = request.args.get('bio')

    try:
        ep.add_a_grad(name=name, dept=major, bio=bio)
    except Exception as ex:
        # Note, error.html doesn't exist yet, we need to decide if we
        # want something like this
        html = render_template('error.html', error=str(ex))
        return make_response(html)

    html = render_template('search_thanks.html',
                           name=name, major=major, bio=bio)
    response = make_response(html)
    return response

