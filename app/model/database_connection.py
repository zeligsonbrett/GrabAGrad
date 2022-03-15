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
    print(get_uri())
    return sqla.create_engine(get_uri())

#     Different tables so far: ['graduates', 'grad_industries',
#     'grad_experiences', 'grad_interests', 'grad_contact']
