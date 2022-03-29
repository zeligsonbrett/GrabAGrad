import pandas as pd
import endpoints as ep

graduates = pd.read_csv("/Users/henryknoll/Downloads/Speedy GrabAGrad Graduate Student Information Form (Responses) - Form Responses 1.csv")
"""Index(['Timestamp', 'Email Address', 'Name (First Last)',
       'Academic Department (choose "Other" if none apply)',
       'Current research focus (1-2 sentences)', 'Current year of grad school',
       'Expected graduation year', 'Years of work experience',
       'Industries you have worked in or plan to work in',
       'Undergraduate institution and major (Ex: Princeton, Computer Science)',
       'Masters institution and subject area (Ex: MIT Sloan, Business)',
       'Are you okay with your information being displayed on our web application? ',
       'Preferred contact email', 'Preferred phone number',
       'Profile photo, headshot preferred',
       'Questions, comments or concerns about our app or this form'],
      dtype='object')"""

name = 'Name (First Last)'
email = 'Email Address'
acad_dept = 'Academic Department (choose "Other" if none apply)'
research_focus = 'Current research focus (1-2 sentences)'
expected_grad_date = 'Expected graduation year'
industries = 'Industries you have worked in or plan to work in'
undergraduate = 'Undergraduate institution and major (Ex: Princeton, Computer Science)'
masters = 'Masters institution and subject area (Ex: MIT Sloan, Business)'
years_worked = 'Years of work experience'
photo_link = 'Profile photo, headshot preferred'

graduates = graduates.loc[graduates['Are you okay with your information being displayed on our web application? '] == 'Yes']

for i in range(1, 12):
    ep.delete_grad(i)


for index, row in graduates.iterrows():
    #print(row)
    if not pd.isna(row[industries]):
        grad_industries = row[industries].split(', ')
        ep.add_a_grad(name=row[name], dept=row[acad_dept], bio=None, un_uni=row[undergraduate], ma_uni=row[masters],
               research_focus=row[research_focus], expected_grad_date=row[expected_grad_date],
               years_worked=row[years_worked], photo_link=row[photo_link],
               website_link=None, experiences=None, industries=grad_industries,
               interests=None, email=row[email], phone=None)

