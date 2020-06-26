# pylint: disable=no-member

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
import sys, traceback

def scrape_stats():
    try:
        # get ref data
        referees = scrape.referee_data(driver)
        for ref in referees:
            ref_data = dict()
            ref_data = ref
            session.add(db.Official(**ref_data))

        # get boxscore by period
        boxscores = scrape.boxscore(driver)
        for boxscore in boxscores:
            boxscore_data = {"period": boxscore, **boxscores[boxscore]}
            session.add(db.Boxscore(**boxscore_data))

        #get penalty summary by team
        penalty_summaries = scrape.penalty_summary(driver)
        for summary in penalty_summaries:
            session.add(db.Penalty_Summary(**summary))

        #get three stars
        stars = scrape.three_stars(driver)
        for star in stars:
            session.add(db.Star(**star))

        #get coaches
        coaches = scrape.coaches(driver)
        for coach in coaches:
            session.add(db.Coach(**coach))

        # get individual scorelines
        player_scorlines = scrape.player_scorelines(driver)
        for player_scoreline in player_scorlines:
            session.add(db.Player_Scoreline(**player_scoreline))

        ###get all preview stats
        top_scorers, recent_games, matchup_statlines, head2head_statlines, previous_meetings = scrape.preview_stats(driver)

        #get top scorers
        for top_scorer in top_scorers:
            session.add(db.Top_Scorer(**top_scorer))

        #get recent games
        for recent_game in recent_games:
            session.add(db.Recent_Game(**recent_game))

        #get matchup stats
        for matchup_statline in matchup_statlines:
            session.add(db.Matchup_Statline(**matchup_statline))

        #get head2head stats
        for head2head_statline in head2head_statlines:
            session.add(db.Head2Head_Statline(**head2head_statline))

        #get previous meetings
        for previous_meeting in previous_meetings:
            session.add(db.Previous_Meeting(**previous_meeting))

        #get all pbp data
        goals, shots, goalie_changes, penalties, onice_events, shootout_attempts, pins = scrape.pbp(driver)


        #get goalie changes
        for goalie_change in goalie_changes:
            session.add(db.Goalie_Change(**goalie_change))

        #get shots
        for shot in shots:
            session.add(db.Shot(**shot))

        #get penalties
        for penalty in penalties:
            session.add(db.Penalty(**penalty))

        #get goals
        for goal in goals:
            session.add(db.Goal(**goal))

        #get onice_events
        for onice_event in onice_events:
            session.add(db.Onice_Event(**onice_event))

        #get shootout_attempts
        for shootout_attempt in shootout_attempts:
            session.add(db.Shootout_Attempt(**shootout_attempt))

        #get pins
        for pin in pins:
            session.add(db.Pin(**pin))
    except:
        traceback.print_exc()
        raise


def error_logging():
    #error logging
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('main.log')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)

    return log

#initialize error logging
logger = error_logging()

#initialize headless firefox
logger.info(f'Opening Firefox...')
driver = scrape.initialize_driver()

#connect to db
Base, engine, session, meta = db.connect()

#get last scraped game
try:    #try getting most recent scraped game
    game_id = 1019754#db.get_last_game_in_db(session, meta) + 1
except: #no games found in database, assume first AHL game with pins
    game_id = 1017122 #see 1020571 for example of a postponed game; 1020558 for sample of typical final game
logger.info(f'Starting scrape sequence at Game #{game_id}')

#loop through games
while game_id <= 1019754:#1020767:

    #navigate to game page via selenium
    driver = scrape.get_driver(game_id, driver)
    time.sleep(10)

    # try to pull game data
    for attempt in range(2):
        try:
            #get game data
            games = scrape.game_data(driver)
            logger.info(f'Pulling data for Game #{game_id}')

        except:
            if attempt == 0:    #try again if first pull attempt fails
                logger.warning(f'Game #{game_id} - game data not found...waiting 10 seconds before retrying')
                time.sleep(10)
            else:               #second try failed, log failure and add game to missing game list
                logger.error(f'Game #{game_id} - ERROR IN LOADING DATA')
                missing_game = db.Missing_Game(game_id, "did not load", datetime.now())
                session.add(missing_game)
                break
        else:
            #loop through games (should only be one game)
            for game in games:
                if game['status'].lower() == 'postponed' or 'final' in game['status'].lower():
                    if 'final' in game['status'].lower():
                        try:
                            session.add(db.Game(**game))
                            scrape_stats()

                        except:
                            logger.error(f'Game #{game_id} - cannot pull data despite game being final: see https://theahl.com/stats/game-center/{game_id}')
                            missing_game = db.Missing_Game(game_id, game['status'].lower(), datetime.now())
                            session.expunge_all()
                            session.add(missing_game)
                            break
                else:   #else game in progress?
                    logger.error(f"Game #{game_id} - game state = {game['status']}")
                    missing_game = db.Missing_Game(game_id, game['status'].lower(), datetime.now())
                    session.expunge_all()
                    session.add(missing_game)
                    break
            commits = len(session.new)
            logger.info(f'Scraping of Game #{game_id} complete.  Adding {commits} new rows to database.')
            break
        
    #try committing whatever you have to db
    try:
        session.commit()
    except:
        logger.error("DB commit failed")
        traceback.print_exc()
        session.expunge_all()
        missing_game = db.Missing_Game(game_id, game['status'].lower(), datetime.now())
        session.add(missing_game)
        try:
            session.commit()
        except:
            logger.error(game_id + ' could not be added to missing games table')
        raise

    #increment game_id
    game_id += 1

# quit everything
logger.info(f'Exiting program.')
session.close()
engine.dispose()
driver.quit()

# if __name__ == "__main__":
#     print("Hello World")