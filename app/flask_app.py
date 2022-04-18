#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
import model.endpoints as ep
import controller.search as search
import os
import controller.pustatus.pustatus as pu

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


@app.route('/about')
def about():
    html = render_template('about.html')
    return make_response(html)


def get_grads_by_filter(name, dept, industry, years_worked, un_uni):
    """
    Takes in the filter parameters and returns a list of graduates.
    """
    graduates = None
    success_msg = "Success"
    if name or dept or industry or years_worked or un_uni:
        success_msg, graduates = search.filter_search(name, dept,
                                                      industry,
                                                      years_worked,
                                                      un_uni)
    else:
        graduates = ep.query_all_grads()
    return success_msg, graduates


@app.route('/filter_grads')
def filter_grads():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    is_admin = pu.is_administrator(netid)
    name = request.args.get('name')
    dept = request.args.get('dept')
    industry = request.args.get('industry')
    years_worked = request.args.get('years_worked')
    un_uni = request.args.get('un_uni')
    type_sort = request.args.get('sortby')
    success_msg, graduates = get_grads_by_filter(name, dept, industry,
                                                 years_worked, un_uni)
    if type_sort == "First Name: Z-A":
        graduates = sorted(graduates, key=lambda x: (
            x._details is None, x._details[1]), reverse=True)
    else:
        graduates = sorted(graduates, key=lambda x: (
            x._details is None, x._details[1]), reverse=False)

    if success_msg != "Success":
        html = '<p style="margin: 23px">%s</p>' % success_msg
    elif len(graduates) == 0:
        html = '<p style="text-align: center">No Grad Students Match The Search Criteria</p>'
    else:
        html = ""
        if (is_admin):
            grad_card = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button onclick="location.href='/delete_grad?id=%s'" class="delete-button">Delete Graduate</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button onclick="view_popup('%s')" class="learn-more">Learn More</button>
                        </div>"""
            for grad in graduates:
                grad_id = grad.get_grad_id()
                grad_card_info = (
                    grad.get_photo_link(), grad_id,
                    grad.get_first_name(),
                    grad.get_acad_dept(), grad_id)
                html += grad_card % grad_card_info
        else:
            html = ""
            grad_card = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button onclick="view_popup('%s')" class="learn-more">Learn More</button>
                        </div>"""
            for grad in graduates:
                grad_card_info = (
                    grad.get_photo_link(), grad.get_first_name(),
                    grad.get_acad_dept(), grad.get_grad_id())
                html += grad_card % grad_card_info
    response = make_response(html)
    return response


@app.route('/see_grads')
def see_grads():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    is_admin = pu.is_administrator(netid)

    html = render_template('search_page.html', is_admin=is_admin)
    response = make_response(html)
    return response


@app.route('/popup')
def popup_results():
    grad_id = request.args.get('id')
    graduate = ep.get_grad_information(grad_id)
    html = render_template('popup_box.html', grad=graduate)
    response = make_response(html)
    return response


@app.route('/delete_grad')
def delete_grad():
    grad_id = request.args.get('id')
    print(grad_id)
    graduate = ep.get_grad_information(grad_id)
    print(graduate.get_name())
    ep.delete_grad(grad_id)
    html = render_template('grad_deleted_page.html', grad=graduate)
    response = make_response(html)
    return response


@app.route('/form')
def form():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingadmin"

    current_grad = ep.get_grad_information(netid)
    uploaded_image = request.args.get('image_link')
    try:
        html = render_template('form_page.html',
                               cloud_name=os.environ['CLOUD_NAME'],
                               grad=current_grad)
    except:
        from controller.keys import CLOUD_NAME
        html = render_template('form_page.html',
                               cloud_name=CLOUD_NAME, grad=current_grad)
    return make_response(html)


@app.route('/submit')
def submit():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingadmin"

    name = request.args.get('name')
    dept = request.args.get('academic-dept')
    undergrad = request.args.get('undergrad-institution')
    masters = request.args.get('masters-institution')
    email = request.args.get('email')
    phone_number = request.args.get('phone-number')
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
        print("Error from function ep.add_a_grad()")
        print(ex)
        html = render_template('error.html', error=str(ex))
        return make_response(html)

    # Search thanks displays None otherwise
    if years_worked is None:
        years_worked = ""
    if phone_number is None:
        phone_number = ""

    html = render_template('submission_thanks.html',
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
