import pandas as pd
import datetime
import re
import vincent
from elasticsearch import Elasticsearch

es = Elasticsearch([
    {'host': 'ops.digiman.us', 'port': '9200'}
])

# get each date from 1 week previous to today until today
date_array = []
for i in range(1):
    date_array.append(datetime.date.today() - datetime.timedelta(days=i))

# format each date in date array
for i in range(len(date_array)):
    date_array[i] = 'logstash-' + str(date_array[i].strftime("%Y.%m.%d"))


source_data = es.search(index=date_array,
                        doc_type='syslog',
                        body={"query": {"match_all": {}},
                              "from": 0,
                              "size": 50000})


def get_title(title_string):
    """reformat the requests data to return only the string for title."""

    m = re.search('(?<=/docs/available_locales/)\w+', title_string)
    n = re.search('(?<=/docs/search/)\w+', title_string)
    o = re.search('(?<=/docs/toc/)\w+', title_string)
    if m:
        title = m.group()
    elif n:
        title = n.group()
    elif o:
        title = o.group()
    else:
        title = 'n/a'
    return title


def get_chapter(chapter_string):
    """reformat the requests data to return only the string for chapter."""

    m = re.search('(?<=/docs/)(available_locales)(?=/)', chapter_string)
    n = re.search('(?<=/docs/)(search)(?=/)', chapter_string)
    o = re.search('(?<=/docs/)(toc)(?=/)', chapter_string)
    p = re.search('(?<=chapter=)\d', chapter_string)

    if m:
        chapter = m.group()
    elif n:
        chapter = n.group()
    elif o:
        chapter = o.group()
    elif p:
        chapter = p.group()
    else:
        chapter = 'n/a'
    return chapter


def get_locale(locale_string):
    """parse the requests data to return only the string for locale."""

    m = re.search('(?<=locale=)\w+', locale_string)
    if m:
        locale = m.group()
    else:
        locale = 'n/a'
    return locale


def get_platform(platform_string):
    """parse the requests data to return only the string for platform"""

    m = re.search('ps4', platform_string)
    n = re.search('psvita', platform_string)
    if m:
        platform = m.group()
    elif n:
        platform = n.group()
    else:
        platform = 'n/a'
    return platform

data_array = []
for i in range(len(source_data['hits']['hits'])):
    if get_title(source_data['hits']['hits'][i]
                 ['_source']['message']) != 'n/a':
        data_title = get_title(source_data['hits']['hits'][i]
                               ['_source']['message'])
        data_location = get_locale(source_data['hits']['hits'][i]
                                   ['_source']['message'])
        data_chapter = get_chapter(source_data['hits']['hits'][i]
                                   ['_source']['message'])
        data_array.append({'title': data_title, 'location': data_location,
                           'chapter': data_chapter})

source_df = pd.DataFrame(data_array)

title_grouped = source_df.groupby('title').size()
print(title_grouped)
title_pie = vincent.Pie(title_grouped)
title_pie.legend(title='Hits per Game Title')
title_bar = vincent.Bar(title_grouped)
title_bar.legend(title='Hits per Game Title')

title_pie.to_json('title_vis.json')
title_bar.to_json('title_pie.json')
