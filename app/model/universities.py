import requests


def get_universities(name):
    """
    Returns a list of universities beginning with name.
    :param name: The name of a university

    Accesses the University Domains and Names API from Hipo
    Accessible via Github at: https://github.com/Hipo/university-domains-list-api

    :return: List of universities beginning with name
    """
    BASE_URL = 'http://universities.hipolabs.com/search?name='
    search_url = BASE_URL + name
    response = requests.request("GET", search_url).json()
    uni_list = [university['name'] for university in response]
    uni_list.sort()
    return uni_list


if __name__ == "__main__":
    print(get_universities(""))
