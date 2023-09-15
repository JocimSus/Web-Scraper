# from https://www.youtube.com/watch?v=XVv6mJpFOb0
from bs4 import BeautifulSoup

class course_dictionary(dict):
    def __init__(self):
        self = dict()
    
    def add(self, key, value):
        self[key] = value

course_dict = course_dictionary()

# Scrape files locally
with open('./html/home.html', 'r') as f:
    content = f.read()

    souped = BeautifulSoup(content, 'lxml')
    course_cards = souped.find_all('div', class_='card')

    for course in course_cards:
        course_text = course.h5.text
        course_price = course.a.text.split()[-1]
        course_dict.add(course_text, course_price)
        print(f'{course_text} costs {course_price}')
    print(course_dict)