# import game
# from scrape.report import Scraper
# from selenium import webdriver
# import scrapers
# import logging
from funcs import error_logging, scrape_all, scrape_game, scrape_game2

logger = error_logging(__name__)

###
###TO-DO: penalties, add exceptions as necessary
###

if __name__ == "__main__":
    game = scrape_game2(1020165)#scrape_all()
    print(game.state.manpower)