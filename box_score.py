import requests
import json
import re
from bs4 import BeautifulSoup
import multiprocessing 
from collections import ChainMap

def gather_boxscores(year, headers):
    
    # extract all the hrefs from the box_years page.
    response = requests.get(f'https://www.thebaseballcube.com/content/box_year/{year}/', headers=headers).text
    soup     = BeautifulSoup(response, 'html.parser')
    table    = soup.findAll('table')[0]
    hrefs    = [href['href'] for href in table.findAll('a')]
    
    # game tags; represent regular, playoff, and all star
    tags     = ['~r', '~p', '~a'] 
    # parse the hrefs to get the dates of all the games.
    dates    = [href.split('/')[-2] for href in hrefs if not any(substr in href for substr in tags)]

    # place hrefs in storage map with date as key, and list of games as values
    storage  = {date: {'overview':None, 'games':[]} for date in dates}

    try:
        for href in hrefs:
            ref = href.split('/')[-2]
            if any(substr in ref for substr in tags):

                # for some reason, the games have an extra zero appended to them, so you have to adjust
                # the key to match it.
                key = re.findall('\d+', ref )[0][:-1]
                
                # create dictionary to store the game href and the game data
                _d  = {'href': href, 'game_data': None}
                storage[key]['games'].append(_d)
            else:
                storage[ref]['overview'] = href

        return {year:storage}
    except Exception as err:
        print(err)
        pass

if __name__ == '__main__':

    YEAR_ARR  = [i for i in range(2000,2022)]

    HEADERS   = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    star_tup  = [(i, HEADERS) for i in YEAR_ARR]

    with multiprocessing.Pool(6) as pool:
        result = pool.starmap(gather_boxscores, star_tup)

    # pool.starmap returns list of dicts, convert to json.
    data = dict(ChainMap(*result))
    
    with open('../datasets/box scores/boxscores.json', 'w') as f:
        json.dump(data, f)
