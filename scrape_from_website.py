from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re

def convert_views(views_str):
    if 'K views' in views_str:
        return int(float(views_str.replace('K views', '').replace(',', '')) * 1000)
    elif 'M views' in views_str:
        return int(float(views_str.replace('M views', '').replace(',', '')) * 1000000)
    else:
        return int(views_str.replace(' views', '').replace(',', ''))

def convert_date_to_seconds(date_str):
    match = re.match(r'(\d+) (\w+) ago', date_str)
    if match:
        value, unit = match.groups()
        if unit == 'second' or unit == 'seconds':
            return int(value)
        elif unit == 'minute' or unit == 'minutes':
            return int(value) * 60
        elif unit == 'hour' or unit == 'hours':
            return int(value) * 3600
        elif unit == 'day' or unit == 'days':
            return int(value) * 86400
        elif unit == 'week' or unit == 'weeks':
            return int(value) * 604800
        elif unit == 'month' or unit == 'months':
            return int(value) * 2592000  # Assuming 30 days in a month on average
    return 0

def remove_special_characters(title):
    return " ".join(title.replace('\u2013', '').strip().split())

driver = webdriver.Chrome()
driver.get('https://www.youtube.com/@freecodecamp/videos')
driver.implicitly_wait(5)

site_text = driver.page_source
soup = BeautifulSoup(site_text, 'lxml')
yt_views_and_date_uploaded = soup.find_all(class_='inline-metadata-item style-scope ytd-video-meta-block')
yt_title = soup.find_all(id='video-title')
yt_channel_name = soup.find('yt-formatted-string', class_='style-scope ytd-channel-name')
driver.quit()

titles = []
date_uploaded = []
views = []

for i in range(len(yt_title)):
    titles.append(yt_title[i])

for i in range(len(yt_views_and_date_uploaded)):
    if (i % 2) != 0:
        date_uploaded.append(yt_views_and_date_uploaded[i])
    else:
        views.append(yt_views_and_date_uploaded[i])

titles_text = [title.text for title in titles]
date_uploaded_text = [day.text for day in date_uploaded]
views_text = [view.text for view in views]
channel_name = yt_channel_name.text

# Create a list of dictionaries
video_info = []

# Loop through the lists and create dictionaries for each video
for title, date_uploaded, views in zip(titles_text, date_uploaded_text, views_text):
    date_seconds = convert_date_to_seconds(date_uploaded)
    cleaned_title = remove_special_characters(title)
    video_dict = {
        'title': cleaned_title,
        'date_uploaded': date_uploaded,
        'date_seconds': date_seconds,
        'views': views,
        'views_converted': convert_views(views)
    }
    video_info.append(video_dict)

# Check user for sorting
input_sort = input('Sort Method: Ascending(a)/Descending(d)\n> ').lower()

# Replace the original data with the sorted data
match input_sort:
    case 'ad':
        video_info.sort(key=lambda x: x['date_seconds'])
    case 'av':
        video_info.sort(key=lambda x: x['views_converted'])
    case 'dd':
        video_info.sort(key=lambda x: x['date_seconds'], reverse=True)
    case 'dv':
        video_info.sort(key=lambda x: x['views_converted'], reverse=True)
    case _:
        print('Invalid')

# Create dictionary, prettify
channel_info = {'channel_name': channel_name, 'videos': video_info}
pretty_channel_info = json.dumps(channel_info, indent=4)
print(pretty_channel_info)

# todo: fix months conversion so that it is accurate (collect other data from page)
# todo: add function to scrape multiple pages / scroll pages according to user input