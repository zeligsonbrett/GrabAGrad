def dept_list():
    """
    :return: List of all graduate departments at Princeton. Updated April 2022.
    """
    departments = [
        "Anthropology", "Applied and Computational Math",
        "Art and Archaeology", "Astrophysical Sciences",
        "Atmospheric and Ocean Sciences",
        "Chemical and Biological Engineering", "Chemistry",
        "Civil and Environmental Engineering", "Classics",
        "Comparative Literature", "Computer Science",
        "East Asian Studies", "Ecology and Evolutionary Biology",
        "Economics", "Electrical and Computer Engineering",
        "English", "Finance", "French and Italian", "Geosciences",
        "German", "History", "History of Science", "Mathematics",
        "Mechanical and Aerospace Engineering", "Molecular Biology",
        "Music Composition", "Musicology", "Near Eastern Studies",
        "Neuroscience", "Operations Research and Financial Engineering",
        "Philosophy", "Physics", "Plasma Physics", "Politics",
        "Population Studies",
        "Princeton School of Public and International Affairs",
        "Psychology", "Quantitative and Computational Biology",
        "Religion", "Slavic Languages and Literatures", "Sociology",
        "Spanish and Portuguese"
    ]

    return departments

def abbreviation(input_abbrev):
    """
    :return: The acronym for input_abbrev, None if it doesn't have one
    """
    abbreviations = abbreviations_dict()
    if input_abbrev in abbreviations:
        return abbreviations[input_abbrev]
    return None

def abbreviations_dict():
    """
    :return: Dictionary where each department key has its acronym as its value
    """
    abbreviations = {"Atmospheric and Ocean Sciences": "AOS",
                    "Chemical and Biological Engineering": "CBE",
                    "Civil and Environmental Engineering": "CEE",
                    "Computer Science": "COS",
                    "Ecology and Evolutionary Biology": "EEB",
                    "Mechanical and Aerospace Engineering": "MAE",
                    "Operations Research and Financial Engineering": "ORFE",
                    "Princeton School of Public and International Affairs": "SPIA",
                    "Quantitative and Computational Biology": "QCB"}
    return abbreviations
