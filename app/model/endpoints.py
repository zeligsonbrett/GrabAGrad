#!/usr/bin/env python

import sqlalchemy as sqla
import model.database_connection as db
from model.graduate import Graduate


def query_all_grads():
    """
    Query all grads in the database
    :return: Graduate object for all graduates in the database
    """

    command = sqla.text('SELECT * FROM graduates')

    output = db.execute_command(command)
    details_list = [
        [x['netid'], x['name'], x['acad_dept'], x['bio'],
         x['undergrad_university'], x['masters_university'],
         x['research_focus'], x['expected_grad_date'],
         x['years_worked'], x['photo_link'], x['website_link']]
        for x in output]
    grad_list = [Graduate(details) for details in details_list]
    return grad_list


def __details_string():
    """
    Returns a String of all of the fields within the graduates database
    that compose the details list of the Graduate object
    :return: String of all fields of Graduate details, including netid,
    name, acad_dept, bio, undergrad_university, masters_university,
    research_focus, expected_grad_date, years_worked, photo_link,
    website_link
    """
    details_string = """graduates.netid, graduates.name, 
    graduates.acad_dept, graduates.bio, 
    graduates.undergrad_university, graduates.masters_university, 
    graduates.research_focus, graduates.expected_grad_date, 
    graduates.years_worked, graduates.photo_link, graduates.website_link
    """
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
    command = sqla.text("""SELECT netid FROM public.graduates LIMIT 1 OFFSET :row;""")
    params = {'row': row_param}
    output = db.execute_command(command, params)
    ids = [x['netid'] for x in output]
    return get_grad_information(ids[0])

def num_graduates():
    command = sqla.text("""SELECT COUNT(*) FROM public.graduates;""")
    output = db.execute_command(command)
    count = [x for x in output]
    return int(count[0][0])

def add_favorite(user_id, fav_id):
    command = sqla.text("""DELETE FROM public.undergrad_favorites WHERE user_netid=:netid AND favorite_netid=:favoriteid;""")
    params = {'netid': user_id, 'favoriteid': fav_id}
    output = db.execute_command(command, params)
    command = sqla.text("""INSERT INTO public.undergrad_favorites VALUES (:netid, :favoriteid);""")
    output = db.execute_command(command, params)

def get_favorites(netid):
    command = sqla.text("""SELECT favorite_netid FROM public.undergrad_favorites WHERE user_netid=:netid;""")
    params = {'netid': netid}
    output = db.execute_command(command, params)
    ids = [x['favorite_netid'] for x in output]
    favorites = __create_graduates_list(ids)
    return favorites

def find_favorites_from_list(netid, listids):
    if netid:
        command = sqla.text("""SELECT favorite_netid FROM public.undergrad_favorites WHERE user_netid=:netid;""")
        params = {'netid': netid}
        output = db.execute_command(command, params)
        favorites = [x['favorite_netid'] for x in output]
        return list(set.intersection(set(favorites), set(listids)))
    else:
        return listids

def is_favorite(netid, fav_id):
    command = sqla.text("""SELECT * FROM public.undergrad_favorites WHERE user_netid=:netid AND favorite_netid=:favoriteid;""")
    params = {'netid': netid, 'favoriteid': fav_id}
    output = db.execute_command(command, params)
    exists = [x for x in output]
    return len(exists) != 0
    
def remove_favorite(user_id, fav_id):
    command = sqla.text("""DELETE FROM public.undergrad_favorites WHERE user_netid=:netid AND favorite_netid=:favoriteid;""")
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
    details_list = [
        [x['netid'], x['name'], x['acad_dept'], x['bio'],
         x['undergrad_university'], x['masters_university'],
         x['research_focus'], x['expected_grad_date'],
         x['years_worked'], x['photo_link'], x['website_link']]
        for x in details_output]

    industry_list = []
    experiences_list = []
    interests_list = []
    contact_list = []

    # Note, row[0] is the row's id. This is used to query the other
    # tables.
    for row in details_list:
        industries_command = sqla.text("""SELECT DISTINCT industry FROM 
                                   grad_industries WHERE netid =
                                   '{}'""".format(row[0]))
        industry_output = db.execute_command(industries_command)
        row_industries = [x['industry'] for x in industry_output]
        industry_list.append(row_industries)

        experiences_command = sqla.text("""SELECT DISTINCT experience 
                                    FROM grad_experiences WHERE netid = 
                                    '{}'""".format(row[0]))
        experiences_output = db.execute_command(experiences_command)
        row_experiences = [x['experience'] for x in experiences_output]
        experiences_list.append(row_experiences)

        interests_command = sqla.text("""SELECT DISTINCT interest 
                                  FROM grad_interests WHERE netid = 
                                  '{}'""".format(row[0]))
        interests_output = db.execute_command(interests_command)
        row_interests = [x['interest'] for x in interests_output]
        interests_list.append(row_interests)

        contacts_command = sqla.text("""SELECT email, phone
                                          FROM grad_contact WHERE netid = 
                                          '{}'""".format(row[0]))
        contact_output = db.execute_command(contacts_command)
        row_contact = [[x['email'], x['phone']] for x in contact_output]
        contact_list.append(row_contact)

    grad_list = [Graduate(details=details_list[i],
                          industries=industry_list[i],
                          experiences=experiences_list,
                          interests=interests_list,
                          contact=contact_list)
                 for i in range(len(details_list))]
    return grad_list


def search_grads(name=None, dept=None, research=None, grad_year=None,
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
    grad_year = __prepare_argument(grad_year)

    if years_worked is None or years_worked == '':
        years_worked_c = ''
    else:
        years_worked_c = 'AND years_worked >= {}'.format(years_worked)

    grad_list = []
    if industry is not None and industry != '':
        industry = __prepare_argument(industry)
        command = sqla.text(
            """SELECT DISTINCT graduates.netid FROM 
            graduates, grad_industries
            WHERE graduates.netid = grad_industries.netid AND name ILIKE :name AND 
            acad_dept ILIKE :dept AND research_focus ILIKE :research AND 
            undergrad_university ILIKE :undergrad_uni AND masters_university
            ILIKE :masters_uni {} AND industry ILIKE :industry ORDER BY graduates.netid
            ASC;""".format(years_worked_c))
        params = {'name': name, 'dept': dept, 'research': research,
                  'undergrad_uni': undergrad_uni, 'grad_year':grad_year,
                  'masters_uni': masters_uni, 'years_worked': years_worked,
                  'industry': industry}
        output = db.execute_command(command, params)
        ids = [x['netid'] for x in output]
        if favorites_on:
            ids = find_favorites_from_list(mynetid, ids)
        grad_list = __create_graduates_list(ids)
    else:
        command = sqla.text(
            """SELECT DISTINCT graduates.netid FROM 
            graduates WHERE name ILIKE :name AND acad_dept ILIKE :dept 
            AND research_focus ILIKE :research AND 
            undergrad_university ILIKE :undergrad_uni AND masters_university
            ILIKE :masters_uni {} ORDER BY graduates.netid ASC;""".format(years_worked_c))
        params = {'name': name, 'dept': dept, 'research': research,
                  'undergrad_uni': undergrad_uni, 'grad_year':grad_year,
                  'masters_uni': masters_uni, 'years_worked': years_worked}
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

    industries_command = sqla.text('SELECT * FROM public.grad_industries WHERE grad_industries.netid=:netid')
    output2 = db.execute_command(industries_command, params)
    experiences_command = sqla.text('SELECT * FROM public.grad_experiences WHERE grad_experiences.netid=:netid')
    output3 = db.execute_command(experiences_command, params)
    interests_command = sqla.text('SELECT * FROM public.grad_interests WHERE grad_interests.netid=:netid')
    output4 = db.execute_command(interests_command, params)
    all_details = [
        [x['netid'], x['name'], x['acad_dept'], x['bio'],
         x['undergrad_university'], x['masters_university'],
         x['research_focus'], x['expected_grad_date'],
         x['years_worked'], x['photo_link'], x['website_link']]
        for x in output1]

    # Returns if no graduate was found for the netid
    if len(all_details) == 0:
        return None

    contact = [[x['email'], x['phone']] for x in contact_output]
    industries = [x['industry'] for x in output2]
    experiences = [[x['experience'], x['experience_desc']] for x in output3]
    interests = [x['interest'] for x in output4]
    return Graduate(details=all_details[0], contact=contact, industries=industries, experiences=experiences, interests=interests)

def update_grad(netid, name=None, dept=None, bio=None, un_uni=None, ma_uni=None, 
                research_focus=None, expected_grad_date=None, years_worked=None, photo_link=None,
                website_link=None, industries=None, experiences=None, interests=None, email=None, phone=None):
    """
    Initial update function for updating fields for certain graduates
    """
    command = sqla.text(
            """UPDATE graduates SET 
            name = :name, acad_dept = :dept, years_worked = :years_worked, research_focus = :research, 
            undergrad_university = :undergrad_uni, masters_university
            = :masters_uni WHERE graduates.netid = :netid;""")
    params = {'netid': netid, 'name': name, 'dept': dept, 'years_worked': years_worked, 'research': research_focus, 'undergrad_uni': un_uni, 'masters_uni': ma_uni}
    output = db.execute_command(command, params)

    params = {'netid': netid}
    remove_industries = sqla.text("""DELETE FROM public.grad_industries WHERE netid=:netid;""")
    remove_experiences = sqla.text("""DELETE FROM public.grad_experiences WHERE netid=:netid;""")
    remove_interests = sqla.text("""DELETE FROM public.grad_interests WHERE netid=:netid;""")
    remove_contact = sqla.text("""DELETE FROM public.grad_contact WHERE netid=:netid;""")
    output = db.execute_command(remove_industries, params)
    output = db.execute_command(remove_experiences, params)
    output = db.execute_command(remove_interests, params)
    output = db.execute_command(remove_contact, params)

    if photo_link is not None and photo_link != '':
         command = sqla.text(
            """UPDATE graduates SET 
            photo_link = :photo WHERE graduates.netid = :netid;""")
         params = {'netid': netid, 'photo': photo_link}
         output = db.execute_command(command, params)

    if experiences is not None:
        if experiences != '':
            for experience, desc in experiences:
                experience_info = {'netid': netid, 'experience': experience,
                                   'experience_desc': desc}
                statement = sqla.text(
                    """INSERT INTO grad_experiences(netid, experience, 
                    experience_desc) VALUES(:netid, :experience, 
                    :experience_desc)""")
                output = db.execute_command(statement, experience_info)

    if industries is not None:
        if industries != '':
            for industry in industries:
                industry_info = {'netid': netid, 'industry': industry}
                statement = sqla.text(
                    """INSERT INTO grad_industries(netid, industry) VALUES(
                    :netid, :industry)""")
                output = db.execute_command(statement, industry_info)

    if interests is not None:
        if interests != '':
            for interest in interests:
                interest_info = {'netid': netid, 'interest': interest}
                statement = sqla.text(
                    """INSERT INTO grad_interests(netid, interest) VALUES(
                    :netid, :interest)""")
                output = db.execute_command(statement, interest_info)

    if email is not None or phone is not None:
        if email != '' or phone != '':
            contact_info = {'netid': netid, 'email': email, 'phone': phone}
            statement = sqla.text(
                """INSERT INTO grad_contact(netid, email, phone) VALUES(:netid, 
                :email, :phone)""")
            output = db.execute_command(statement, contact_info)

def add_a_grad(netid, name, dept, bio=None, un_uni=None, ma_uni=None,
               research_focus=None, expected_grad_date=None,
               years_worked=None, photo_link=None,
               website_link=None, experiences=None, industries=None,
               interests=None, email=None, phone=None):
    """
    Adds a grad to the database in each respective table based on data
    inputted
        netid VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255),
        acad_dept VARCHAR(70),
        bio TEXT,
        undergrad_university TEXT,
        masters_university TEXT,
        research_focus TEXT,
        expected_grad_date VARCHAR(10),
        years_worked INTEGER,
        photo_link TEXT,
        website_link TEXT
    """
    graduates_info = {"netid": netid,
                      "name": name,
                      "acad_dept": dept,
                      "bio": bio,
                      "undergrad_university": un_uni,
                      "masters_university": ma_uni,
                      "research_focus": research_focus,
                      "expected_grad_date": expected_grad_date,
                      "years_worked": years_worked,
                      "photo_link": photo_link,
                      "website_link": website_link}
    statement = sqla.text(
        """INSERT INTO graduates(netid, name, acad_dept, bio, 
        undergrad_university, masters_university, research_focus, 
        expected_grad_date, years_worked, photo_link, website_link) 
        VALUES(:netid, :name, :acad_dept, :bio,
        :undergrad_university, :masters_university, :research_focus,
        :expected_grad_date, :years_worked, :photo_link, :website_link)""")
    output = db.execute_command(statement, graduates_info)

    if experiences is not None:
        if experiences != '':
            for experience, desc in experiences:
                experience_info = {'netid': netid, 'experience': experience,
                                   'experience_desc': desc}
                statement = sqla.text(
                    """INSERT INTO grad_experiences(netid, experience, 
                    experience_desc) VALUES(:netid, :experience, 
                    :experience_desc)""")
                output = db.execute_command(statement, experience_info)

    if industries is not None:
        if industries[0] != '':
            for industry in industries:
                industry_info = {'netid': netid, 'industry': industry}
                statement = sqla.text(
                    """INSERT INTO grad_industries(netid, industry) VALUES(
                    :netid, :industry)""")
                output = db.execute_command(statement, industry_info)

    if interests is not None:
        if interests[0] != '':
            for interest in interests:
                interest_info = {'netid': netid, 'interest': interest}
                statement = sqla.text(
                    """INSERT INTO grad_interests(netid, interest) VALUES(
                    :netid, :interest)""")
                output = db.execute_command(statement, interest_info)

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
        ['grad_contact', 'grad_experiences', 'grad_industries',
         'grad_interests', 'graduates'], net_id)


if __name__ == "__main__":
    print(search_grads())
    # add_a_grad(name = "Henry", dept = "COS", experiences = [("Software Engineering Intern", "Cellanome")], interests = ['Football', 'Basketball'], email = "henryjknoll@gmail.com")
    # del_a_grad(11)
