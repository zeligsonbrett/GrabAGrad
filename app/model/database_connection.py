#!/usr/bin/env python

from dotenv import load_dotenv
import os
import sqlalchemy as sqla

def get_uri():
    """
    Loads in the environmental variables to get the database URI
    :return: the database URI
    """
    load_dotenv()
    uri = os.getenv("POSTGRES")
    # Heroku variable provides slightly incorrect connection String
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    return uri

def create_engine():
    """
    Creates an engine linked to the database
    :return: sqlalchemy engine linked to postgresql database
    """
    return sqla.create_engine(get_uri())

def query_all_from_table(engine, table):
    """
    Queries all rows from the table given by parameter table and prints
    each row out
    """
    with engine.connect() as con:
        output = con.execute('SELECT * FROM {}'.format(table))
        print(output.keys())
        for row in output:
            print(row)

def query_all_grads(engine):
    """
    Prints all rows in the 'graduates' table
    """
    query_all_from_table(engine, 'graduates')

def add_a_grad(engine):
    """
    Adds a grad to the 'graduates' table - BETA VERSION
    *Need to add grad information to other tables too*
    """
    with engine.connect() as con:
        graduates_info = ({ "id":           11, 
                            "name":         "Jane Doe SPA", 
                            "acad_dept":    "Spanish", 
                            "bio":          "DELETETHISLATER", 
                            "photo_link":   "later", 
                            "website_link": "later"})
        statement = sqla.text("""INSERT INTO graduates(id, name, acad_dept, bio, photo_link, website_link) VALUES(:id, :name, :acad_dept, :bio, :photo_link, :website_link)""")
        output = con.execute(statement, **new)
        print(output)

def del_a_grad(engine):
    """
    Deletes a grad from the 'graduates' table by ID
    """
    with engine.connect() as con:
        output = con.execute('DELETE FROM graduates WHERE id == 11')
        print(output)


if __name__ == '__main__':
    engine = create_engine()
    #add_a_grad(engine)

    # Different tables so far: ['graduates', 'grad_industries', 'grad_experiences', 'grad_interests', 'grad_contact']
    query_all_grads(engine)

