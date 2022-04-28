import model.endpoints as ep

# sample_search_bar_input = 'name:"Austin Wang,  Cedrick Argueta,Henry Knoll   " name:"Henry Knoll" department:"Computer Science" undergraduate_university:"Princeton, Stanford"'
'''
VALID_SEARCH_FIELDS = ['name', 'department', 'research', 'grad_year',
                       'industry', 'undergraduate_university',
                       'masters_university', 'years_worked']
'''
'''
def search(search_input):
    try:
        return "Success", search_grads(
            parse_search_bar_input(search_input))
    except Exception as ex:
        print(ex)
        return "Error occurred when searching, make sure search input is valid", []
'''

def filter_search(name, dept, industry, years_worked, un_uni, ma_uni, favorites_on, mynetid):
    """
    Search function for if the filter by options are used.
    """
    try:
        grad_list = ep.search_grads(name=name, dept=dept,
                                    industry=industry,
                                    undergrad_uni=un_uni,
                                    masters_uni=ma_uni,
                                    years_worked=years_worked,
                                    favorites_on=favorites_on,
                                    mynetid=mynetid)
        return "Success", grad_list
    except Exception as ex:
        print(ex)
        return "Error occurred when searching, make sure filter input is valid", []

'''
def parse_search_bar_input(search_input):
    query = {}
    input_fields = search_input.split('" ')
    for input_field in input_fields:
        field_name, field_value = input_field.split(':"', 1)

        if field_name.lower() not in VALID_SEARCH_FIELDS:
            raise Exception('Unknown field in query: ' + field_name)
        if field_name in query:
            raise Exception('Duplicate values for field: ' + field_name)

        field_value = field_value.replace('"', "").lower()
        query[field_name] = field_value
    return query


def search_grads(query):
    grad_list = []
    name = department = research = grad_year = industry = undergraduate_university = masters_university = years_worked = None
    if 'name' in query:
        name = query['name']
    if 'department' in query:
        department = query['department']
    if 'research' in query:
        research = query['research']
    if 'grad_year' in query:
        grad_year = query['grad_year']
    if 'industry' in query:
        industry = query['industry']
    if 'undergraduate_university' in query:
        undergraduate_university = query['undergraduate_university']
    if 'masters_university' in query:
        masters_university = query['masters_university']
    if 'years_worked' in query:
        years_worked = query['years_worked']

    grad_list.extend(
        ep.search_grads(name=name, dept=department, research=research,
                        grad_year=grad_year, industry=industry,
                        undergrad_uni=undergraduate_university,
                        masters_uni=masters_university,
                        years_worked=years_worked))
    return grad_list


def parse_search_bar_input_complex(search_input):
    query = {}
    input_fields = search_input.split('" ')
    for input_field in input_fields:
        field_name, field_value = input_field.split(':"', 1)

        if field_name not in VALID_SEARCH_FIELDS:
            raise Exception('Unknown field in query: ' + field_name)

        field_values = list(
            map(str.strip, field_value.replace('"', "").split(',')))
        if field_name in query:
            query[field_name].extend(field_values)
        else:
            query[field_name] = field_values
    return query


def search_grads_complex(query):
    grad_list = []
    name = department = research = grad_year = industry = undergraduate_university = masters_university = years_worked = None
    if 'name' in query:
        name = query['name']
    if 'department' in query:
        department = query['department']
    if 'research' in query:
        research = query['research']
    if 'grad_year' in query:
        grad_year = query['grad_year']
    if 'industry' in query:
        industry = query['industry']
    if 'undergraduate_university' in query:
        undergraduate_university = query['undergraduate_university']
    if 'masters_university' in query:
        masters_university = query['masters_university']
    if 'years_worked' in query:
        years_worked = query['years_worked']

    grad_list.extend(
        ep.search_grads(name=name, dept=department, research=research,
                        grad_year=grad_year, industry=industry,
                        undergrad_uni=undergraduate_university,
                        masters_uni=masters_university,
                        years_worked=years_worked))
    return grad_list
'''
