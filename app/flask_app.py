#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
import model.endpoints as ep
from model.graduate import Graduate
import controller.search as search
import os
import controller.pustatus.pustatus as pu

app = Flask(__name__, template_folder='./view', static_folder='./view')
import auth
is_graduate = False
chosen_graduate_or_undergraduate = False

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
    global chosen_graduate_or_undergraduate
    chosen_graduate_or_undergraduate = False
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

    is_admin_param = request.args.get('is_admin')
    is_admin = False;
    if is_admin_param == "true":
        is_admin = True;
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

    html = ""
    grad_card_admin_me = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button class="me-button">Me</button>
                        <button onclick="location.href='/delete_grad?id=%s'" class="delete-button">Delete Graduate</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button onclick="view_popup('%s')" class="learn-more">Learn More</button>
                        </div>"""
    grad_card_admin = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button onclick="location.href='/delete_grad?id=%s'" class="delete-button">Delete Graduate</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button onclick="view_popup('%s')" class="learn-more">Learn More</button>
                        </div>"""
    grad_card_me = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button class="me-button">Me</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button onclick="view_popup('%s')" class="learn-more">Learn More</button>
                        </div>"""
    grad_card = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button onclick="view_popup('%s')" class="learn-more">Learn More</button>
                        </div>"""

    if success_msg != "Success":
        html = '<p style="margin: 23px">%s</p>' % success_msg
    elif len(graduates) == 0:
        html = '<p style="text-align: center">No Grad Students Match The Search Criteria</p>'
    else:
        if is_admin:
            for grad in graduates:
                grad_id = grad.get_grad_id()
                grad_card_info = (
                    grad.get_photo_link(), grad_id,
                    grad.get_first_name(),
                    grad.get_acad_dept(), grad_id)
                if grad.get_grad_id() == netid:
                    html += grad_card_admin_me % grad_card_info
                else:
                    html += grad_card_admin % grad_card_info
        else:
            for grad in graduates:
                grad_card_info = (
                    grad.get_photo_link(), grad.get_first_name(),
                    grad.get_acad_dept(), grad.get_grad_id())
                if grad.get_grad_id() == netid:
                    html += grad_card_me % grad_card_info
                else:
                    html += grad_card % grad_card_info
    response = make_response(html)
    return response

@app.route('/admin_see_grads')
def admin_see_grads():
    html = render_template('search_page.html', is_admin=True)
    response = make_response(html)
    return response

@app.route('/see_grads')
def see_grads():
    global chosen_graduate_or_undergraduate, is_graduate
    if not chosen_graduate_or_undergraduate:
        is_graduate = False
    chosen_graduate_or_undergraduate = True

    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    html = render_template('search_page.html', is_admin=False)
    response = make_response(html)
    return response

@app.route('/header_tabs')
def header_tabs_results():
    global is_graduate
    current_page = request.args.get('page')

    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingadmin"

    has_profile = False
    if ep.get_grad_information(netid):
        has_profile = True

    is_admin = pu.is_administrator(netid)
    html = '<a style="text-decoration: none" href="/">Home</a>'
    if current_page != 'search_page':
        html += '<a style="text-decoration: none" href="/see_grads">Search Graduates</a>'
    if is_graduate:
        if current_page == 'search_page' or current_page == 'about':
            if has_profile:
                html += '<a style="text-decoration: none" href="/form">Update My Profile</a>'
            else:
                html += '<a style="text-decoration: none" href="/form">Create A Profile</a>'
    if not is_graduate and current_page != 'explore':
        html += '<a style="text-decoration: none" href="/explore">Explore</a>'
    if current_page != 'about':
        html += '<a style="text-decoration: none" href="/about">About GrabAGrad</a>'
    if is_admin and current_page != 'admin':
        html += '<a style="text-decoration: none" href="/admin_see_grads">Admin Page</a>'
    response = make_response(html)
    return response

@app.route('/explore')
def explore_page():
    html = render_template('explore_page.html')
    response = make_response(html)
    return response

@app.route('/explorebox')
def explore_page_box():
    num = int(request.args.get('grad'))
    max_num = ep.num_graduates()
    grad = ep.get_grad_by_row(num % max_num)
    html = render_template('explore_box.html', grad=grad)
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
    global chosen_graduate_or_undergraduate, is_graduate
    if not chosen_graduate_or_undergraduate:
        is_graduate = True
        chosen_graduate_or_undergraduate = True

    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingadmin"
    current_grad = ep.get_grad_information(netid)
    #uploaded_image = request.args.get('image_link')
    page = 'update_page.html'
    if not current_grad:
        page = 'form_page.html'
        current_grad = Graduate()
    try:
        html = render_template(page,
                               cloud_name=os.environ['CLOUD_NAME'],
                               grad=current_grad)
    except:
        from controller.keys import CLOUD_NAME
        html = render_template(page,
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

    current_grad = ep.get_grad_information(netid)
    #uploaded_image = request.args.get('image_link')
    if not current_grad:
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
    else:
        try:
            ep.update_grad(netid=netid, name=name, dept=dept, bio=None,
                          un_uni=undergrad, ma_uni=masters,
                          research_focus=research, expected_grad_date=None,
                          years_worked=years_worked, photo_link=photo,
                          website_link=None, experiences=None,
                          industries=industries,
                          interests=None, email=email, phone=phone_number)
        except Exception as ex:
            print("Error from function ep.update_grad()")
            print(ex)
            html = render_template('error.html', error=str(ex))
            return make_response(html)

    # Search thanks displays None otherwise
    if years_worked is None:
        years_worked = ""
    if phone_number is None:
        phone_number = ""
    if photo is None or photo == '' and current_grad:
        photo = current_grad.get_photo_link()

    html = render_template('submission_thanks.html',
                           name=name, dept=dept, bio=None,
                           un_uni=undergrad, ma_uni=masters,
                           research_focus=research,
                           expected_grad_date=None,
                           years_worked=years_worked, photo_link=photo,
                           website_link=None, experiences=None,
                           industries=str.join(', ', industries),
                           interests=None, email=email,
                           phone=phone_number)
    response = make_response(html)
    return response
