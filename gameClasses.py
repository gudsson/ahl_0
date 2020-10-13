import constants as C
from scrape.report import raw_page
from scrape.scrapers import game_data, referee_data, boxscore, penalty_summary, three_stars, coaches, player_scorelines, preview_stats, pbp, test
from dbfunctions import db_commit
from time import sleep
from datetime import datetime
from state import GameState

# class GameState(object):
#     def __init__(self, manpower = {"home": 5, "away": 5}):
#         self._manpower = manpower
#         self._active_penalties = { "home": [], "away": [] }
#         self._state_certainty = True


# individual game class
class Game2(object):
    def __init__(self, game_id=0, data_queried = [], manpower = {"home": 5, "away": 5}):#, data=None):
        self.data_queried = data_queried
        self.game_id = game_id
        self._manpower = manpower
        self._state_certainty = True
        # self.state = GameState()

    @property
    def manpower(self):
        return self._manpower

    @manpower.setter
    def manpower(self, value):
        self._manpower = value

    def change_manpower(self):
        test(self, self._manpower) #self._manpower = test(self)


class Game(object):
<<<<<<< HEAD
    def __init__(self, game_id=0, data_queried = []): #manpower = {"home": 5, "away": 5, "homeGoalie": True, "awayGoalie": True}):
=======
    def __init__(self, game_id=0, data_queried = [], manpower = {"home": 5, "away": 5}):#, data=None):
>>>>>>> parent of 99ecd43... add pulled goalie columns to db
        self.data_queried = data_queried
        self.game_id = game_id
        # self._manpower = manpower
        self._state_certainty = True

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        if value < C.MIN_GAME or value > C.MAX_GAME:
            raise ValueError(f'Game {value} out of range [{C.MIN_GAME, C.MAX_GAME}]')
        else:
            self._game_id = int(value)
            for attempt in range(2):
                try:
                    self._report = raw_page(self._game_id)
                    self._games = game_data(self._game_id, self._report)
                    self._game_type = self._games["game_type"]


                    print(self._game_type)




                    self._teams = { "home": self._games[0]["home_team"], "away": self._games[0]["away_team"] }

                    # self._states = GameStates()

                    if not self.data_queried: #data queried array is empty, load all
                        try:
                            self.load_all()
                        except:
                            raise ValueError(f'Game #{self._game_id} - could not load data despite game being final')
                            self._missing_games = [{ "game_id": self._game_id,  "status": self._games["status"], "time_queried": datetime.now()}]

                    else:
                        for report_type in data_queried:
                            getattr(Game, self.report_type) #check if works
                    break

                except:
                    if attempt == 0:
                        sleep(10)
                    else:
                        raise ValueError(f'Game #{self._game_id} - could not load data, added to missing games table')
                        self._missing_games = [{ "game_id": self._game_id,  "status": "did not load", "time_queried": datetime.now()}]
                        
            #commit returned data to db
            # db_commit(self)

    #not sure I need these
    @property
    def game_type(self):
        return self._game_type

    @property
    def report(self):
        return self._report

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

    def states(self):
        pass

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


#define game state
# class GameStates(object):
#     def __init__(self, manpower = {"home": 5, "away": 5}):
#         self._manpower = manpower

#     @property
#     def manpower(self):
#         return self._manpower

#     @manpower.setter
#     def manpower(self, value):
#         self._manpower = value

if __name__ == "__main__":
    pass