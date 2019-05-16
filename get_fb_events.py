import os
import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver

#csv to dataframe
df = pd.read_csv('/Users/celarno/Downloads/cat.csv')
df

def _remove_attrs(soup):
    for tag in soup.findAll(True): 
        tag.attrs = None
    return soup


final = {
    'name' : [],
    'events' : []
    }
i=1

for row in df.itertuples(index=True, name='Pandas'):

    venue = getattr(row, "name")
    url = getattr(row, "facebook") + "events/"
    print(i)
    print(venue)
    i=i+1

    browser = webdriver.Chrome()
    browser.get(url)
    r = browser.page_source

    soup = BeautifulSoup(r, "lxml")
    fb_events = soup.find("div", {"id": "pagelet_events"})
    clean_soup = _remove_attrs(fb_events)
    for match in clean_soup.findAll('span'):
        match.unwrap()
    for match in clean_soup.findAll('div'):
        match.unwrap()
    for match in clean_soup.findAll('a'):
        match.unwrap()
    for match in clean_soup.findAll('table'):
        match.unwrap()

    fb_events = clean_soup
    rows = fb_events.find_all('tr')
    data = {
        'date' : [],
        'title' : [],
        'location' : [],
        'guests' : []
        }

    # filling columns
    for row in rows:
        cols = row.find_all('td')
        data['date'].append(cols[0].get_text())
        data['title'].append(cols[1].get_text())
        data['location'].append(cols[2].get_text())
        data['guests'].append(cols[3].get_text())

    events = pd.DataFrame(data)
    events['guests'] = ""
    events['location'] = events.location.apply(lambda x: x[:-8])
    events['guests'] = events.title.str.split('·').str.get(1)
    events['title'] = events.title.str.split('·').str.get(0)
    events.columns.str.strip()
    events.date = events.date.str.extract('(\d+)') + " " + events.date.str[0:3] + " 2018"
    
    final['name'].append(venue)
    final['events'].append(events)

export = pd.DataFrame(final)
out = export.to_json(orient='records')
with open('test.json', 'w') as f:
    f.write(out)





