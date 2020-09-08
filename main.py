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
    print(game.manpower)
    game.manpower = {"home": 4, "away": 5}
    # game.state["home"] = {"home": 4, "away": 5}
    print(game.manpower["home"])