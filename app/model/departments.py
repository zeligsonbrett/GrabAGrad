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
    abbreviations = abbreviations_dict()
    if input_abbrev in abbreviations:
        return abbreviations[input_abbrev]
    return None

def abbreviations_dict():
    """
    :return: List of all graduate department abbreviations at Princeton. Updated April 2022.
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

def mapping_dict():
    """
    :return: Dictionary mapping abbreviations and non-abbreviations to their major
    """
    abbreviations = {"AOS": "Atmospheric and Ocean Sciences",
                    "CBE": "Chemical and Biological Engineering",
                    "CEE": "Civil and Environmental Engineering",
                    "COS": "Computer Science",
                    "EEB": "Ecology and Evolutionary Biology",
                    "MAE": "Mechanical and Aerospace Engineering",
                    "ORFE": "Operations Research and Financial Engineering",
                    "SPIA": "Princeton School of Public and International Affairs",
                    "QCB": "Quantitative and Computational Biology",
                    "Anthropology": "Anthropology",
                    "Applied and Computational Math": "Applied and Computational Math",
                    "Art and Archaeology": "Art and Archaeology", 
                    "Astrophysical Sciences": "Astrophysical Sciences",
                    "Atmospheric and Ocean Sciences": "Atmospheric and Ocean Sciences",
                    "Chemical and Biological Engineering": "Chemical and Biological Engineering", 
                    "Chemistry": "Chemistry",
                    "Civil and Environmental Engineering": "Civil and Environmental Engineering", 
                    "Classics": "Classics",
                    "Comparative Literature": "Comparative Literature", 
                    "Computer Science": "Computer Science",
                    "East Asian Studies": "East Asian Studies", 
                    "Ecology and Evolutionary Biology": "Ecology and Evolutionary Biology",
                    "Economics": "Economics", 
                    "Electrical and Computer Engineering": "Electrical and Computer Engineering",
                    "English": "English", 
                    "Finance": "Finance", 
                    "French and Italian": "French and Italian", 
                    "Geosciences": "Geosciences",
                    "German": "German", 
                    "History": "History", 
                    "History of Science": "History of Science", 
                    "Mathematics": "Mathematics",
                    "Mechanical and Aerospace Engineering": "Mechanical and Aerospace Engineering", 
                    "Molecular Biology": "Molecular Biology",
                    "Music Composition": "Music Composition", 
                    "Musicology": "Musicology",
                    "Near Eastern Studies": "Near Eastern Studies",
                    "Neuroscience": "Neuroscience", 
                    "Operations Research and Financial Engineering": "Operations Research and Financial Engineering",
                    "Philosophy": "Philosophy", 
                    "Physics": "Physics", 
                    "Plasma Physics": "Plasma Physics", 
                    "Politics": "Politics",
                    "Population Studies": "Population Studies",
                    "Princeton School of Public and International Affairs": "Princeton School of Public and International Affairs",
                    "Psychology": "Psychology", 
                    "Quantitative and Computational Biology": "Quantitative and Computational Biology",
                    "Religion": "Religion", 
                    "Slavic Languages and Literatures": "Slavic Languages and Literatures", 
                    "Sociology": "Sociology",
                    "Spanish and Portuguese": "Spanish and Portuguese"}
    return abbreviations




