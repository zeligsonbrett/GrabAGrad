#!/usr/bin/env python

"""
Henry Knoll, Theo Knoll, Brett Zeligson
GrabAGrad
"""

from flask import Flask, request, make_response, render_template
import model.endpoints as ep
from model.graduate import Graduate
import controller.search as search
import os
import model.departments as dept
import model.universities as uni
import random

app = Flask(__name__, template_folder='./view', static_folder='./view')

import controller.pustatus.pustatus as pu
import auth
#-------------------------------------------------------------------------

# Determines whether or not CAS authentification will be turned on
try:
    app.secret_key = os.environ['APP_SECRET_KEY']
    # Note, CAS approved for our Heroku site, not for all sites,
    # meaning CAS doesn't work for our local tests.
    cas_enabled = True
except:
    # Note, this except clause is designed to function locally
    from controller.keys import APP_SECRET_KEY
    app.secret_key = APP_SECRET_KEY
    cas_enabled = False

#-------------------------------------------------------------------------

def get_netid(cas_enabled):
    """
    Gets the netid of the current user if CAS authentification is
    on, if not then it must be a local instance and we can return
    the designated testing netid 'testingadmin'
    :param cas_enabled: True if CAS authentification is on, False
                        otherwise
    :return: The netid of the user or 'testingadmin'
    """
    netid = 'testingadmin'
    if cas_enabled:
        netid = auth.authenticate()
        netid = netid.strip()
    return netid

def __get_grads_by_filter(name, dept, industry, years_worked, un_uni, ma_uni, favorites_on, mynetid):
    """
    Takes in the filter parameters and returns a list of graduates.
    :return: Successful search or not?, resulting graduates list
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

def __filter_suggestion_info():
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

        # Ensures all elements are unique
        un_unis = list(dict.fromkeys(un_unis))
        ma_unis = list(dict.fromkeys(ma_unis))

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


#-------------------------------------------------------------------------
#   Flask Endpoints
#-------------------------------------------------------------------------

@app.route('/')
def landing_page():
    """
    Routes the landing page of the app: index.html
    """
    html = render_template('index.html')
    return make_response(html)

@app.route('/about')
def about_page():
    """
    Route to the about/help page of the app: about.html
    """
    user = request.args.get('user')
    html = render_template('about.html', user=user)
    return make_response(html)

@app.route('/form')
def form():
    """
    Loads either the "Create a Profile" or "Update My Profile" page when a graduate wants to input/change their info
    """
    netid = get_netid(cas_enabled)
    current_grad = ep.get_grad_information(netid)

    #uploaded_image = request.args.get('image_link')
    page = 'update_page.html'
    # Get suggestions for text fields
    # industries = ind.get_industries()
    unis = uni.get_universities("")
    dept_list = dept.dept_list()

    if not current_grad:
        # Go to "Create a Profile" page
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

@app.route('/admin_page')
def admin_page():
    """
    Loads the admin page, which is essentially the normal search page but with the option to delete graduates
    """
    netid = get_netid(cas_enabled)
    if pu.is_administrator(netid):
        # Must verify that the user is in fact an administrator
        user = request.args.get('user')
        info = __filter_suggestion_info()
        all_grad_names = info[0]
        depts = info[1]
        # industries = info[2]
        un_unis = info[3]
        ma_unis = info[4]
        html = render_template('search_page.html', user=user, is_admin=True, grad_names=all_grad_names, depts=depts, un_unis=un_unis, ma_unis=ma_unis)
    else:
        html = "<p>ERROR: Must be an administrator to access this page</p>"
    response = make_response(html)
    return response

@app.route('/search_page')
def search_page():
    """
    Loads the search page for users to search through graduates
    """
    netid = get_netid(cas_enabled)

    user = request.args.get('user')

    # Load in search suggestions
    info = __filter_suggestion_info()
    all_grad_names = info[0]
    depts = info[1]
    # industries = info[2]
    un_unis = info[3]
    ma_unis = info[4]

    html = render_template('search_page.html', user=user, is_admin=False, grad_names=all_grad_names, depts=depts, un_unis=un_unis, ma_unis=ma_unis)
    response = make_response(html)
    return response

@app.route('/favorites_page')
def favorites_page():
    """
    Loads the favorites page, where undergraduates can see the graduates who they have favorited
    """
    netid = get_netid(cas_enabled)
    html = render_template('favorites.html')
    response = make_response(html)
    return response


@app.route('/explore_page')
def explore_page():
    """
    Loads the explore page
    """
    # Everytime the explore page opens, a random graduate should be shown
    netid = get_netid(cas_enabled)
    starting_grad_int = random.randint(0, ep.num_graduates())
    html = render_template('explore_page.html', grad=str(starting_grad_int))
    response = make_response(html)
    return response

@app.route('/searchfavorite', methods=['POST'])
def search_favorite():
    """
    Favorites a graduate when the user clicks "Favorite" on their popup in the search page or favorites page
    """
    netid = get_netid(cas_enabled)
    grad_id = request.args.get('grad')
    ep.add_favorite(netid, grad_id)
    return popup_box(grad_id=grad_id, favorite=None, user='undergrad')

@app.route('/searchunfavorite', methods=['POST'])
def search_unfavorite():
    """
    Unfavorites a graduate when the user clicks "Unfavorite" on their popup in the search page or favorites page
    """
    netid = get_netid(cas_enabled)
    grad_id = request.args.get('grad')
    ep.remove_favorite(netid, grad_id)
    return popup_box(grad_id=grad_id, favorite=None, user='undergrad')

@app.route('/removefavorite', methods=['POST'])
def favorite_remove():
    """
    Unfavorites a graduate when the user clicks "Remove" on top of a graduate's card on the Favorites page,
    no response returned
    """
    netid = get_netid(cas_enabled)
    favorite_id = request.args.get('id')
    ep.remove_favorite(netid, favorite_id)
    return '', 204

@app.route('/admin_delete_grad', methods=['POST'])
def admin_delete_grad():
    """
    Deletes a grad when a user clicks "Delete" on the admin page
    """
    netid = get_netid(cas_enabled)
    grad_id = request.args.get('id')
    ep.delete_grad(grad_id)
    return '', 204

@app.route('/self_delete_grad', methods=['POST'])
def self_delete_grad():
    """
    Deletes a grad when a graduate user clicks "Delete Profile" on their Update My Profile page
    """
    try:
        netid = get_netid(cas_enabled)
        deleted_grad = ep.get_grad_information(netid)
        ep.delete_grad(netid)
        html = render_template('grad_deleted_page.html', grad=deleted_grad)
    except Exception as ex:
        html = render_template('error.html', error=str(ex))
    response = make_response(html)
    return response

@app.route('/popup')
def popup_box(grad_id=None, favorite=None, user=None):
    """
    Loads in the popup for a graduates card with their information and the favorite/unfavorite button
    """
    netid = get_netid(cas_enabled)

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

@app.route('/explorebox')
def explore_page_box(grad=None):
    """
    Loads the explore page box including the information about a graduate and the buttons below it
    """
    netid = get_netid(cas_enabled)

    if grad == None:
        num = int(request.args.get('grad'))
        max_num = ep.num_graduates()
        grad = ep.get_grad_by_row(num % max_num)
    html = render_template('explore_box.html', grad=grad, favorite=ep.is_favorite(netid, grad.get_grad_id()))
    response = make_response(html)
    return response

@app.route('/exploretogglefavorite', methods=['POST'])
def explore_favorite():
    """
    Favorites a graduate when the user clicks "Favorite" on the Explore page, unfavorites a graduate 
    when the user clicks "Unfavorite" on the Explore page
    """
    netid = get_netid(cas_enabled)

    # Explore page relies on a numbering system for each graduate, get the correct graduate
    # based on the number id
    num = int(request.args.get('grad'))
    max_num = ep.num_graduates()
    grad = ep.get_grad_by_row(num % max_num)

    favorite = request.args.get('favorite')
    if favorite == "Favorite":
        # Favoriting the grad
        ep.add_favorite(netid, grad.get_grad_id())
    else:
        # Unfavoriting the grad
        ep.remove_favorite(netid, grad.get_grad_id())
    return explore_page_box(grad);

@app.route('/loadfavorites')
def favorites_load():
    """
    Populates the favorites page with the graduates a user has favorited
    """
    netid = get_netid(cas_enabled)
    favorites = ep.get_favorites(netid)

    # HTML template for each grad card
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
        # No favorites added, show a message
        html = '<p style="text-align: center">No Favorites Added</p>'
    else:
        for grad in favorites:
            # Fill in paramaters on graduate template accordingly
            grad_id = grad.get_grad_id()
            grad_card_info = (grad.get_photo_link(), grad.get_grad_id(), grad.get_first_name(), grad.get_acad_dept(), grad.get_grad_id())
            html += grad_card % grad_card_info
    response = make_response(html)
    return response

@app.route('/load_header_tabs')
def load_header_tabs():
    """
    Loads in the proper page tabs for each page on the site since certain pages only have access to certain other pages
    """
    netid = get_netid(cas_enabled)
    current_page = request.args.get('page')
    user = request.args.get('user')
    user_param = 'user=' + user

    has_profile = False
    if ep.get_grad_information(netid):
        has_profile = True
    is_admin = pu.is_administrator(netid)
    
    html = '<a style="text-decoration: none" href="/">Home</a>'
    if current_page != 'search_page':
        html += '<a style="text-decoration: none" href="/search_page?{}">Search</a>'.format(user_param)
    else:
        html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px;" href="/search_page?{}">Search</a>'.format(user_param)
    if user == 'graduate':
        if has_profile:
            html += '<a style="text-decoration: none" href="/form">Update My Profile</a>'
        else:
            html += '<a style="text-decoration: none" href="/form">Create A Profile</a>'
    else:
        if current_page != 'explore':
            html += '<a style="text-decoration: none" href="/explore_page">Explore</a>'
        else:
            html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px; border-radius: 5px;" href="/explore">Explore</a>'
        if current_page != 'favorites':
            html += '<a style="text-decoration: none" href="/favorites_page">Favorites</a>'
        else:
            html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px; border-radius: 5px;" href="/favorites_page">Favorites</a>'
    if is_admin:
        if current_page != 'admin':
            html += '<a style="text-decoration: none" href="/admin_page?{}">Admin Page</a>'.format(user_param)
        else:
            html += '<a style="text-decoration: none; font-weight: bolder; color: white; padding-right: 10px; padding-left: 10px; border-radius: 5px;" href="/admin_page?{}">Admin Page</a>'.format(user_param)
    html += '<a href="/about?{}">'.format(user_param)
    response = make_response(html)
    return response

@app.route('/filter_grads')
def filter_grads():
    """
    Populates the search page grid, admin page grid, and favorites
    grid with the graduates who match the search parameters
    """
    netid = get_netid(cas_enabled)

    # Parameters from the request
    name = request.args.get('name')
    dept = request.args.get('dept')
    industry = request.args.get('industry')
    years_worked = request.args.get('years_worked')
    un_uni = request.args.get('un_uni')
    ma_uni = request.args.get('ma_uni')
    type_sort = request.args.get('sortby')
    is_admin_param = request.args.get('is_admin')
    favorites_only = request.args.get('favorites_on')

    is_admin = False
    favorites_on = False
    if is_admin_param == "true":
        # Need to verify that the user is an administrator
        if pu.is_administrator(netid):
            is_admin = True
    else:
        # Determines if favorites page should load or not
        if favorites_only == 'true':
            favorites_on = True

    # Determines whether search is a success, and loads in respective 
    # graduates
    success_msg, graduates = __get_grads_by_filter(name, dept, industry,
                                                   years_worked, un_uni, 
                                                   ma_uni, favorites_on, 
                                                   netid)

    # Sorts the loaded in graduates by the proper sort-by
    if type_sort == "First Name: Z-A":
        # Alphabetical by last name
        graduates = sorted(graduates, key=lambda x: (
            x._details is None, x._details[1]), reverse=True)
    else:
        # Alphabetical by first name
        graduates = sorted(graduates, key=lambda x: (
            x._details is None, x._details[1]), reverse=False)

    # HTML templates for each grad card (different template for each kind, described below)
    html = ""

    # For the admin page, when the graduate card shares same netid as user
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
    # For the admin page, when graduate card has different netid as user
    grad_card_admin = """
                        <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                        <button onclick="delete_grad('%s')" class="delete-button">Delete Graduate</button>
                        <h2>%s</h2>
                        <p><b></b>%s</p>
                        <br>
                        <br>
                        <button id="learn-more" name="%s" class="learn-more">Learn More</button>
                        </div>"""
    # For the normal search page or favorites page, when the graduate card has same netid as user
    grad_card_me = """
                    <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                    <button class="me-button">Me</button>
                    <h2>%s</h2>
                    <p><b></b>%s</p>
                    <br>
                    <br>
                    <button id="learn-more" name="%s" class="learn-more">Learn More</button>
                    </div>"""
    # For the normal search page or favorites page, when the graduate card has same netid as user
    grad_card = """
                <div class="card">  <img src="%s" onerror="this.onerror=null; this.src='https://res.cloudinary.com/hc9ax9esb/image/upload/v1649079305/grad_photos/ybl7syt9b0nthyamzazg.jpg'" alt="Image of graduate">
                <h2>%s</h2>
                <p><b></b>%s</p>
                <br>
                <br>
                <button id="learn-more" name="%s" class="learn-more">Learn More</button>
                </div>"""

    if success_msg != "Success":
        # Error occurred during search
        html = '<p style="margin: 23px">%s</p>' % success_msg
    elif len(graduates) == 0:
        # No graduates match search criteria
        html = '<p style="text-align: center">No Grad Students Match The Search Criteria</p>'
    else:
        # Search was successful, load in the graduates accordingly
        if is_admin:
            # Admin page
            for grad in graduates:
                # Fill in paramaters on graduate template accordingly
                grad_card_info = (grad.get_photo_link(), grad.get_grad_id(), grad.get_first_name(), grad.get_acad_dept(), grad.get_grad_id())
                if grad.get_grad_id() == netid:
                    html += grad_card_admin_me % grad_card_info
                else:
                    html += grad_card_admin % grad_card_info
        else:
            # Search page or favorites page
            for grad in graduates:
                # Fill in paramaters on graduate template accordingly
                grad_card_info = (grad.get_photo_link(), grad.get_first_name(), grad.get_acad_dept(), grad.get_grad_id())
                if grad.get_grad_id() == netid:
                    html += grad_card_me % grad_card_info
                else:
                    html += grad_card % grad_card_info
    response = make_response(html)
    return response

@app.route('/submit', methods=['POST'])
def submit():
    """
    Takes graduate user input and inserts it into the database accordingly
    """
    netid = get_netid(cas_enabled)
    print(request.form)

    # Get each input field's value

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    dept = request.form['academic-dept']
    undergrad = request.form['undergrad-institution']
    undergrad_major = request.form['undergrad-major']
    masters = request.form['masters-institution']
    masters_field = request.form['masters-degree']
    email = request.form['email']
    phone_number = request.form['phone-number']
    years_worked = request.form['years-worked']
    photo = request.form['image_link']
    research = request.form['research-focus']
    industry_experience = request.form['industry-experience']

    # Strip any leading or trailing whitespace from input
    if first_name: first_name = first_name.strip()
    if last_name: last_name = last_name.strip()
    if dept: dept = dept.strip()
    if undergrad: undergrad = undergrad.strip()
    if undergrad_major: undergrad_major = undergrad_major.strip()
    if masters: masters = masters.strip()
    if masters_field: masters_field = masters_field.strip()
    if email: email = email.strip()
    if phone_number: phone_number = phone_number.strip()
    if years_worked: years_worked = years_worked.strip()
    if research: research = research.strip()
    if industry_experience: industry_experience = industry_experience.strip()

    try:
        years_worked = int(years_worked)
    except:
        years_worked = None

    current_grad = ep.get_grad_information(netid)
    #uploaded_image = request.args.get('image_link')
    if not current_grad:
        # Add a new grad to the database
        try:
            ep.add_a_grad(netid=netid, first_name=first_name, last_name=last_name, dept=dept, industry_experience=industry_experience,
                          un_uni=undergrad, undergrad_major=undergrad_major, ma_uni=masters, masters_field=masters_field,
                          research_focus=research, years_worked=years_worked, photo_link=photo, email=email, phone=phone_number)
        except Exception as ex:
            print("Error from function ep.add_a_grad()")
            print(ex)
            html = render_template('error.html', error=str(ex))
            return make_response(html)
    else:
        # Update a grads information in the database
        try:
            ep.update_grad(netid=netid, first_name=first_name, last_name=last_name, dept=dept,
                          un_uni=undergrad, undergrad_major=undergrad_major, ma_uni=masters, masters_field=masters_field,
                          research_focus=research, years_worked=years_worked, photo_link=photo,
                          industry_experience=industry_experience, email=email, phone=phone_number)
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
                           research_focus=research, years_worked=years_worked, photo_link=photo,
                           industry_experience=industry_experience, email=email,
                           phone=phone_number)
    response = make_response(html)
    return response
