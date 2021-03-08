import pickle
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
import json

prefix = '.*org-people-bar-graph-module__.*'
reList = ['geo-region', 'organization', 'current-function',
          'field-of-study', 'skill-explicit']
keys = ['region', 'company', 'function', 'major', 'skill']
stop_words = ['Where they live', 'Where they work', 'What they do',
              'What they studied', 'What they are skilled at', 'Add']


schoolUrls = pd.read_csv('data/linkedin_schools_demo.csv',usecols = ['INSTNM.1', 'Alumni URL'])
schoolUrls = schoolUrls.rename(columns = {'INSTNM.1':'name', 'Alumni URL':'url'})

## change the index
top = schoolUrls.iloc[:2,]

alumniData = {}

for _, row in top.iterrows():
    name = row['name']
    name = name.replace('/', '_')
    url = row['url']
    with open(f'geo/{name}.pickle', 'rb') as f:
        page = pickle.load(f)

    alumniData[name] = {}
    ks = list(page.keys())

    for j in range(len(page)): 
        p = page[ks[j]]
        soup = bs(p, 'html.parser')

        geo = soup.find_all(class_ = 'org-people-bar-graph-element mt4 org-people-bar-graph-element--is-selectable org-people-bar-graph-element--is-selected ember-view')[0]
        geo = geo.find_all(class_ = 'org-people-bar-graph-element__category')[0].text
        result = {}

        for i in range(1,5):
            className = prefix + reList[i]
            classHtml = soup.find_all(class_ = re.compile(className))
            cleanList = [g.text.strip() for g in classHtml][0]
            cleanList = [g.strip() for g in cleanList.split("\n") if g.strip() != '']
            cleanList = [g for g in cleanList if g not in stop_words]
        #     alumniNum = int(soup.find('span', 't-20 t-black').text.strip().split(' ')[0].replace(',',''))
            cleanList = [ {'name':c.split(' ', 1)[1], 'count':c.split(' ', 1)[0]} for c in cleanList ]

            result[keys[i]] = cleanList
        #     result['alumni_num'] = alumniNum
        alumniData[name][geo] = result


# store all data in json
with open('alumniData.json', 'w') as jf:
    json.dump(alumniData, jf)


# count employers
company_all = {}
company_occurence = {}

for _, row in top.iterrows():
    name = row['name']
    name = name.replace('/', '_')
    url = row['url']
    
    d = alumniData[name]
    
    for k, v in d.items():
        if k != 'United States':
            company = v['company']
            for c in company:
                if c['name'] in company_all:
                    company_all[c['name']] += int(c['count'].replace(',',''))
                    company_occurence[c['name']] += 1
                else:
                    company_all[c['name']] = int(c['count'].replace(',',''))
                    company_occurence[c['name']] = 1

c_count = pd.DataFrame.from_dict(company_all, orient = 'index')

c_times = pd.DataFrame.from_dict(company_occurence, orient = 'index')\
    .rename(columns = {0:'appearance'})

c_count.join(c_times)\
    .reset_index()\
    .rename(columns = {'index':'Company Name', 0:'Total Counts', 'appearance':'Total Appearance'})\
    .sort_values(by = 'Total Counts', ascending = False)\
    .to_csv('top_200.csv')


# flatten the json data
cols = ['school', 'region']
for k in keys[1:]:
    for i in range(1,16):
        cols.append(f'{k}_{i}_name')
        cols.append(f'{k}_{i}_count')

df = pd.DataFrame(columns = cols)
d = {}
idx = 0
for school_name, d_school in alumniData.items():
    for region, d_region in d_school.items():
        d['school'] = school_name
        d['region'] = region
        for k in keys[1:]:  
            for i in range(1,16):
                try:  
                    d[f'{k}_{i}_name'] = d_region[k][i-1]['name']
                    d[f'{k}_{i}_count'] = d_region[k][i-1]['count']
                except:
                    d[f'{k}_{i}_name'] = ''
                    d[f'{k}_{i}_count'] = ''
        df = df.append(d, ignore_index = True)
    print(f'{idx} : {school_name}')
    idx += 1

df.to_csv('alumniData.csv')


print("All finished.")