#!/usr/bin/env python

class Graduate:
    """
    Graduate objects represent graduate students and their relevant
    data fields.
    """

    def __init__(self, details=None, industries=None, experiences=None,
                 interests=None, contact=None):
        if details is None:
            details = [None] * 11
        self._details = details
        self._industries = industries
        self._experiences = experiences
        self._interests = interests
        self._contact = contact

    def get_grad_id(self):
        return self._details[0]

    def get_name(self):
        return self._details[1]

    def get_first_name(self):
        return self._details[1].split(" ", 1)[0]

    def get_acad_dept(self):
        return self._details[2]

    def get_bio(self):
        return self._details[3]

    def get_undergrad_university(self):
        return self._details[4]

    def get_masters_university(self):
        return self._details[5]

    def get_research_focus(self):
        return self._details[6]

    def get_expected_grad_date(self):
        return self._details[7]

    def get_years_worked(self):
        if self._details[8] is None:
            return ''
        return self._details[8]

    def get_photo_link(self):
        return self._details[9]

    def get_website_link(self):
        return self._details[10]

    def get_industries(self):
        return self._industries

    def get_industries_str(self):
        return str.join(', ', self._industries)

    def get_experiences(self):
        return self._experiences

    def get_interests(self):
        return self._interests

    def get_contact(self):
        return self._contact
