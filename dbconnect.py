from APIfooty import footy
import datetime
from dbkeys import *

footy1 = footy()
starter_coins = 100

class db():
    global footy1
    global mydb
    global starter_coins

    def init_user(self, author):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT username FROM users WHERE username = \"%s\"" % (author))
        checkUsername = mycursor.fetchone()
        print(checkUsername)
        if checkUsername == None:
            mycursor.execute("INSERT INTO users (username, coins) VALUES(\"%s\", \"%d\")" % (author, starter_coins))
            response = "You now have " + str(starter_coins) + " coins to start betting with!"
            mydb.commit()
            return response
        else:
            response = "You are already registered uwu"
            return response

    def next_match(self, number):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT home,away,m_starts, fixture_id, home_evens, away_evens, draw_evens FROM v_next_matches LIMIT %d;" % (number))
        query_r=mycursor.fetchall()
        return query_r

    def next_match_team(self, name, number):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT home,away,m_starts, fixture_id, home_evens, away_evens, draw_evens FROM v_next_matches WHERE home LIKE '%s' or away LIKE '%s' LIMIT %d;" % (name, name, number))
        query_r = mycursor.fetchall()
        print(mycursor.statement)
        return query_r

    def insert_db(self):
        list_of_fixtures = []
        results = footy1.update_seasonal_fixtures()
        for i in range (0,380):
        # i = 0
            league_id = results[i]['league_id']
            fixture_id = results[i]['fixture_id']
            isPostponed= 1 if results[i]['status']=="Match Postponed" else 0
            m_starts = datetime.datetime.fromtimestamp(results[i]['event_timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            # print(m_starts)
            home = results[i]['homeTeam']['team_name']
            away = results[i]['awayTeam']['team_name']
            cur = (fixture_id, home, away, m_starts, league_id, isPostponed)
            list_of_fixtures.append(cur)
        # print(list_of_fixtures)
        mycursor = mydb.cursor()
        query = "INSERT INTO fixtures (fixture_id, home, away, m_starts, league_id, isPostponed) VALUES (%s, %s, %s, %s, %s, %s);"
        mycursor.executemany(query, list_of_fixtures)
        mydb.commit()

    def update_odds(self):
        mycursor = mydb.cursor()
        # print(len(odds))
        # i=0
        mycursor.execute("SELECT fixture_id FROM fixtures WHERE m_starts > CURRENT_DATE() AND m_starts < (CURRENT_DATE() + INTERVAL 7 DAY) AND result is NULL;")

        fixtures_to_fetch_dirty = mycursor.fetchall()
        for i in fixtures_to_fetch_dirty:
            # fixtures_to_fetch.append(i[0])
            odds = footy1.update_fixtures_daily(i[0])
            for i in range(len(odds)):
                print(odds[i]['fixture'])
                cur_fix = odds[i]['fixture']['fixture_id']
                bets_path = odds[i]['bookmakers'][0]['bets']
                for i in range(len(bets_path)):
                    if bets_path[i]['label_name']=="Match Winner":
                        odds_path = bets_path[i]['values']
                        break
                for i in range(len(odds_path)):
                    if odds_path[i]['value'] == "Home":
                        home_odds = odds_path[i]['odd']
                    if odds_path[i]['value'] == "Away":
                        away_odds = odds_path[i]['odd']
                    if odds_path[i]['value'] == "Draw":
                        draw_odds = odds_path[i]['odd']

                print(cur_fix,home_odds,draw_odds,away_odds)
                mycursor.execute("UPDATE fixtures SET home_evens = %s, draw_evens = %s, away_evens = %s WHERE fixture_id = %s" %  (home_odds, draw_odds, away_odds, cur_fix))

        # print(fixtures_to_fetch)

        # odds = footy1.update_fixtures_daily(fixtures_fetch)

        mydb.commit()

    def update_results(self):
        results = footy1.update_results()
        mycursor = mydb.cursor()

        for i in range (0,380):
            if results[i]['statusShort']=="FT":
                fixture_id = results[i]['fixture_id']
                h_goals = int(results[i]['goalsHomeTeam'])
                a_goals = int(results[i]['goalsAwayTeam'])
                win = 'H' if h_goals > a_goals else 'A' if a_goals>h_goals else 'D'
                # print(win+str(fixture_id))
                mycursor.execute("UPDATE fixtures SET result = '%s' WHERE fixture_id = '%s' AND result is NULL"% (win, fixture_id))
                # print(win, fixture_id)
            else:
                continue
        mydb.commit()

    def add_bets(self, home, away, side, amount, user):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT user_id, coins FROM users WHERE username ='%s'" % (user))
        print("Step1")
        u_id, coins = mycursor.fetchone()
        if amount<=coins and amount>0:
            mycursor.execute("SELECT fixture_id, result FROM v_next_matches WHERE home LIKE '%s' and away LIKE '%s'" % (home, away))
            print("Step2")
            f_id = mycursor.fetchone()
            # print(f_id[1])
            if(f_id[1] is None):
                if side == "H" or side == "h":
                    mycursor.execute("SELECT home_evens FROM fixtures WHERE fixture_id = '%s'" % (f_id[0]))
                elif side == "A" or side == "a":
                    mycursor.execute("SELECT away_evens FROM fixtures WHERE fixture_id = '%s'" % (f_id[0]))
                elif side == "D" or side =="d":
                    mycursor.execute("SELECT draw_evens FROM fixtures WHERE fixture_id = '%s'" % (f_id[0]))
                bet_evens = mycursor.fetchone()
                print("Step3" + str(u_id) + str(bet_evens[0]) + str(amount) + str(f_id[0]))
                mycursor.execute("INSERT INTO bets (user_id, betEvens, betAmount, fixture_id, bet_on) VALUES (%s, %s, %s, %s, '%s')" % (u_id, bet_evens[0], amount, f_id[0], side))
                print("Step4")
                mycursor.execute("UPDATE users SET coins = coins - %s WHERE user_id = '%s'" % (amount, u_id))
                mydb.commit()
                return 1
            else:
                return 0

        else:
            return 0

    def show_coins(self, author):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT coins FROM users WHERE username = '%s'" % author)
        coins = mycursor.fetchone()
        return(coins[0])

    def show_bets(self, author):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT user_id FROM users WHERE username = '%s'" % author)
        user = mycursor.fetchone()
        mycursor.execute("SELECT COUNT(*) FROM bets WHERE user_id = '%s' and successful is NULL" % user[0])
        count = mycursor.fetchone()
        return(count[0])

    def show_current_bets(self, author):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT user_id FROM users WHERE username = '%s'" % author)
        user = mycursor.fetchone()
        mycursor.execute("SELECT * FROM bets WHERE user_id = '%s' AND successful is NULL" % user)
        result = mycursor.fetchall()
        fixtures = []
        for i in result:
            mycursor.execute("SELECT home, away FROM fixtures WHERE fixture_id = '%s'" % i[4])
            fixtures.append(mycursor.fetchall())

        # print(fixtures)
        return(result, fixtures)

    # def update_fix_timings(self):
    #     results = footy1.update_ten_fixtures()
    #     mycursor = mydb.cursor()
    #     mycursor.execute("SELECT fixture_id from v_next_matches LIMIT 10;")
    #     fixtures = mycursor.fetchall()
    #     # fixtures=[(1234,0), (1235,0), (1234,0)]
    #     for i in range(len(fixtures)):
    #         for j in range(len(results)):
    #             if fixtures[i[0]] == results[j]['fixture_id']:
    #                 m_starts = datetime.datetime.fromtimestamp(results[j]['event_timestamp']).strftime("%Y-%m-%d %H:%M:%S")
    #                 mycursor.execute("UPDATE fixtures SET m_starts = %s WHERE fixture_id = %s" %(m_starts, fixtures[i[0]]))
    #                 break
    #     mydb.commit()

    # def test(self):
    #     mycursor = mydb.cursor()
    #     mycursor.execute("SELECT fixture_id from v_next_matches LIMIT 10;")
    #     fixtures = mycursor.fetchall()
    #     print(fixtures)



# db1 = db()
# db1.test()
# db1.update_results()
# db1.update_odds()
# db1.insert_db()
# db1.next_match(3)
