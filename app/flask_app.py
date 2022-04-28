#!/usr/bin/env python
from flask import Flask, request, make_response, render_template
import model.endpoints as ep
from model.graduate import Graduate
import controller.search as search
import os
import controller.pustatus.pustatus as pu
import model.departments as dept
import model.universities as uni
import model.industries as ind
import random

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
    html = render_template('index.html')
    return make_response(html)

@app.route('/about')
def about():
    user = request.args.get('user')
    html = render_template('about.html', user=user)
    return make_response(html)

def get_grads_by_filter(name, dept, industry, years_worked, un_uni, ma_uni, favorites_on, mynetid):
    """
    Takes in the filter parameters and returns a list of graduates.
    """
    graduates = None
    success_msg = "Success"
    if name or dept or industry or years_worked or un_uni or ma_uni or favorites_on:
        success_msg, graduates = search.filter_search(name, dept,
                                                      industry,
                                                      years_worked,
                                                      un_uni, ma_uni, favorites_on, mynetid)
    else:
        graduates = ep.query_all_grads()
    return success_msg, graduates


@app.route('/filter_grads')
def filter_grads():
    if cas_enabled:
        # Ensures netid is just the name, with no extra spaces.
        netid = auth.authenticate()
        netid = netid.strip()
    else:
        netid = "testingadmin"

    is_admin_param = request.args.get('is_admin')
    is_admin = False
    if is_admin_param == "true":
        is_admin = True

    name = request.args.get('name')
    dept = request.args.get('dept')
    industry = request.args.get('industry')
    years_worked = request.args.get('years_worked')
    un_uni = request.args.get('un_uni')
    ma_uni = request.args.get('ma_uni')
    type_sort = request.args.get('sortby')
    favorites_only = request.args.get('favorites_on')
    favorites_on = False
    if favorites_only == 'true':
        favorites_on = True
    print("Updating")
    success_msg, graduates = get_grads_by_filter(name, dept, industry,
                                                 years_worked, un_uni, ma_uni, favorites_on, netid)
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
                        <button onclick="delete_grad('%s')" class="delete-button">Delete Graduate</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button id="learn-more" name="%s" class="learn-more">Learn More</button>
                        </div>"""
    grad_card_admin = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button onclick="delete_grad('%s')" class="delete-button">Delete Graduate</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button id="learn-more" name="%s" class="learn-more">Learn More</button>
                        </div>"""
    grad_card_me = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button class="me-button">Me</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button id="learn-more" name="%s" class="learn-more">Learn More</button>
                        </div>"""
    grad_card = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button id="learn-more" name="%s" class="learn-more">Learn More</button>
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

def _filter_suggestion_info():
    """
    Creates lists that are needed for the dropdown suggestions feature on the search page
    :return: [graduate_names, departments, ]
    """
    try:
        all_grads = ep.search_grads()
        all_grad_names = [grad.get_name() for grad in all_grads]
        all_industries = []
        dept_list = dept.dept_list()
        un_unis = [grad.get_undergrad_university() for grad in all_grads]
        ma_unis = [grad.get_masters_university() for grad in all_grads]

        # Decided we didn't need information about industries in dropdown
        # for grad in all_grads:
        #     industries = grad.get_industries()
        #     all_industries.extend(industries)
        #
        # all_industries = [word.capitalize() for word in all_industries]
        # all_industries.sort()

        # gets all universities
        # unis = uni.get_universities("")

        # Something to get industries
        # Something to get years worked
        # Something to get undergrad university
    except Exception as ex:
        all_grad_names = []
        all_industries = []
        un_unis = []
        ma_unis = []
        dept_list = []
        print("Error occurred querying all the grads:")
        print(ex)
        pass

    return all_grad_names, dept_list, all_industries, un_unis, ma_unis

@app.route('/admin_see_grads')
def admin_see_grads():
    user = request.args.get('user')
    info = _filter_suggestion_info()
    all_grad_names = info[0]
    depts = info[1]
    # industries = info[2]
    un_unis = info[3]
    ma_unis = info[4]

    html = render_template('search_page.html', user=user, is_admin=True, grad_names=all_grad_names, depts=depts, un_unis=un_unis, ma_unis=ma_unis)
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

    user = request.args.get('user')

    info = _filter_suggestion_info()
    all_grad_names = info[0]
    depts = info[1]
    # industries = info[2]
    un_unis = info[3]
    ma_unis = info[4]

    html = render_template('search_page.html', user=user, is_admin=False, grad_names=all_grad_names, depts=depts, un_unis=un_unis, ma_unis=ma_unis)
    response = make_response(html)
    return response

@app.route('/favorites')
def see_favorites():
    html = render_template('favorites.html')
    response = make_response(html)
    return response

@app.route('/searchfavorite')
def search_favorite():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    grad_id = request.args.get('grad')
    print(grad_id, "ie being added as a favorite")
    ep.add_favorite(netid, grad_id)
    return popup_results(grad_id=grad_id, favorite=True, user='undergrad')

@app.route('/searchunfavorite')
def search_unfavorite():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    grad_id = request.args.get('grad')
    print(grad_id, "is being removed as a favorite")
    ep.remove_favorite(netid, grad_id)
    return popup_results(grad_id=grad_id, favorite=False, user='undergrad')

@app.route('/remove_favorite')
def remove_favorite():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    favorite_id = request.args.get('id')
    ep.remove_favorite(netid, favorite_id)
    return '', 204

@app.route('/load_favorites')
def load_favorites():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    favorites = ep.get_favorites(netid)

    html = ""
    grad_card = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button id="delete-button" name="%s" class="delete-button">Remove</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button id="learn-more" name="%s" class="learn-more">Learn More</button>
                        </div>"""

    if len(favorites) == 0:
        html = '<p style="text-align: center">No Favorites Added</p>'
    else:
        for grad in favorites:
            grad_id = grad.get_grad_id()
            grad_card_info = (
                    grad.get_photo_link(), grad.get_grad_id(), grad.get_first_name(),
                    grad.get_acad_dept(), grad.get_grad_id())
            html += grad_card % grad_card_info
    response = make_response(html)
    return response

@app.route('/explorefavorite')
def favorite_a_grad():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
        is_graduate = pu.is_graduate(netid)
    else:
        netid = "testingadmin"

    num = int(request.args.get('grad'))
    favorite = request.args.get('favorite')
    max_num = ep.num_graduates()
    grad = ep.get_grad_by_row(num % max_num)
    if favorite == "Favorite":
        ep.add_favorite(netid, grad.get_grad_id())
    else:
        ep.remove_favorite(netid, grad.get_grad_id())
    return explore_page_box(grad);

@app.route('/header_tabs')
def header_tabs_results():
    current_page = request.args.get('page')
    user = request.args.get('user')

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

    user_param = 'user=' + user
    html = '<a style="text-decoration: none" href="/">Home</a>'
    if current_page != 'search_page':
        html += '<a style="text-decoration: none" href="/see_grads?{}">Search</a>'.format(user_param)
    else:
        html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px;" href="/see_grads?{}">Search</a>'.format(user_param)
    if user == 'graduate':
        if has_profile:
            html += '<a style="text-decoration: none" href="/form">Update My Profile</a>'
        else:
            html += '<a style="text-decoration: none" href="/form">Create A Profile</a>'
    else:
        if current_page != 'explore':
            html += '<a style="text-decoration: none" href="/explore">Explore</a>'
        else:
            html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px; border-radius: 5px;" href="/explore">Explore</a>'
        if current_page != 'favorites':
            html += '<a style="text-decoration: none" href="/favorites">Favorites</a>'
        else:
            html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px; border-radius: 5px;" href="/favorites">Favorites</a>'
    if is_admin:
        if current_page != 'admin':
            html += '<a style="text-decoration: none" href="/admin_see_grads?{}">Admin Page</a>'.format(user_param)
        else:
            html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px; border-radius: 5px;" href="/admin_see_grads?{}">Admin Page</a>'.format(user_param)
    html += '<a href="/about?{}"><img id="top-right-img" style="z-index: 20000; position: fixed; top: 10px; right: 10px; width: 180px; height: auto;" src="/view/expandedLogo.png"></a>'.format(user_param)
    response = make_response(html)
    return response

@app.route('/explore')
def explore_page():
    html = render_template('explore_page.html', grad=str(random.randint(0, ep.num_graduates())))
    response = make_response(html)
    return response

@app.route('/explorebox')
def explore_page_box(grad=None):
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingadmin"

    if grad == None:
        num = int(request.args.get('grad'))
        max_num = ep.num_graduates()
        grad = ep.get_grad_by_row(num % max_num)
    html = render_template('explore_box.html', grad=grad, favorite=ep.is_favorite(netid, grad.get_grad_id()))
    response = make_response(html)
    return response

@app.route('/popup')
def popup_results(grad_id=None, favorite=None, user=None):
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingadmin"

    if grad_id == None:
        grad_id = request.args.get('id')
    if favorite == None:
        is_favorite = ep.is_favorite(netid, grad_id)
    else:
        is_favorite = favorite
    
    if user == None:
        user = request.args.get('user')

    print(user)
    graduate = ep.get_grad_information(grad_id)
    html = render_template('popup_box.html', user=user, grad=graduate, favorite=is_favorite)
    response = make_response(html)
    return response


@app.route('/delete_grad')
def delete_grad():
    grad_id = request.args.get('id')
    graduate = ep.get_grad_information(grad_id)
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
    #uploaded_image = request.args.get('image_link')
    page = 'update_page.html'
    # industries = ind.get_industries()
    unis = uni.get_universities("")
    dept_list = dept.dept_list()
    if not current_grad:
        page = 'form_page.html'
        current_grad = Graduate()
    try:
        html = render_template(page,
                               cloud_name=os.environ['CLOUD_NAME'],
                               grad=current_grad, dept=dept_list,
                               unis=unis)
    except:
        from controller.keys import CLOUD_NAME
        html = render_template(page,
                               cloud_name=CLOUD_NAME, grad=current_grad,
                               dept=dept_list, unis=unis)
    return make_response(html)


@app.route('/submit')
def submit():
    if cas_enabled:
        netid = auth.authenticate()
        # Ensures netid is just the name, with no extra spaces.
        netid = netid.strip()
    else:
        netid = "testingadmin"

    first_name = request.args.get('first-name').strip()
    last_name = request.args.get('last-name').strip()
    dept = request.args.get('academic-dept').strip()
    undergrad = request.args.get('undergrad-institution').strip()
    undergrad_major = request.args.get('undergrad-major').strip()
    masters = request.args.get('masters-institution').strip()
    masters_field = request.args.get('masters-degree').strip()
    email = request.args.get('email')
    phone_number = request.args.get('phone-number')
    years_worked = request.args.get('years-worked')
    try:
        years_worked = int(years_worked)
    except:
        years_worked = None

    photo = request.args.get('image_link')
    research = request.args.get('research-focus')
    industry_experience = request.args.get('industry-experience')

    current_grad = ep.get_grad_information(netid)
    #uploaded_image = request.args.get('image_link')
    if not current_grad:
        try:
            ep.add_a_grad(netid=netid, first_name=first_name, last_name=last_name, dept=dept, industry_experience=industry_experience,
                          un_uni=undergrad, undergrad_major=undergrad_major, ma_uni=masters, masters_field=masters_field,
                          research_focus=research, expected_grad_date=None,
                          years_worked=years_worked, photo_link=photo,
                          website_link=None, email=email, phone=phone_number)
        except Exception as ex:
            print("Error from function ep.add_a_grad()")
            print(ex)
            html = render_template('error.html', error=str(ex))
            return make_response(html)
    else:
        try:
            ep.update_grad(netid=netid, first_name=first_name, last_name=last_name, dept=dept,
                          un_uni=undergrad, undergrad_major=undergrad_major, ma_uni=masters, masters_field=masters_field,
                          research_focus=research, years_worked=years_worked, photo_link=photo,
                          website_link=None, industry_experience=industry_experience, email=email, phone=phone_number)
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
    if industry_experience is None:
        industry_experience = ""
    if photo is None or photo == '' and current_grad:
        photo = current_grad.get_photo_link()

    html = render_template('submission_thanks.html',
                           first_name=first_name, last_name=last_name, dept=dept,
                           un_uni=undergrad, undergrad_major=undergrad_major, ma_uni=masters, masters_field=masters_field,
                           research_focus=research,
                           expected_grad_date=None,
                           years_worked=years_worked, photo_link=photo,
                           website_link=None, industry_experience=industry_experience, email=email,
                           phone=phone_number)
    response = make_response(html)
    return response
