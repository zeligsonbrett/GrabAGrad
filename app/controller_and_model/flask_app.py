#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
import endpoints #import query_all_grads, add_a_grad


app = Flask(__name__, template_folder='../view', static_folder='../view')


@app.route('/')
def index():
    html = render_template('index.html')
    return make_response(html)


@app.route('/see_grads')
def see_grads():
    # engine = create_engine()
    # graduates = query_all_grads()
    try:
        graduates = endpoints.query_all_grads()
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
    html = render_template('search_page.html',
                           grads=graduates)
    response = make_response(html)
    return response

@app.route('/form')
def form():
    html = render_template('form_page.html')
    return make_response(html)

# add in form one
# call add_a grad with the saerch form
# name and dept is required
# use add_a_grad variable names

@app.route('/submit')
def submit():
    # engine = create_engine()
    name = request.args.get('name')
    major = request.args.get('major')
    bio = request.args.get('bio')
    print(name, major, bio)
    try:
        endpoints.add_a_grad(name=name, dept=major, bio=bio)
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

