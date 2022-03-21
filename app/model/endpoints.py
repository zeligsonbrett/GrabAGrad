#!/usr/bin/env python

import pandas as pd
import sqlalchemy as sqla
import model.database_connection as db


def query_all_grads():
    """
    Queries all graduates
    :return: The id, name, acad_dept, bio, photo_link, and website_link
             of all graduates
    """
    output = db.query_all_from_table('graduates')
    return output


def __prepare_argument(user_input):
    """
    Prepares the user input for use in SQL by adding wildcards
    :return: The user input, prepared for use in an SQL statement
    """
    prepped_arg = '%' + user_input + '%'
    return prepped_arg


def search_grads(name='', dept='', bio='', experience='', industry='',
                 interest=''):
    """
    Search all grads for matches based on search criteria
    :return: id of all matching graduates
    """
    name = __prepare_argument(name)
    dept = __prepare_argument(dept)
    bio = __prepare_argument(bio)
    experience = __prepare_argument(experience)
    industry = __prepare_argument(industry)
    interest = __prepare_argument(interest)

    command = sqla.text(
        'SELECT DISTINCT graduates.id, graduates.name FROM graduates, grad_experiences, grad_industries, grad_interests ' \
        ' WHERE graduates.id = grad_industries.id AND graduates.id = grad_experiences.id AND ' \
        'graduates.id = grad_interests.id AND graduates.name LIKE :name AND graduates.acad_dept LIKE :dept ' \
        'AND graduates.bio LIKE :bio AND grad_experiences.experience LIKE :experience AND grad_industries.industry LIKE :industry AND ' \
        'grad_interests.interest LIKE :interest;')
    params = {'name': name, 'dept': dept, 'bio': bio,
              'experience': experience, 'industry': industry,
              'interest': interest}
    output = db.execute_command(command, params)
    matching_ids = [x[0] for x in output]
    return matching_ids


def get_grad_information(idnum):
    """
    Gets overview information for a certain id number graduate
    """
    command = sqla.text(
        'SELECT * FROM graduates WHERE graduates.id = :id')
    params = {'id': idnum}
    output = db.execute_command(command, params)
    return [x for x in output][0]


def add_a_grad(name=None, dept=None, bio=None, photo_link=None,
               website_link=None, experiences=None, industries=None,
               interests=None, email=None, phone=None):
    """
    Adds a grad to the database in each respective table based on data inputted
    """
    new_id = db.get_last_id_graduates() + 1
    graduates_info = {"id": new_id,
                      "name": name,
                      "acad_dept": dept,
                      "bio": bio,
                      "photo_link": photo_link,
                      "website_link": website_link}
    statement = sqla.text(
        """INSERT INTO graduates(id, name, acad_dept, bio, photo_link, website_link) VALUES(:id, :name, :acad_dept, :bio, :photo_link, :website_link)""")
    output = db.execute_command(statement, graduates_info)

    if experiences is not None:
        for experience, desc in experiences:
            experience_info = {'id': new_id, 'experience': experience,
                               'experience_desc': desc}
            statement = sqla.text(
                """INSERT INTO grad_experiences(id, experience, experience_desc) VALUES(:id, :experience, :experience_desc)""")
            output = db.execute_command(statement, experience_info)

    if industries is not None:
        for industry in industries:
            industry_info = {'id': new_id, 'industry': industry}
            statement = sqla.text(
                """INSERT INTO grad_industries(id, industry) VALUES(:id, :industry)""")
            output = db.execute_command(statement, industry_info)

    if interests is not None:
        for interest in interests:
            interest_info = {'id': new_id, 'interest': interest}
            statement = sqla.text(
                """INSERT INTO grad_interests(id, interest) VALUES(:id, :interest)""")
            output = db.execute_command(statement, interest_info)

    if email is not None or phone is not None:
        contact_info = {'id': new_id, 'email': email, 'phone': phone}
        statement = sqla.text(
            """INSERT INTO grad_contact(id, email, phone) VALUES(:id, :email, :phone)""")
        output = db.execute_command(statement, contact_info)


def del_a_grad(del_id):
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
    print("")
    # search_grads(name='John')
    # add_a_grad(name = "Henry", dept = "COS", experiences = [("Software Engineering Intern", "Cellanome")], interests = ['Football', 'Basketball'], email = "henryjknoll@gmail.com")
    # del_a_grad(11)
