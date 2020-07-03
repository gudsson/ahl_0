from game import Game, GameStates
# from scrape.report import Scraper
from selenium import webdriver
import scrapers

###
###TO-DO: penalties, DB link (works, but check all stat pulls), empty preview stats early in season, add exceptions as necessary, account for missing games based on original main.py code
###



#get game id
game = Game(1019754) #empty game at beginning of season: 1017122
print(game.game_id)

report = game.report
print(report.title)

# for item in game.goals:
#     print(item)

# print("====")

# for item in game.shots:
#     print(item)

# print(vars(game))

# for key in vars(game):
#     if isinstance(vars(game)[key], list):
#         print(key)

    # self._goals, self._shots, self._goalie_changes, self._penalties, self._onice_events, self._shootout_attempts


# self._top_scorers, self._recent_games, self._matchup_statlines, self._head2head_statlines, self._previous_meetings

# print(game.game_data)
# print(game.officials)

# print(game.three_stars)






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