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
        if self._details[0] is None:
            return ""
        return self._details[0]

    def get_name(self):
        if self._details[1] is None:
            return ""
        return self._details[1]

    def get_first_name(self):
        if self._details[1] is None:
            return ""
        try:
            return self._details[1].split(" ", 1)[0]
        except Exception:
            return ""

    def get_acad_dept(self):
        if self._details[2] is None:
            return ""
        return self._details[2]

    def get_bio(self):
        if self._details[3] is None:
            return ""
        return self._details[3]

    def get_undergrad_university(self):
        if self._details[4] is None:
            return ""
        return self._details[4]

    def get_masters_university(self):
        if self._details[5] is None:
            return ""
        return self._details[5]

    def get_research_focus(self):
        if self._details[6] is None:
            return ""
        return self._details[6]

    def get_expected_grad_date(self):
        if self._details[7] is None:
            return ""
        return self._details[7]

    def get_years_worked(self):
        if self._details[8] is None:
            return ''
        return self._details[8]

    def get_photo_link(self):
        if self._details[9] is None:
            return ""
        return self._details[9]

    def get_website_link(self):
        if self._details[10] is None:
            return ""
        return self._details[10]

    def get_industries(self):
        if self._industries is None:
            return ""
        return self._industries

    def get_industries_str(self):
        try:
            return str.join(', ', self._industries)
        except Exception:
            return ""

    def get_experiences(self):
        if self._experiences is None:
            return ""
        return self._experiences

    def get_interests(self):
        if self._interests is None:
            return ""
        return self._interests

    def get_email(self):
        if self._contact is None:
            return ""
        try:
            return self._contact[0]
        except Exception:
            return ""

    def get_phone(self):
        if self._contact is None:
            return ""
        try:
            return self._contact[1]
        except Exception:
            return ""
