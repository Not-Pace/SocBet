import requests
import json
import datetime
import os

from requests.api import head
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_KEY2 = os.getenv('API_KEY2')

### League IDs
# Premier League - 2790
# Bundesliga - 2755

# league_id_cur = 0
# fixture_id_cur = 0
# start_time = 0
# isPostponed = 0
# home_team = 0
# away_team = 0
league_id = 2790
bl_league_id = 2755
bookmaker_id = 8

# fixture_id = 592151

headers = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": API_KEY
}

headers2 = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": API_KEY2
}

class footy():
    global league_id
    global bl_league_id
    global bookmaker_id
    global headers
    global headers2

    def update_fixtures_daily(self, fixture_id):
        url = "https://v2.api-football.com/odds/fixture/%d/bookmaker/%d" % (fixture_id, bookmaker_id)
        response = requests.request("GET", url, headers=headers)

        with open ('odds.txt' , 'w') as f:
            f.write(response.text)
            # response = f.read()
            parsed_json = json.loads(response.text)
            results = parsed_json['api']['odds']
            # print(len(results))
            return results

    def update_seasonal_fixtures(self):
        url = "https://v2.api-football.com/fixtures/league/%d" % (bl_league_id)
        response = requests.request("GET", url, headers=headers2)

        with open('temp.txt', 'w') as f:
            f.write(response.text)
            # print(response)
            # for i in range (0,379):
            # i=1
            parsed_json = json.loads(response.text)
            results = parsed_json['api']['fixtures']
            return results
            # league_id_cur = parsed_json['api']['fixtures'][i]['league_id']
            # fixture_id_cur = parsed_json['api']['fixtures'][i]['fixture_id']
            # start_time = parsed_json['api']['fixtures'][i]['firstHalfStart']
            # isPostponed= 1 if parsed_json['api']['fixtures'][i]['status']=="Match Postponed" else 0
            # home_team = parsed_json['api']['fixtures'][i]['homeTeam']['team_name']
            # away_team = parsed_json['api']['fixtures'][i]['awayTeam']['team_name']

        # print(league_id_cur, fixture_id_cur, start_time,isPostponed,home_team,away_team)

    def update_results(self):
        url = "https://v2.api-football.com/fixtures/league/%d" % (league_id)
        response = requests.request("GET", url, headers=headers)
        # url2 = "https://v2.api-football.com/fixtures/league/%d" % (bl_league_id)
        # response2 = requests.request("GET", url, headers=headers2)

        with open('results.txt', 'w') as f:
            f.write(response.text)
            parsed_json = json.loads(response.text)
            results = parsed_json['api']['fixtures']
            # parsed_json2 = json.loads(response2.text)
            # results.append(parsed_json2['api']['fixtures'])
            return results

    def bl_update_results(self):
        url = "https://v2.api-football.com/fixtures/league/%d" % (bl_league_id)
        response = requests.request("GET", url, headers=headers2)
        # url2 = "https://v2.api-football.com/fixtures/league/%d" % (bl_league_id)
        # response2 = requests.request("GET", url, headers=headers2)

        with open('results.txt', 'w') as f:
            f.write(response.text)
            parsed_json = json.loads(response.text)
            results = parsed_json['api']['fixtures']
            # parsed_json2 = json.loads(response2.text)
            # results.append(parsed_json2['api']['fixtures'])
            return results

        # print(datetime.datetime.fromtimestamp(start_time))

        # with open('temp2.txt', 'w') as d:
        #     d.write(results)

    def update_ten_fixtures(self):
        url = "https://v2.api-football.com/fixtures/league/%d/next/5" % (league_id)
        response = requests.request("GET", url, headers=headers)

        with open('fixtures.txt', 'w') as f:
            f.write(response.text)
            parsed_json = json.loads(response.text)
            print(response.text)
            results = parsed_json['api']['fixtures']
            return results

# footy1 = footy()
# temp = footy1.update_fixtures_daily()