#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
import model.endpoints as ep
import controller.search as search
import os
import controller.pustatus.pustatus as pu

app = Flask(__name__, template_folder='./view', static_folder='./view')
search_input = ""
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

@app.route('/about')
def about():
    html = render_template('about.html')
    return make_response(html)


def get_grads(search_input):
    graduates = None
    success_msg = "Success"
    if search_input:
        success_msg, graduates = search.search(search_input)
    else:
        graduates = ep.query_all_grads()
    return success_msg, graduates


@app.route('/see_grads')
def see_grads():
    global search_input
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)


    search_input = request.args.get('searchbar')

    success_msg, graduates = get_grads(search_input)
    html = render_template('search_page.html',
                           success=success_msg, graduates=graduates)
    response = make_response(html)
    return response


@app.route('/popup')
def popup_results():
    grad_id = request.args.get('id')
    graduate = ep.get_grad_information(grad_id)
    html = render_template('popup_box.html', grad=graduate)
    response = make_response(html)
    return response


@app.route('/form')
def form():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingid"

    uploaded_image = request.args.get('image_link')
    try:
        html = render_template('form_page.html',
                               cloud_name=os.environ['CLOUD_NAME'], )
    except:
        from controller.keys import CLOUD_NAME
        html = render_template('form_page.html',
                               cloud_name=CLOUD_NAME)
    return make_response(html)


@app.route('/sortgradsby')
def sort_grads():
    global search_input
    type_sort = request.args.get('Submit')
    success_msg, graduates = get_grads(search_input)
    if success_msg == "Success":
        if type_sort == "First Name: Z-A":
            graduates = sorted(graduates, key=lambda x: (
            x._details is None, x._details[1]), reverse=True)
        else:
            graduates = sorted(graduates, key=lambda x: (
            x._details is None, x._details[1]), reverse=False)

    html = render_template('search_page.html',
                           success=success_msg, graduates=graduates)
    response = make_response(html)
    return response


# add in form one
# call add_a grad with the search form
# name and dept is required
# use add_a_grad variable names

@app.route('/submit')
def submit():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingid"

    name = request.args.get('name')
    dept = request.args.get('academic-dept')
    undergrad = request.args.get('undergrad-institution')
    masters = request.args.get('masters-institution')
    email = request.args.get('email')
    phone_number = request.args.get('phone_number')
    years_worked = request.args.get('years-worked')
    try:
        years_worked = int(years_worked)
    except:
        years_worked = None

    photo = request.args.get('image_link')
    research = request.args.get('research-focus')
    industries = request.args.get('industries')
    industries = [x.strip() for x in industries.split(',')];

    try:
        ep.add_a_grad(netid=netid, name=name, dept=dept, bio=None,
                      un_uni=undergrad, ma_uni=masters,
                      research_focus=research, expected_grad_date=None,
                      years_worked=years_worked, photo_link=photo,
                      website_link=None, experiences=None,
                      industries=industries,
                      interests=None, email=email, phone=phone_number)
    except Exception as ex:
        print(ex)
        html = render_template('error.html', error=str(ex))
        return make_response(html)

    # Search thanks displays None otherwise
    if years_worked is None:
        years_worked = ""
    if phone_number is None:
        phone_number = ""

    html = render_template('search_thanks.html',
                           name=name, dept=dept, bio=None,
                           un_uni=undergrad, ma_uni=masters,
                           research_focus=research,
                           expected_grad_date=None,
                           years_worked=years_worked, photo_link=photo,
                           website_link=None, experiences=None,
                           industries=None,
                           interests=None, email=email,
                           phone=phone_number)
    response = make_response(html)
    return response
