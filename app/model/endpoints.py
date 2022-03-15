#!/usr/bin/env python

import pandas as pd
import sqlalchemy as sqla


def query_all_from_table(engine, table):
    """
    Queries all rows from the table given by parameter table and prints
    each row out
    :return: all rows from the table
    """

    query_text = 'SELECT * FROM {}'.format(table)
    output = pd.read_sql(query_text, engine)
    df = pd.DataFrame(output)
    result = df.to_string(index=False)
    print(result)

    # alternative way to do this:
    # with engine.connect() as con:
    #     output = con.execute(query_text)
    return result


def add_a_grad(engine):
    """
    Adds a grad to the 'graduates' table - BETA VERSION
    *Need to add grad information to other tables too*
    """
    with engine.connect() as con:
        graduates_info = ({"id": 11,
                           "name": "Jane Doe SPA",
                           "acad_dept": "Spanish",
                           "bio": "DELETETHISLATER",
                           "photo_link": "later",
                           "website_link": "later"})
        statement = sqla.text(
            """INSERT INTO graduates(id, name, acad_dept, bio, photo_link, website_link) VALUES(:id, :name, :acad_dept, :bio, :photo_link, :website_link)""")
        output = con.execute(statement, **new)
        print(output)


def del_a_grad(engine):
    """
    Deletes a grad from the 'graduates' table by ID
    """
    with engine.connect() as con:
        output = con.execute('DELETE FROM graduates WHERE id == 11')
        print(output)
