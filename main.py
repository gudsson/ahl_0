# import scrapers
# from sqlalchemy import create_engine

import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Time, Date, MetaData, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dbfunctions as db
import scrapers as scrape
import pandas as pd

# connect to the db
# conn = psycopg2.connect(
#         host = "localhost",
#         database = "AHLdb",
#         user="postgres",
#         password="Olafur84!"
# )

engine, session = db.connect()

game_id = 1020540

driver = scrape.get_driver(game_id)

# # get game data
# game_data = dict()
# game_data = scrape.game_data(driver)
# game_data['game_id'] = game_id
# game = db.Game(**game_data)
# session.add(game)

# # get ref data
# referees = scrape.referee_data(driver)
# for ref in referees:
#     ref_data = dict()
#     ref_data = ref
#     ref_data['game_id'] = game_id
#     session.add(db.Official(**ref_data))

# get boxscore by period
boxscores = scrape.boxscore(driver)
for boxscore in boxscores:
    boxscore_data = {"period": boxscore, **boxscores[boxscore]}
    boxscore_data['game_id'] = game_id
    session.add(db.Boxscore(**boxscore_data))

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