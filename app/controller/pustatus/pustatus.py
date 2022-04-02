from controller.pustatus.req_lib import ReqLib

'''
Users endpoint displays following information, when given a netid.
displayname (Full name of the user)
universityid (PUID number)
mail (user's email address)
pustatus (is the user a graduate, undergraduate, or faculty?)
department (which department the user belongs to)
eduPersonPrimaryAffiliation (whether the user is a student or faculty)
streetAddress (office number and location if it is a faculty member)
telephoneNumber (phone number if it is a faculty member)
'''


def is_graduate(netid):
    req_lib = ReqLib()
    print(type(netid))
    req = req_lib.getJSON(
        req_lib.configs.USERS,
        uid=str(netid),
    )
    return req[0]['pustatus'] == 'graduate'
