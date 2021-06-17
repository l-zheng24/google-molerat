from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
import requests
import pandas as pd


def search(query, num_results=50, lang='en', timerange=None):
    '''Return a dataframe containing Google search results

    Keyword arguments:
    query -- search parameters (string)
    num_results -- the number of results to search (int)
    lang -- language code (string)
    timerange -- tuple containing two years to search between.
                    if none, then no query for year is made

    '''
    root = 'https://www.google.com/search?q='
    search = quote_plus(query)
    if timerange:
        begin = min(timerange)
        end = max(timerange)
        timestring = f'&tbs=cdr%3A1%2Ccd_min%3A{begin}%2Ccd_max%3A{end}'
    else:
        timestring = ''
    link = f'{root}{search}&num={str(num_results)}&hl={lang}{timestring}'
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.100 Safari/537.36'
    }
    req = Request(link, headers=usr_agent)
    webpage = urlopen(req).read()
    return get_data(BeautifulSoup(webpage, 'html.parser'))


def get_data(soup):
    ''' Return a dataframe containing parsed search results

    Keyword arguments:
    soup -- a bs4 soup object representing the Google page

    '''
    result_block = soup.find_all('div', attrs={'class': 'g'})
    df_dict = {
        "Title": [],
        "Description": [],
        "Link": []
    }
    for result in result_block:
        if(len(result['class']) != 1):
            continue
        link = result.find('a', href=True)
        title = result.find('h3')
        desc = result.find('span', attrs={'class': None})
        if link and title and desc:
            df_dict["title"].append(title.text)
            df_dict["description"].append(desc.text)
            df_dict["link"].append(link['href'])
    return pd.DataFrame(df_dict)


df = search('africa', lang='en')
df.to_csv('test.csv', index=False)
