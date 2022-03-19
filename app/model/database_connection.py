#!/usr/bin/env python

from dotenv import load_dotenv
import os
import sqlalchemy as sqla

engine = None

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
    global engine
    engine = sqla.create_engine(get_uri())

def query_all_from_table(table):
    """
    Queries all rows from the table given by parameter table and prints
    each row out
    """
    with engine.connect() as con:
        output = con.execute('SELECT * FROM {}'.format(table))
        print(output.keys())
        for row in output:
            print(row)

def execute_command(command, params=None):
    output = None
    with engine.connect() as con:
        if params:
            output = con.execute(command, params)
        else:
            ouput = con.execute(command)
        return output

def get_last_id_graduates():
    with engine.connect() as con:
        output = con.execute('SELECT id FROM graduates')
        rows = [x for x in output]
        return rows[-1][0]

def del_id_from_tables(tables, del_id):
    with engine.connect() as con:
        for table in tables:
            statement = 'DELETE FROM ' + table + ' WHERE id = ' + str(del_id)
            con.execute(statement)

engine = sqla.create_engine(get_uri())
