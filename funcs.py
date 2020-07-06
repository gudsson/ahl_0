import gameClasses as gC
import constants as C
import dbfunctions
import logging
from datetime import datetime, timedelta

def error_logging(name):
    #error logging
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('main.log')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)

    return log

def scrape_all():
    # get highest game from DB
    starting_game = dbfunctions.get_last_game_in_db()

    # if no game returned from DB, start at first game with pins
    if starting_game < C.MIN_GAME:
        starting_game = C.MIN_GAME

    finishing_game = C.MAX_GAME + 1

    for i in range(starting_game, finishing_game):
        game = gC.Game(i)

def per_overflow(time, period):
    if time > datetime.strptime('20:00', C.FMT): # if penalty expires after the end of the period, move expiry to beginning of next period.
        time = time - timedelta(minutes=20)
        period += 1 #pass
    
    time = (time).strftime(C.FMT) #convert time to string
    
    return time, period
