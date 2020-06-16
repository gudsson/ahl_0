import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Time, Date, MetaData, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dbfunctions as db
import scrapers as scrape
import pandas as pd
import time
from datetime import datetime
import logging

def scrape_stats():
    # get ref data
    print("got to scrape_stats")
    try:
        referees = scrape.referee_data(driver)
        for ref in referees:
            ref_data = dict()
            ref_data = ref
            session.add(db.Official(**ref_data))
    except:
        logger.error(f'could not pull referees')

    # # get boxscore by period
    # boxscores = scrape.boxscore(driver)
    # for boxscore in boxscores:
    #     boxscore_data = {"period": boxscore, **boxscores[boxscore]}
    #     session.add(db.Boxscore(**boxscore_data))

    # #get penalty summary by team
    # penalty_summaries = scrape.penalty_summary(driver)
    # for summary in penalty_summaries:
    #     session.add(db.Penalty_Summary(**summary))

    # #get three stars
    # stars = scrape.three_stars(driver)
    # for star in stars:
    #     session.add(db.Star(**star))

    # #get coaches
    # coaches = scrape.coaches(driver)
    # for coach in coaches:
    #     session.add(db.Coach(**coach))

    # # get individual scorelines
    # player_scorlines = scrape.player_scorelines(driver)
    # for player_scoreline in player_scorlines:
    #     session.add(db.Player_Scoreline(**player_scoreline))


    # ###get all preview stats
    # top_scorers, recent_games, matchup_statlines, head2head_statlines, previous_meetings = scrape.preview_stats(driver)

    # #get top scorers
    # for top_scorer in top_scorers:
    #     session.add(db.Top_Scorer(**top_scorer))

    # # #get recent games
    # for recent_game in recent_games:
    #     session.add(db.Recent_Game(**recent_game))

    # #get matchup stats
    # for matchup_statline in matchup_statlines:
    #     session.add(db.Matchup_Statline(**matchup_statline))

    # #get head2head stats
    # for head2head_statline in head2head_statlines:
    #     session.add(db.Head2Head_Statline(**head2head_statline))

    # #get previous meetings
    # for previous_meeting in previous_meetings:
    #     session.add(db.Previous_Meeting(**previous_meeting))


    # #get all pbp data
    # goals, shots, goalie_changes, penalties, onice_events, shootout_attempts, pins = scrape.pbp(driver)

    # #get goalie changes
    # for goalie_change in goalie_changes:
    #     session.add(db.Goalie_Change(**goalie_change))

    # #get shots
    # for shot in shots:
    #     session.add(db.Shot(**shot))

    # #get penalties
    # for penalty in penalties:
    #     session.add(db.Penalty(**penalty))

    # #get goals
    # for goal in goals:
    #     session.add(db.Goal(**goal))

    # #get onice_events
    # for onice_event in onice_events:
    #     session.add(db.Onice_Event(**onice_event))

    # #get shootout_attempts
    # for shootout_attempt in shootout_attempts:
    #     session.add(db.Shootout_Attempt(**shootout_attempt))

    # #get pins
    # for pin in pins:
    #     session.add(db.Pin(**pin))



#error logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

#connect to db
engine, session, meta = db.connect()

#get last game
game_id = 1020558
#1017122 start
#1020767 end
#1020571 postponed example
#1020558 final example

#load next game on gamecenter via firefox
driver = scrape.get_driver(game_id)

# try to pull game data
for attempt in range(2):
    try:
        #get game data
        games = scrape.game_data(driver)
        
        #loop through games (should only be one game)
        for game in games:

            session.add

            if game['status'].lower() == 'postponed' or game['status'].lower() == 'final':
                print(game['status'])

                if game['status'].lower() == 'final':
                    try:
                        scrape_stats()
                        session.add(db.Game(**game))
                    except:
                        logger.error(f'Game #{game_id} - cannot pull data despite game being final')
                        missing_game = db.Missing_Game(game_id, game['status'].lower(), datetime.now())
                        session.add(missing_game)
            else:   #else game in progress?
                logger.error(f"Game #{game_id} - game state = {game['status']}")
                missing_game = db.Missing_Game(game_id, game['status'].lower(), datetime.now())
                session.add(missing_game)
        break
    except:
        if attempt == 0:    #try again
            logger.warning(f'Game #{game_id} - game data not found...waiting 10 seconds before retrying')
            time.sleep(10)
        else:               #second try failed, log failure and add game to missing game list
            logger.error(f'Game #{game_id} - ERROR IN LOADING DATA')
            missing_game = db.Missing_Game(game_id, "did not load", datetime.now())
            session.add(missing_game)
            break
    finally:
        #commit whatever you have to db
        session.commit()



    # finally:
        # #commit
        # session.commit()

        # # quit
        # session.close()
        # engine.dispose()
        # driver.quit()



session.commit()

# quit
session.close()
engine.dispose()
driver.quit()




# engine, session = db.connect()


# previous_mtg = db.Previous_Meeting(game_id=999, away_team='Toronto Buttheads', away_score=5, home_team='Virginia Virgins', home_score=4, date='March 26, 2020')

# # get_last_meeting(session, meta)

# session.add(previous_mtg)


# # print(session.new)

# session.commit()

# session.close()
# engine.dispose()

# c.execute("select * from Teams")

# c.commit()

# rows = c.fetchall()

# for r in rows:
#     print(f"id {r[0]} location {r[1]} name {r[2]}")

# c.execute('''SELECT * FROM public."TEAMS_test"''')

# c.fetchall()

# c.execute("""SELECT table_name FROM information_schema.tables
#        WHERE table_schema = 'public'""")
# for table in c.fetchall():
#     print(table)



# close the cursor
# c.close()

# # close the connection
# conn.close()

# if __name__ == "__main__":
#     print("hello World")