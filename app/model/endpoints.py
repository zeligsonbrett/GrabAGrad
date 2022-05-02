#!/usr/bin/env python

"""
Henry Knoll, Theo Knoll, Brett Zeligson
GrabAGrad
"""

import sqlalchemy as sqla
import model.database_connection as db
from model.graduate import Graduate
import model.departments as depts

def query_all_grads():
    """
    Query all grads in the database
    :return: Graduate object for all graduates in the database
    """

    command = sqla.text('SELECT * FROM graduates')

    output = db.execute_command(command)
    details_list = __details_list(output)
    grad_list = [Graduate(details) for details in details_list]
    return grad_list

def __details_list(output):
    """
    Gets the relevant details for each graduate from a SQL query and assembles into a list
    """
    return [[x['netid'], x['first_name'], x['last_name'], x['acad_dept'], x['industry_experience'],
         x['undergrad_university'], x['undergrad_major'], x['masters_university'], x['masters_field'],
         x['research_focus'], x['years_worked'], x['photo_link']]
        for x in output]

def __details_string():
    """
    Returns a String of all of the fields within the graduates database
    that compose the details list of the Graduate object
    :return: String of all fields of Graduate details, including netid,
    name, acad_dept, bio, undergrad_university, masters_university,
    research_focus, years_worked, photo_link
    """
    details_string = """graduates.netid, graduates.first_name, graduates.last_name,
    graduates.acad_dept, graduates.industry_experience, graduates.undergrad_university, 
    graduates.undergrad_major, graduates.masters_university, graduates.masters_field,
    graduates.research_focus, graduates.years_worked, graduates.photo_link"""
    return details_string


def __id_string(id_list):
    """
    Returns a String WHERE clause to only search for netids that appear
    in id_list
    :return: WHERE id IN ( ... )
    """
    if len(id_list) > 0:
        id_string = "'"
        id_string += "', '".join(id_list)
        id_string += "'"
        return 'WHERE netid IN ( {} )'.format(id_string)
    else:
        return ''


def __prepare_argument(user_input):
    """
    Prepares the user input for use in SQL by adding wildcards
    :return: The user input, prepared for use in an SQL statement
    """
    if user_input == None:
        user_input = ''
    user_input = user_input.replace("%", "\%")
    user_input = user_input.replace("%", "\_")
    prepped_arg = '%' + user_input + '%'
    return prepped_arg

def get_grad_by_row(row_param):
    """
    Gets a certain grad by the row number in the database
    """
    command = sqla.text("""SELECT netid FROM public.graduates LIMIT 1 OFFSET :row;""")
    params = {'row': row_param}
    output = db.execute_command(command, params)
    ids = [x['netid'] for x in output]
    return get_grad_information(ids[0])

def num_graduates():
    """
    Gets total number of graduates in the database
    """
    command = sqla.text("""SELECT COUNT(*) FROM public.graduates;""")
    output = db.execute_command(command)
    count = [x for x in output]
    return int(count[0][0])

def add_favorite(user_id, fav_id):
    """
    Adds a favorite to the database when user_id favorites fav_id
    """
    command = sqla.text("""DELETE FROM public.undergrad_favorites WHERE user_netid=:netid AND netid=:favoriteid;""")
    params = {'netid': user_id, 'favoriteid': fav_id}
    output = db.execute_command(command, params)
    command = sqla.text("""INSERT INTO public.undergrad_favorites VALUES (:netid, :favoriteid);""")
    output = db.execute_command(command, params)

def get_favorites(netid):
    """
    Gets a list of the favorited graduates for a certain netid
    """
    command = sqla.text("""SELECT netid FROM public.undergrad_favorites WHERE user_netid=:netid;""")
    params = {'netid': netid}
    output = db.execute_command(command, params)
    ids = [x['netid'] for x in output]
    favorites = __create_graduates_list(ids)
    return favorites

def find_favorites_from_list(netid, listids):
    """
    Finds the graduates in listids that the user netid has favorited
    """
    if netid:
        command = sqla.text("""SELECT netid FROM public.undergrad_favorites WHERE user_netid=:netid;""")
        params = {'netid': netid}
        output = db.execute_command(command, params)
        favorites = [x['netid'] for x in output]
        return list(set.intersection(set(favorites), set(listids)))
    else:
        return listids

def is_favorite(netid, fav_id):
    """
    Returns whether or not fav_id is a favorite of netid
    """
    command = sqla.text("""SELECT * FROM public.undergrad_favorites WHERE user_netid=:netid AND netid=:favoriteid;""")
    params = {'netid': netid, 'favoriteid': fav_id}
    output = db.execute_command(command, params)
    exists = [x for x in output]
    return len(exists) != 0
    
def remove_favorite(user_id, fav_id):
    """
    Removes a favorite fav_id from the user user_id
    """
    command = sqla.text("""DELETE FROM public.undergrad_favorites WHERE user_netid=:netid AND netid=:favoriteid;""")
    params = {'netid': user_id, 'favoriteid': fav_id}
    output = db.execute_command(command, params)

def __create_graduates_list(id_list):
    """
    Creates and returns a list of graduates that have ids from id_list.
    In doing so, retrieves information about details, industries,
    experiences, interests, and contact information.
    Note, this currently queries pretty inefficiently to create the
    industry, experiences, interest, and contact attributes of a grad
    :param id_list: A list of netid's corresponding to graduates in the
                    database.
    :return: A list of Graduate objects corresponding with netids from
             id_list
    """
    if len(id_list) == 0:
        return []

    details_command = sqla.text("""SELECT {} FROM graduates {} 
        ORDER BY netid""".format(__details_string(), __id_string(id_list)))
    details_output = db.execute_command(details_command)
    details_list = __details_list(details_output)

    contact_list = []

    # Note, row[0] is the row's id. This is used to query the other
    # tables.
    for row in details_list:
        contacts_command = sqla.text("""SELECT email, phone
                                          FROM grad_contact WHERE netid = 
                                          '{}'""".format(row[0]))
        contact_output = db.execute_command(contacts_command)
        row_contact = [[x['email'], x['phone']] for x in contact_output]
        contact_list.append(row_contact)

    grad_list = [Graduate(details=details_list[i],
                          contact=contact_list[i])
                 for i in range(len(details_list))]
    return grad_list


def search_grads(name=None, dept=None, research=None,
                 undergrad_uni=None, masters_uni=None, years_worked=None,
                 industry=None, favorites_on=False, mynetid=None):
    """
    Search all grads for matches based on search criteria
    :return: Graduate object for all matching graduates
    """
    name = __prepare_argument(name)
    dept = __prepare_argument(dept)
    research = __prepare_argument(research)
    undergrad_uni = __prepare_argument(undergrad_uni)
    masters_uni = __prepare_argument(masters_uni)

    if years_worked is None or years_worked == '':
        years_worked_c = ''
    else:
        years_worked_c = 'AND years_worked >= {}'.format(years_worked)

    industry = __prepare_argument(industry)
    command = sqla.text(
        """SELECT DISTINCT graduates.netid FROM 
        graduates WHERE CONCAT(first_name, ' ', last_name) ILIKE :name AND 
        (acad_dept ILIKE :dept OR acad_dept_abbrev ILIKE :dept) AND research_focus ILIKE :research AND 
        undergrad_university ILIKE :undergrad_uni AND masters_university
        ILIKE :masters_uni {} AND industry_experience ILIKE :industry ORDER BY graduates.netid
        ASC;""".format(years_worked_c))
    params = {'name': name, 'dept': dept, 'research': research,
              'undergrad_uni': undergrad_uni,
              'masters_uni': masters_uni, 'years_worked': years_worked,
              'industry': industry}
    output = db.execute_command(command, params)
    ids = [x['netid'] for x in output]
    if favorites_on:
        ids = find_favorites_from_list(mynetid, ids)
    grad_list = __create_graduates_list(ids)
    return grad_list

def get_grad_information(netid):
    """
    Gets overview information for a certain netid graduate
    """
    command = sqla.text(
        'SELECT * FROM public.graduates WHERE graduates.netid=:netid')
    params = {'netid': netid}
    output1 = db.execute_command(command, params)

    contact_command = sqla.text(
        'SELECT * FROM public.grad_contact WHERE grad_contact.netid=:netid')
    params = {'netid': netid}
    contact_output = db.execute_command(contact_command, params)

    all_details = __details_list(output1)

    # Returns if no graduate was found for the netid
    if len(all_details) == 0:
        return None

    contact = [[x['email'], x['phone']] for x in contact_output]
    return Graduate(details=all_details[0], contact=contact)

def update_grad(netid, first_name, last_name, dept=None, un_uni=None, 
               undergrad_major=None, ma_uni=None, masters_field=None,
               research_focus=None, years_worked=None, photo_link=None,
               industry_experience=None, email=None, phone=None):
    """
    Initial update function for updating fields for certain graduates
    """
    abbrev = depts.abbreviation(dept)
    print(abbrev)
    command = sqla.text(
            """UPDATE graduates SET 
            first_name = :firstname, last_name = :lastname, acad_dept = :dept, years_worked = :years_worked,
            undergrad_university = :undergrad_uni, undergrad_major = :undergrad_major, masters_university = :masters_uni, masters_field = :masters_field, 
            research_focus = :research_focus, industry_experience = :industryexperience, acad_dept_abbrev = :abbrev WHERE graduates.netid = :netid;""")
    params = {'netid': netid, 'firstname': first_name, 'lastname': last_name, 'dept': dept, 'years_worked': years_worked, 
              'research_focus': research_focus, 'undergrad_uni': un_uni, 'undergrad_major': undergrad_major, 'masters_uni': ma_uni, 
              'masters_field': masters_field, 'industryexperience': industry_experience, 'abbrev': abbrev}
    output = db.execute_command(command, params)

    params = {'netid': netid}
    remove_contact = sqla.text("""DELETE FROM public.grad_contact WHERE netid=:netid;""")
    output = db.execute_command(remove_contact, params)

    if photo_link is not None and photo_link != '':
         command = sqla.text(
            """UPDATE graduates SET 
            photo_link = :photo WHERE graduates.netid = :netid;""")
         params = {'netid': netid, 'photo': photo_link}
         output = db.execute_command(command, params)

    if email is not None or phone is not None:
        if email != '' or phone != '':
            contact_info = {'netid': netid, 'email': email, 'phone': phone}
            statement = sqla.text(
                """INSERT INTO grad_contact(netid, email, phone) VALUES(:netid, 
                :email, :phone)""")
            output = db.execute_command(statement, contact_info)

def add_a_grad(netid, first_name, last_name, dept=None, un_uni=None, 
               undergrad_major=None, ma_uni=None, masters_field=None,
               research_focus=None, years_worked=None, photo_link=None,
               industry_experience=None, email=None, phone=None):
    """
    Adds a grad to the database in each respective table based on data
    inputted
    """
    abbrev = depts.abbreviation(dept)
    graduates_info = {"netid": netid,
                      "first_name": first_name,
                      "last_name": last_name,
                      "acad_dept": dept,
                      "industry_experience": industry_experience,
                      "undergrad_university": un_uni,
                      "undergrad_major": undergrad_major,
                      "masters_university": ma_uni,
                      "masters_field": masters_field,
                      "research_focus": research_focus,
                      "years_worked": years_worked,
                      "photo_link": photo_link,
                      "abbrev": abbrev}
    statement = sqla.text(
        """INSERT INTO graduates(netid, first_name, last_name, acad_dept, industry_experience, 
        undergrad_university, undergrad_major, masters_university, masters_field, research_focus, 
        years_worked, photo_link, acad_dept_abbrev) 
        VALUES(:netid, :first_name, :last_name, :acad_dept, :industry_experience,
        :undergrad_university, :undergrad_major, :masters_university, :masters_field, :research_focus,
        :years_worked, :photo_link, :abbrev)""")
    output = db.execute_command(statement, graduates_info)

    if email is not None or phone is not None:
        if email != '' or phone != '':
            contact_info = {'netid': netid, 'email': email, 'phone': phone}
            statement = sqla.text(
                """INSERT INTO grad_contact(netid, email, phone) VALUES(:netid, 
                :email, :phone)""")
            output = db.execute_command(statement, contact_info)

def delete_grad(net_id):
    """
    Deletes all rows corresponding to id from the graduate tables
    """
    # param = {'id': id}
    # statement = 'DELETE graduates, grad_contact, grad_experiences, grad_industries, grad_interests FROM graduates INNER JOIN grad_contact INNER JOIN grad_experiences INNER JOIN grad_industries INNER JOIN grad_interests ON graduates.id = :id AND grad_contact.id = :id AND grad_experiences = :id AND grad_industries = :id AND grad_interests = :id'
    # output = db.execute_command(statement, param)
    db.del_id_from_tables(
        ['grad_contact', 'undergrad_favorites', 'graduates'], net_id)
