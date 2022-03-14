#!/usr/bin/env python

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine


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


def connect_engine():
    """
    Creates an engine linked to the database
    :return: sqlalchemy engine linked to postgresql database
    """
    return create_engine(get_uri())

