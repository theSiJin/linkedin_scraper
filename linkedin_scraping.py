from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re
import pickle
import random
import os

def pause():
    time_break = random.randint(3,8)
    return time.sleep(time_break)


def get_page(start, end):
    segment = schoolUrls.iloc[start:end,]

    for idx, row in segment.iterrows():
        name = row['name']
        # avoid file path issue
        name = name.replace('/', '_')
        url = row['url']
        
        try:
            driver.get(url)

            pause()

            # show more
            showMore = driver.find_element_by_css_selector('.org-people__show-more-button.t-16.t-16--open.t-black--light.t-bold')
            driver.execute_script('arguments[0].scrollIntoView(false)', showMore)
            showMore.click()

            page_by_geo = {}
            for i in range(1,15):
                try:
                    fltr = driver.find_element_by_css_selector(f'.org-people-bar-graph-element__percentage-bar.org-people-bar-graph-module__geo-region--{i}')
                    driver.execute_script('arguments[0].scrollIntoView(false)', fltr)

                    fltr.click()
                    pause()

                    page = driver.page_source
                    soup = bs(page, 'html.parser')
                    page_by_geo[i] = str(soup)

                    fltrClear = driver.find_element_by_css_selector('.artdeco-pill.artdeco-pill--blue.artdeco-pill--3.artdeco-pill--dismiss.artdeco-pill--selected.ember-view')
                    driver.execute_script('arguments[0].scrollIntoView(false)', fltrClear)
                    fltrClear.click()

                    pause()
                except:
    #                 print(f'fail: {name}, {i}')
                    break

            if not os.path.exists('geo'):
                os.makedirs('geo')

            with open(f'geo/{name}.pickle', 'wb') as handle:
                pickle.dump(page_by_geo, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print(f'{idx} - {name} : saved')

        except:
            print(f'{idx} - {name} : failed to open url')
        
        time.sleep(2)


# LinkedIn profile
## fill in before running the program ##
username = ''
password = ''
if not os.path.exists('geo'):
    os.makedirs('geo')
# load the college dataframe
schoolUrls = pd.read_csv('data/linkedin_schools_demo.csv',usecols = ['INSTNM.1', 'Alumni URL'])
schoolUrls = schoolUrls.rename(columns = {'INSTNM.1':'name', 'Alumni URL':'url'})

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/school/Alverno-College/people/')
pause()

user = driver.find_element_by_id('username')
user.clear()
user.send_keys(username)

pw = driver.find_element_by_id('password')
pw.clear()
pw.send_keys(password)

try:
    submit = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[4]/button')
except:
    submit = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')
    submit.click()
else:
    driver.quit()
    print('failed to log in.')


get_page(0, 2)
driver.quit()