from game import Game, GameStates
# from scrape.report import Scraper
from selenium import webdriver
import scrapers

#get game id
game = Game(1017122)
print(game.game_id)

report = game.report
print(report.title)

# print(game.game_data)
# print(game.officials)








#####
#####How does retreiving boxscore work?
# print(game.boxscore)  #
#####







# print(game.teams["home"])
# print(game.teams["away"])
# print(game_id.game_id)

# game = Game(game_id)


# print(game.game_id)
# if __name__ == "__main__":
#     print("hello")