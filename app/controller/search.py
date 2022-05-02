"""
Henry Knoll, Theo Knoll, Brett Zeligson
GrabAGrad
"""

import model.endpoints as ep

def filter_search(name, dept, industry, years_worked, un_uni, ma_uni, favorites_on, mynetid):
    """
    Search function for if the filter by options are used
    """
    try:
        grad_list = ep.search_grads(name=name, dept=dept.replace('.', ''),
                                    industry=industry,
                                    undergrad_uni=un_uni,
                                    masters_uni=ma_uni,
                                    years_worked=years_worked,
                                    favorites_on=favorites_on,
                                    mynetid=mynetid)
        return "Success", grad_list
    except Exception as ex:
        print(ex)
        return "Server side error occurred, if this problem persists, please contact hknoll@princeton.edu.", []