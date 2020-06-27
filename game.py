import constants as C
import scrapers
from scrape.report import ScrapeReport, raw_page

# from driver import driver

class Game(object):
    def __init__(self, game_id=0):
        self.game_id = game_id

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        if value < C.MIN_GAME or value > C.MAX_GAME:
            raise ValueError(f'Game {value} out of range [{C.MIN_GAME, C.MAX_GAME}]')
        else:
            # print(f'game_id set to: {value}')
            self._game_id = int(value)
            self._report = raw_page(self._game_id)
            self._summary_container = self._report.find_element_by_xpath("//div[@class='ht-summary-container']")

    @property
    def report(self):
        return self._report

    @property
    def summary_container(self):
        return self._summary_container

    # @report.setter
    # def report(self, value):
    #     # if self._report is None:
    #     #     rep = Scraper()
    #     # # game_id = value
    #     self._report = scrape_report(self.game_id)

    

# class Game(object):
#     def __init__(self, game_id = None, raw_report = None):
#         self._game_id = game_id#.game_id if hasattr(game_id, 'game_id') else None
#         self.raw_report = Scraper.raw_report(game_id.game_id)

    # @property
    # def game_id(self):
    #     return self._game_id
    
    # @game_id.setter
    # def game_id(self, value):
    #     print(f'game_id set to: {value}')
    #     self._game_id = value
    #     return self._game_id


#define game state
class GameStates(object):
    def __init__(self, manpower = {"home": 5, "away": 5}):
        self._teams = {"home": None, "away": None}

    @property
    def home_team(self):
        print(f'home team: {self._teams["home"]}')
        return self._teams["home"]

    @home_team.setter
    def home_team(self, value):
        print(f'home team set to {value}')
        self._teams["home"] = value

    @home_team.deleter
    def home_team(self):
        print(f'home team cleared')
        self._teams["home"] = None

    @property
    def away_team(self):
        print(f'away team: {self._teams["away"]}')
        return self._teams["away"]

    @away_team.setter
    def away_team(self, value):
        print(f'away team set to {value}')
        self._teams["away"] = value

    @away_team.deleter
    def away_team(self):
        print(f'away team cleared')
        self._teams["away"] = None

    

#define game class
# class Game():
#     def __init__(self, game_id=None, home_team=None, away_team=None, key_tup=None):
#         if key_tup is None:
#             self.game_id = game_id
#             self.home_team = home_team
#             self.away_team = away_team
#         else:
#             self.game_id, self.home_team, self.away_team = key_tup

# if __name__ == "__main__":
#     driver.quit()