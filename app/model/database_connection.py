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
    # Below comments for loading in environment locally
    # load_dotenv()
    # uri = os.getenv("POSTGRES")

    # The below URI should work in postgres
    try:
        uri = os.environ['DATABASE_URL']
    except:
        uri = "postgres://ruxygftkaufzpd:9ba414b96d4a50d87de47d6984f1cd090cf2318c3579dbcf7a60a52d31133a71@ec2-52-70-186-184.compute-1.amazonaws.com:5432/d3u5tigp9qpsbb"
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
    with engine.connect() as con:
        if params:
            output = con.execute(command, params)
        else:
            output = con.execute(command)
        return output


def get_last_id_graduates():
    with engine.connect() as con:
        output = con.execute('SELECT id FROM graduates')
        rows = [x for x in output]
        if len(rows) == 0:
            return 0
        return rows[-1][0]


def del_id_from_tables(tables, del_id):
    with engine.connect() as con:
        for table in tables:
            statement = 'DELETE FROM ' + table + ' WHERE id = ' + str(
                del_id)
            con.execute(statement)


def __print_query(query_result):
    """
    Takes query_result and prints it to StdOut.
    :param query_result: The resulting output from a query
    """
    print(query_result.keys())
    for row in query_result:
        print(row)


engine = sqla.create_engine(get_uri())

