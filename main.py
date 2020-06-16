# import scrapers
# from sqlalchemy import create_engine

import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Time, Date, MetaData, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dbfunctions as db
import scrapers as scrape
import pandas as pd
import time
import logging

# logging.basicConfig(level=logging.INFO, file='sample.log')
# logging.info("Penis")


#error logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



logger.info("Hello")




# connect to the db
# conn = psycopg2.connect(
#         host = "localhost",
#         database = "AHLdb",
#         user="postgres",
#         password="Olafur84!"
# )

engine, session, meta = db.connect()

game_id = 1020531

driver = scrape.get_driver(game_id)




# time.sleep(10)




# # get game data
# game_data = scrape.game_data(driver)
# game = db.Game(**game_data)
# session.add(game)

# # get ref data
# referees = scrape.referee_data(driver)
# for ref in referees:
#     ref_data = dict()
#     ref_data = ref
#     session.add(db.Official(**ref_data))

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

# #get top scorers
# top_scorers, recent_games, matchup_statlines, head2head_statlines, previous_meetings = scrape.preview_stats(driver)
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


##get all pbp data
# goals, shots, goalie_changes, penalties, onice_events, shootout_attempts, pins = scrape.pbp(driver) #goals, shots, goalie_changes, penalties, onice_events, shootout_attempts, pins 

# #get goalie changes
# for goalie_change in goalie_changes:
#     session.add(db.Goalie_Change(**goalie_change))

#get shots
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

    
# session.commit()

# # quit
# session.close()
# engine.dispose()
# driver.quit()




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