from webbrowser import get
import requests
import multiprocessing
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import pathlib

def get_individual_box_scores(href):

    base_url = 'https://www.baseball-reference.com/boxes/'
    new_url = base_url + href['href'].split('/boxes/')[1]
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get the box score.
    table = soup.findAll("table")[0]

    # initialize scoreboard
    box_score = {
        i:{} for i in [1,2,3,4,5,6,7,8,9,'R','H','E']
    }

    # for table in tables:
    rows = table.findAll('tr')[1:3]
    for row in rows:
        team = row.select("a[href*='/teams/']")[0]['href'].split('/')[2]
        scores = [0 if td.text == 'X' else int(td.text) for td in row.find_all('td', {'class':'center'})[1:]]
        for score,key in zip(scores,box_score.keys()):
            box_score[key][team] = score 
        
    # create the directory.

    directory = "../datasets/daily box scores/" + "_vs_".join(box_score[1].keys())
    
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 

    comments_removed = response.text.replace("<!--","").replace("-->","")
    _soup = BeautifulSoup(comments_removed, 'html.parser')
    
    tables = _soup.find_all("table", {"class":"sortable stats_table min_width shade_zero"})
    for table in tables:
        if 'batting' in table["id"]:

            team_unparsed = table["id"].split('batting')[0]
            team_separated = re.findall('[A-Z][^A-Z]*', team_unparsed)
            team = " ".join(team_separated) + ' Batting'

            rows = table.find_all('tr')
            headers = rows[0].find_all('th')
            table_list = []
            for row in rows[1:]:
                
                player_info = row.find('th').text.split(' ')
                name = " ".join(player_info[:2])
                name = name.replace(u'\xa0', u'')
                position = player_info[-1]
                
                table_dict = {header.text:None for header in headers[1:]}
                table_dict['name'] = name
                table_dict['position'] = position

                stats = [stat.text for stat in row.find_all('td')]
                for k,s in zip(table_dict.keys(), stats):
                    table_dict[k] = s

                table_list.append(table_dict)
                
            # remove pitchers and pinch hitters
            table_list = [player for player in table_list if player['position'] not in ['P','PH', 'Totals', '']]
            df = pd.DataFrame(table_list).set_index(['name'])
            
            df.to_pickle(f'{directory}/{team}.pkl')

            
        else:
            team_unparsed = table["id"].split('pitching')[0]
            team_separated = re.findall('[A-Z][^A-Z]*', team_unparsed)
            team = " ".join(team_separated) + ' Pitching'

            rows = table.find_all('tr')
            headers = rows[0].find_all('th')
            table_list = []
            for row in rows[1:]:
                
                player_info = row.find('th').text.split(' ')
                name = " ".join(player_info[:2])
                name = name.replace(u'\xa0', u'')
                position = 'P'
                
                table_dict = {header.text:None for header in headers[1:]}
                table_dict['name'] = name
                table_dict['position'] = position

                stats = [stat.text for stat in row.find_all('td')]
                for k,s in zip(table_dict.keys(), stats):
                    table_dict[k] = s

                table_list.append(table_dict)

            # # remove pitchers and pinch hitters
            table_list = [player for player in table_list if player['position'] not in ['Totals', '']]
            df = pd.DataFrame(table_list).set_index(['name'])

            df.to_pickle(f'{directory}/{team}.pkl')

def get_box_scores():
    
    base_url = 'https://www.baseball-reference.com/boxes/'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    game_hrefs = [href for href in soup.select("a[href*='2022']") if 'Final' in href.text]

    return game_hrefs


def get_baseball_savant_leaderboard(_iter):

    key = _iter[0]
    endpoint = _iter[1]

    response = requests.get(endpoint)
    soup = BeautifulSoup(response.text, 'html.parser')

    # find leaderboard data (should only be one element.)
    script = str(soup.find_all("div", {"class":"article-template"})[0])

    # use regex and put everything within brackets to create a pseudo-list
    # then load this as json.
    leaderboard = json.loads('[' + re.findall('\[(.*?)\]', script)[0] + ']')

    df = pd.DataFrame(leaderboard)

    df.to_pickle(f"../datasets/baseball savant/daily leaderboards/{key}.pkl")

if __name__ == "__main__":

    # reading the data from the file
    # with open('../housekeeping/baseball_savant_endpoints.txt') as f:
    #     data = json.loads(f.read())
    #     _iter = zip(data.keys(),data.values())

    # with multiprocessing.Pool(6) as pool:
    #     result = pool.map(get_baseball_savant_leaderboard, _iter)
    
    # this doesn't take too long, so don't worry about it.
    for href in get_box_scores():
        get_individual_box_scores(href)
   
   