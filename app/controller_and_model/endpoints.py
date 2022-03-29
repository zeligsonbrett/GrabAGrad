#!/usr/bin/env python

import sqlalchemy as sqla
import database_connection as db
from graduate import Graduate


def query_all_grads():
    """
    Query all grads in the database
    :return: Graduate object for all graduates in the database
    """

    command = sqla.text('SELECT * FROM graduates')

    output = db.execute_command(command)
    details_list = [
        [x['id'], x['name'], x['acad_dept'], x['bio'],
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
    :return: String of all fields of Graduate details, including id,
    name, acad_dept, bio, undergrad_university, masters_university,
    research_focus, expected_grad_date, years_worked, photo_link,
    website_link
    """
    details_string = """graduates.id, graduates.name, 
    graduates.acad_dept, graduates.bio, 
    graduates.undergrad_university, graduates.masters_university, 
    graduates.research_focus, graduates.expected_grad_date, 
    graduates.years_worked, graduates.photo_link, graduates.website_link
    """
    return details_string


def __id_string(id_list):
    """
    Returns a String WHERE clause to only search for ids that appear in
    id_list
    :return: WHERE id IN ( ... )
    """
    if len(id_list) > 0:
        id_string = ', '.join(map(str, id_list))
        return 'WHERE id IN ( {} )'.format(id_string)
    else:
        return ''


def __prepare_argument(user_input):
    """
    Prepares the user input for use in SQL by adding wildcards
    :return: The user input, prepared for use in an SQL statement
    """
    prepped_arg = '%' + user_input + '%'
    return prepped_arg


def __create_graduates_list(id_list):
    """
    Creates and returns a list of graduates that have ids from id_list.
    In doing so, retrieves information about details, industries,
    experiences, interests, and contact information.
    Note, this currently queries pretty inefficiently to create the
    industry, experiences, interest, and contact attributes of a grad
    :param id_list: A list of id's corresponding to graduates in the
                    database.
    :return: A list of Graduate objects corresponding with ids from
             id_list
    """
    details_command = sqla.text("""SELECT {} FROM graduates {} 
        ORDER BY id""".format(__details_string(), __id_string(id_list)))
    details_output = db.execute_command(details_command)
    details_list = [
        [x['id'], x['name'], x['acad_dept'], x['bio'],
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
                                   grad_industries WHERE id =
                                   {}""".format(row[0]))
        industry_output = db.execute_command(industries_command)
        row_industries = [x['industry'] for x in industry_output]
        industry_list.append(row_industries)

        experiences_command = sqla.text("""SELECT DISTINCT experience 
                                    FROM grad_experiences WHERE id = 
                                    {}""".format(row[0]))
        experiences_output = db.execute_command(experiences_command)
        row_experiences = [x['experience'] for x in experiences_output]
        experiences_list.append(row_experiences)

        interests_command = sqla.text("""SELECT DISTINCT interest 
                                  FROM grad_interests WHERE id = 
                                  {}""".format(row[0]))
        interests_output = db.execute_command(interests_command)
        row_interests = [x['interest'] for x in interests_output]
        interests_list.append(row_interests)

        contacts_command = sqla.text("""SELECT email, phone
                                          FROM grad_contact WHERE id = 
                                          {}""".format(row[0]))
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


# Based on Henry's valid search fields from search.py
def search_grads(name='', dept='', research='', grad_year='',
                 undergrad_uni='', masters_uni='', years_worked=None,
                 industry=''):
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
    industry = __prepare_argument(industry)

    if years_worked is None:
        years_worked_c = ''
    else:
        years_worked_c = 'AND years_worked = {}'.format(years_worked)

    command = sqla.text(
        """SELECT DISTINCT graduates.id FROM 
        graduates, grad_industries
        WHERE graduates.id = grad_industries.id AND name LIKE :name AND 
        acad_dept LIKE :dept AND research_focus LIKE :research AND 
        undergrad_university LIKE :undergrad_uni AND masters_university
        LIKE :masters_uni AND expected_grad_date LIKE :grad_year {} AND
        industry LIKE :industry ORDER BY graduates.id
        ASC;""".format(years_worked_c))
    params = {'name': name, 'dept': dept, 'research': research,
              'undergrad_uni': undergrad_uni, 'grad_year':grad_year,
              'masters_uni': masters_uni, 'years_worked': years_worked,
              'industry': industry}
    output = db.execute_command(command, params)
    ids = [x['id'] for x in output]
    grad_list = __create_graduates_list(ids)

    return grad_list


def get_grad_information(idnum):
    """
    Gets overview information for a certain id number graduate
    """
    command = sqla.text(
        'SELECT * FROM graduates WHERE graduates.id = :id')
    params = {'id': idnum}
    output = db.execute_command(command, params)
    return [x for x in output][0]


def add_a_grad(name, dept, bio=None, un_uni=None, ma_uni=None,
               research_focus=None, expected_grad_date=None,
               years_worked=None, photo_link=None,
               website_link=None, experiences=None, industries=None,
               interests=None, email=None, phone=None):
    """
    Adds a grad to the database in each respective table based on data
    inputted
        id SERIAL PRIMARY KEY,
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
    new_id = db.get_last_id_graduates() + 1
    graduates_info = {"id": new_id,
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
        """INSERT INTO graduates(id, name, acad_dept, bio, 
        undergrad_university, masters_university, research_focus, 
        expected_grad_date, years_worked, photo_link, website_link) 
        VALUES(:id, :name, :acad_dept, :bio,
        :undergrad_university, :masters_university, :research_focus,
        :expected_grad_date, :years_worked, :photo_link, :website_link)""")
    output = db.execute_command(statement, graduates_info)

    if experiences is not None:
        for experience, desc in experiences:
            experience_info = {'id': new_id, 'experience': experience,
                               'experience_desc': desc}
            statement = sqla.text(
                """INSERT INTO grad_experiences(id, experience, 
                experience_desc) VALUES(:id, :experience, 
                :experience_desc)""")
            output = db.execute_command(statement, experience_info)

    if industries is not None:
        for industry in industries:
            industry_info = {'id': new_id, 'industry': industry}
            statement = sqla.text(
                """INSERT INTO grad_industries(id, industry) VALUES(
                :id, :industry)""")
            output = db.execute_command(statement, industry_info)

    if interests is not None:
        for interest in interests:
            interest_info = {'id': new_id, 'interest': interest}
            statement = sqla.text(
                """INSERT INTO grad_interests(id, interest) VALUES(
                :id, :interest)""")
            output = db.execute_command(statement, interest_info)

    if email is not None or phone is not None:
        contact_info = {'id': new_id, 'email': email, 'phone': phone}
        statement = sqla.text(
            """INSERT INTO grad_contact(id, email, phone) VALUES(:id, 
            :email, :phone)""")
        output = db.execute_command(statement, contact_info)


def delete_grad(del_id):
    """
    Deletes all rows corresponding to id from the graduate tables
    """
    # param = {'id': id}
    # statement = 'DELETE graduates, grad_contact, grad_experiences, grad_industries, grad_interests FROM graduates INNER JOIN grad_contact INNER JOIN grad_experiences INNER JOIN grad_industries INNER JOIN grad_interests ON graduates.id = :id AND grad_contact.id = :id AND grad_experiences = :id AND grad_industries = :id AND grad_interests = :id'
    # output = db.execute_command(statement, param)
    db.del_id_from_tables(
        ['grad_contact', 'grad_experiences', 'grad_industries',
         'grad_interests', 'graduates'], del_id)


if __name__ == "__main__":
    print(search_grads())

    # add_a_grad(name = "Henry", dept = "COS", experiences = [("Software Engineering Intern", "Cellanome")], interests = ['Football', 'Basketball'], email = "henryjknoll@gmail.com")
    # del_a_grad(11)
