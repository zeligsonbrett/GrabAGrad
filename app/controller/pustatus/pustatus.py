from controller.pustatus.req_lib import ReqLib
import model.database_connection as db
import sqlalchemy as sqla

def _request_users_endpoint(netid):
    """
    Sends request to Princeton's ActiveDirectory API's USERS endpoint.

    Users endpoint displays following information, when given a netid.
    displayname (Full name of the user)
    universityid (PUID number)
    mail (user's email address)
    pustatus (is the user a graduate, undergraduate, or faculty?)
    department (which department the user belongs to)
    eduPersonPrimaryAffiliation (whether the user is a student or faculty)
    streetAddress (office number and location if it is a faculty member)
    telephoneNumber (phone number if it is a faculty member)

    :param netid: The netid to search for in ActiveDirectory.
    :return: A JSON String of the results of the users endpoint.
    """
    try:
        netid = netid.strip()
        req_lib = ReqLib()
        req = req_lib.getJSON(
            req_lib.configs.USERS,
            uid=netid,
        )
        return req[0]
    except Exception as ex:
        print("Exception discovered while attemping ActiveDirectory request:\n", ex)
        return {"pustatus": "unknown"}


def is_graduate(netid):
    """
    Sends request to Princeton's ActiveDirectory API to determine if
    the netid provided corresponds to a graduate student.
    :param netid: The netid of an authenticated user, for use in the
                  API call.
    :return: True if the netid corresponds to a graduate, False if the
             netid doesn't correspond to the graduate or there was an
             error within the database.
    """
    result = _request_users_endpoint(netid)
    try:
        return result['pustatus'] == 'graduate'
    except Exception as ex:
        print("Exception discovered while determining pustatus:\n", ex)
        return False


def is_administrator(netid):
    """
    Determines if the netid corresponds to a GrabAGrad Administrator
    :param netid: The netid of an authenticated user, for use in the
                  API call.
    :return: True if the netid corresponds to an admin, False if the
             netid doesn't correspond to the admin or there was an
             error within the database.
    """
    command = sqla.text("""SELECT netid FROM public.administrators WHERE netid=:netid""")
    params = {'netid': netid}
    output = db.execute_command(command, params)
    ids = [x['netid'] for x in output]
    return len(ids) != 0
