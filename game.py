import constants as C
import scrapers
from scrape.report import ScrapeReport, raw_page
from scrape.scrapers import game_data, referee_data, boxscore, penalty_summary, three_stars, coaches, player_scorelines, preview_stats, pbp
from dbfunctions import db_commit
# from func import *

# from driver import driver

class Game(object):
    def __init__(self, game_id=0, data_queried = []):#, data=None):
        self.data_queried = data_queried
        self.game_id = game_id
        # self.data = dict()

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
            self._games = game_data(self._game_id, self._report)
            self._teams = { "home": self._games[0]["home_team"], "away": self._games[0]["away_team"] }

            if not self.data_queried: #data queried array is empty, load all
                self.load_all()
            else:
                for report_type in data_queried:
                    getattr(Game, self.report_type) #check if works
            
            #commit returned data to db
            db_commit(self)
                # load individually (eventually...)

    # @property
    # def data_queried(self):
    #     return self._data_queried

    @property
    def report(self):
        return self._report

    # @property
    # def summary_container(self):
    #     return self._summary_container
    
    @property
    def games(self):
        return self._games

    @property
    def teams(self):
        return self._teams

    @property
    def officials(self):
        return self._officials

    @property
    def boxscores(self):
        return self._boxscores

    @property
    def penalty_statlines(self):
        return self._penalty_statlines

    @property
    def stars(self):
        return self._stars

    @property
    def coaches(self):
        return self._coaches

    @property
    def player_scorelines(self):
        return self._player_scorelines
    
    @property
    def top_scorers(self):
        return self._top_scorers

    @property
    def recent_games(self):
        return self._recent_games 

    @property
    def matchup_statlines(self):
        return self._matchup_statlines

    @property
    def head2head_statlines(self):
        return self._head2head_statlines

    @property
    def previous_meetings(self):
        return self._previous_meetings

    @property
    def goals(self):
        return self._goals

    @property
    def shots(self):
        return self._shots

    @property
    def goalie_changes(self):
        return self._goalie_changes

    @property
    def penalty_calls(self):
        return self._penalty_calls

    @property
    def onice_events(self):
        return self._onice_events

    @property
    def shootout_attempts(self):
        return self._shootout_attempts

    @property
    def pins(self):
        return self._pins

    def officials(self):
        self._officials = referee_data(self, self._report)
    
    def boxscores(self):
        self._boxscores = boxscore(self, self._report)

    def penalty_statlines(self):
        self._penalty_statlines = penalty_summary(self, self._report)

    def stars(self):
        self._stars = three_stars(self, self._report)

    def coaches(self):
        self._coaches = coaches(self, self._report)

    def player_scorelines(self):
        self._player_scorelines = player_scorelines(self, self._report)

    def preview_stats(self):
        self._top_scorers, self._recent_games, self._matchup_statlines, self._head2head_statlines, self._previous_meetings = preview_stats(self, self._report)

    def pbp(self):
        self._goals, self._shots, self._goalie_changes, self._penalty_calls, self._onice_events, self._shootout_attempts, self._pins = pbp(self, self._report)

    # @property
    def load_all(self):
        self.officials()
        self.boxscores()
        self.penalty_statlines()
        self.stars()
        self.coaches()
        self.player_scorelines()
        self.preview_stats()
        self.pbp()
        # self._officials = referee_data(self, self._report)
        # self._boxscores = boxscore(self, self._report)
        # self._penalty_statlines = penalty_summary(self, self._report)
        # self._stars = three_stars(self, self._report)
        # self._coaches = coaches(self, self._report)
        # self._player_scorelines = player_scorelines(self, self._report)
        # self._top_scorers, self._recent_games, self._matchup_statlines, self._head2head_statlines, self._previous_meetings = preview_stats(self, self._report)
        # self._goals, self._shots, self._goalie_changes, self._penalty_calls, self._onice_events, self._shootout_attempts, self._pins = pbp(self, self._report)





    # @officials.setter
    # def officials(self):
    #     self._officials = referee_data(self._report)


    # @data.setter
    # def data(self, value):
    #     self._data = game_data(self._game_id, self._report)
        

    #     def game_data(driver):
    
    # def get_game_data(matchup_container):
    #     #declarations
    #     global game
    #     game_info = dict()
    #     arena = dict()
    #     # combined_dict = dict()
    #     game_data = []
        
    #     #get various elements
    #     scores = matchup_container.find_elements_by_xpath("//div[@class='ht-gc-score-container']")
    #     date = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-game-date')]").text.split(", ", 1)

    #     #add scraping to dict
    #     game_info["game_id"] = game.game_id
    #     game_info["game_number"] = matchup_container.find_element_by_xpath("//*[@class='ht-game-number']").text.split("#: ")[1]
        
    #     #establish date
    #     game_info["date"] = date[1]
    #     game_date = datetime.strptime(game_info["date"],"%B %d, %Y")

    #     game_info["dow"] = date[0]
    #     game_info["status"] = matchup_container.find_element_by_xpath("//*[contains(@ng-bind,'gameSummary.details.status')]").text
    #     game_info["away_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-visiting-team')]").text
    #     game_info["away_score"] = scores[0].text
    #     game_info["home_score"] = scores[1].text
    #     game_info["home_team"] = matchup_container.find_element_by_xpath("//*[contains(@class,'ht-gc-home-team')]").text

    #     #Gets game_type
    #     if game_date.month == 9:
    #         game_info["game_type"] = "Pre-Season"
    #     elif 4 <= game_date.month <= 7:
    #         if int(game_info["game_number"]) <= 7:
    #             game_info["game_type"] = "Playoff"
    #     elif "All-Star" in game_info["home_team"] or "All-Star" in game_info["away_team"]:
    #         game_info["game_type"] = "All-Star"
    #     else:
    #         game_info["game_type"] = "Regular"

    #     #Gets season based on date.  Assumes season will always end before September 1
    #     game_info["season"] = game_info["date"].split(",")[1].strip()
    #     game_info["season"] = game_info["season"] + str(int(game_info["season"])+1) if game_date.month > 8 else str(int(game_info["season"])-1) + game_info["season"]
        
    #     #add arena to game_info dict
    #     arena = arena_data(driver)
    #     game_info.update(arena)

    #     #append all game data to return array
    #     game_data.append(game_info)

    #     #update class instance 'game'
    #     game.home_team = game_info["home_team"]
    #     game.away_team = game_info["away_team"]

    #     #return array
    #     return game_data

    # try:
    #     container = driver.find_element_by_xpath("//div[@class='ht-gc-header-row']")
    #     return get_game_data(container)
    # except:
    #     raise ValueError('Cannot find game data')


        return (self._game_id + 12)


    

    

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