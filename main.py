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
import sys

def scrape_stats():
    # get ref data
    try:
        referees = scrape.referee_data(driver)
        for ref in referees:
            ref_data = dict()
            ref_data = ref
            session.add(db.Official(**ref_data))
    except:
        logger.error(f'could not pull referees')

    # get boxscore by period
    try:
        boxscores = scrape.boxscore(driver)
        for boxscore in boxscores:
            boxscore_data = {"period": boxscore, **boxscores[boxscore]}
            session.add(db.Boxscore(**boxscore_data))
    except:
        logger.error(f'could not pull boxscore')

    #get penalty summary by team
    try:
        penalty_summaries = scrape.penalty_summary(driver)
        for summary in penalty_summaries:
            session.add(db.Penalty_Summary(**summary))
    except:
        logger.error(f'could not pull penalty summary')

    #get three stars
    try:
        stars = scrape.three_stars(driver)
        for star in stars:
            session.add(db.Star(**star))
    except:
        logger.error(f'could not pull three stars')

    #get coaches
    try:
        coaches = scrape.coaches(driver)
        for coach in coaches:
            session.add(db.Coach(**coach))
    except:
        logger.error(f'could not pull coaches')

    # get individual scorelines
    try:
        player_scorlines = scrape.player_scorelines(driver)
        for player_scoreline in player_scorlines:
            session.add(db.Player_Scoreline(**player_scoreline))
    except:
        logger.error(f'could not pull player scoreline')


    ###get all preview stats
    try:
        top_scorers, recent_games, matchup_statlines, head2head_statlines, previous_meetings = scrape.preview_stats(driver)
    except:
        logger.error(f'could not pull preview stats')

    #get top scorers
    try:
        for top_scorer in top_scorers:
            session.add(db.Top_Scorer(**top_scorer))
    except:
        logger.error(f'could not pull preview stats')

    #get recent games
    try:
        for recent_game in recent_games:
            session.add(db.Recent_Game(**recent_game))
    except:
        logger.error(f'could not pull recent games')

    #get matchup stats
    try:
        for matchup_statline in matchup_statlines:
            session.add(db.Matchup_Statline(**matchup_statline))
    except:
        logger.error(f'could not pull matchup stats')

    #get head2head stats
    try:
        for head2head_statline in head2head_statlines:
            session.add(db.Head2Head_Statline(**head2head_statline))
    except:
        logger.error(f'could not pull head-to-head stats')

    #get previous meetings
    try:
        for previous_meeting in previous_meetings:
            session.add(db.Previous_Meeting(**previous_meeting))
    except:
        logger.error(f'could not pull previous meetings')

    #get all pbp data
    try:
        goals, shots, goalie_changes, penalties, onice_events, shootout_attempts, pins = scrape.pbp(driver)
    except:
        logger.error(f'could not pull pbp data')

    #get goalie changes
    try:
        for goalie_change in goalie_changes:
            session.add(db.Goalie_Change(**goalie_change))
    except:
        logger.error(f'could not pull goalie changes')

    #get shots
    try:
        for shot in shots:
            session.add(db.Shot(**shot))
    except:
        logger.error(f'could not pull shots')

    #get penalties
    try:
        for penalty in penalties:
            session.add(db.Penalty(**penalty))
    except:
        logger.error(f'could not pull penalties')

    #get goals
    try:
        for goal in goals:
            session.add(db.Goal(**goal))
    except:
        logger.error(f'could not pull goals')

    #get onice_events
    try:
        for onice_event in onice_events:
            session.add(db.Onice_Event(**onice_event))
    except:
        logger.error(f'could not pull plus-minus events')

    #get shootout_attempts
    try:
        for shootout_attempt in shootout_attempts:
            session.add(db.Shootout_Attempt(**shootout_attempt))
    except:
        logger.error(f'could not pull shootout attempts')

    #get pins
    try:
        for pin in pins:
            session.add(db.Pin(**pin))
    except:
        logger.error(f'could not pull pins')

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
    game_id = db.get_last_game_in_db(session, meta) + 1
except: #no games found in database, assume first AHL game with pins
    game_id = 1017122 #see 1020571 for example of a postponed game; 1020558 for sample of typical final game
logger.info(f'Starting scrape sequence at Game #{game_id}')

#loop through games
while game_id <= (game_id + 10):#1020767:

    #navigate to game page via selenium
    driver = scrape.get_driver(game_id, driver)

    # try to pull game data
    for attempt in range(2):
        try:
            #get game data
            games = scrape.game_data(driver)
            
            #loop through games (should only be one game)
            for game in games:

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
            commits = len(session)
            session.commit()

            #log out that game was completed
            logger.info(f'Scraping of Game #{game_id} complete.  {commits} rows added to database.')

            #increment game_id
            game_id += 1

# quit everything
session.close()
engine.dispose()
driver.quit()

# if __name__ == "__main__":
#     print("Hello World")