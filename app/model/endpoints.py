#!/usr/bin/env python

import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker

# Queries the database and returns a dataframe of the results
def query_all_grads(engine):
    print("This is running")
    query_text = 'SELECT * FROM GRADUATES'
    with engine.connect() as con:
        result = con.execute(query_text)

    # result = pd.read_sql(query_text, engine)
    # print(result)
    result = 'dang'
    return result
