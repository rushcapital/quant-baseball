import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display

from django.core.management.base import BaseCommand
from boxscores.models import BoxScoreHitting
from sqlalchemy import create_engine
from django.conf import settings

class Command(BaseCommand):
    help = "a command to gather data frome baseball-reference box scores."

    def handle(self, *args, **kwargs):

        df = pd.read_csv('../datasets/baseball savant/general sets/batter percentile rankings.csv')
        df['player_name'] = df['player_name'].astype(str)

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format( user=user,password=password,database_name=database_name,)

        engine = create_engine(database_url, echo=False)

        df.to_sql(BoxScoreHitting._meta.db_table, if_exists='replace', con=engine, index=False)

# # generate the box scores.
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
            display(df)
            
            
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
            display(df)

def get_box_scores():
    
    base_url = 'https://www.baseball-reference.com/boxes/'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    game_hrefs = [href for href in soup.select("a[href*='2022']") if 'Final' in href.text]

    for href in game_hrefs:
        get_individual_box_scores(href)
        break

    return game_hrefs
