#!/usr/bin/env python

"""
Henry Knoll, Theo Knoll, Brett Zeligson
GrabAGrad
"""

from dotenv import load_dotenv
import os
import sqlalchemy as sqla

engine = None

def get_uri():
    """
    Loads in the environmental variables to get the database URI
    :return: the database URI
    """
    # Below comments for loading in environment locally
    # load_dotenv()
    # uri = os.getenv("POSTGRES")

    # The below URI should work in postgres
    try:
        uri = os.environ['DATABASE_URL']
    except:
        from controller.keys import DATABASE_URI
        uri = DATABASE_URI
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
        return output


def execute_command(command, params=None):
    """
    Executes a command with given parameters
    """
    with engine.connect() as con:
        if params:
            output = con.execute(command, params)
        else:
            output = con.execute(command)
        return output


def del_id_from_tables(tables, del_id):
    """
    Deletes the primary key del_id from each table in order of how they are listed in tables
    """
    with engine.connect() as con:
        for table in tables:
            statement = "DELETE FROM {} WHERE netid = '{}'".format(table, str(del_id))
            con.execute(statement)


def __print_query(query_result):
    """
    Takes query_result and prints it to StdOut.
    :param query_result: The resulting output from a query
    """
    print(query_result.keys())
    for row in query_result:
        print(row)

# Creates the engine when the module is loaded
engine = sqla.create_engine(get_uri())

