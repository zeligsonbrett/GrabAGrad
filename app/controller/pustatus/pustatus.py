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
    req = req_lib.getJSON(
        req_lib.configs.USERS,
        uid=netid,
    )
    req2 = req_lib.getJSON(
        req_lib.configs.USERS,
        uid="taknoll",
    )
    newVar = "taknoll"
    req3 = req_lib.getJSON(
        req_lib.configs.USERS,
        uid=newVar,
    )
    newNetID = netid
    print(newNetID == newVar)
    req4 = req_lib.getJSON(
        req_lib.configs.USERS,
        uid=newNetID,
    )

    print(req)
    print(req2)
    print(req3)
    print(req4)
    # return req[0]['pustatus'] == 'graduate'
    return True
