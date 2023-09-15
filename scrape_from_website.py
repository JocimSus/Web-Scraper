from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.youtube.com/@freecodecamp/videos')
driver.implicitly_wait(5)

site_text = driver.page_source
soup = BeautifulSoup(site_text, 'lxml')
yt_views_and_date_uploaded = soup.find_all(class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
yt_title = soup.find_all(id='video-title')

titles = []
date_uploaded = []
views = []

for i in range(len(yt_title)):
    titles.append(yt_title[i])

for i in range(len(yt_views_and_date_uploaded)):
    if (i % 2) != 0:
        views.append(yt_views_and_date_uploaded[i])
    else:
        date_uploaded.append(yt_views_and_date_uploaded[i])

titles_text = [title.text for title in titles]
date_uploaded_text = [day.text for day in date_uploaded]
views_text = [view.text for view in views]

# OPTIMIZED CODE ABOVE (list comprehension)
# date_uploaded_text = []
# views_text = []
# titles_text = []

# for title in titles:
#     title_text = title.text
#     titles_text.append(title_text)
# for day in date_uploaded:
#     day_text = day.text
#     date_uploaded_text.append(day_text)
# for view in views:
#     view_text = view.text
#     views_text.append(view_text)
# OPTIMIZED CODE ABOVE (list comprehension)

print(titles_text)
print(date_uploaded_text)
print(views_text)

driver.quit()

# todo: create a dictionary and insert an object with the properties: 'title', 'views', 'date_uploaded' with the values from the code above