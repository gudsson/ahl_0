import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, Float, Time, Date, MetaData, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import atexit
import sys

Base = declarative_base()

def connect():
        
        engine = create_engine(
        "postgresql+psycopg2://postgres:Olafur84!@localhost/AHLdb",
        executemany_mode='batch')

        Session = sessionmaker(bind=engine)
        session = Session()
        meta = MetaData()
        Base.metadata.create_all(engine)

        return Base, engine, session, meta

class Missing_Game(Base):
        __tablename__ = 'missing_games'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        status = Column(String(length=20))
        time_queried = Column(Time)

        def __init__(self, game_id, status, time_queried):
                self.game_id = game_id
                self.status = status
                self.time_queried = time_queried


class Game(Base):
        __tablename__ = 'games'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        game_number = Column(String(length=4))
        season = Column(Integer)
        game_type = Column(String(length=20))
        date = Column(Date)
        dow = Column(String(length=9))
        status = Column(String(length=10))
        away_team = Column(String(length=50))
        away_score = Column(Integer)
        home_score = Column(Integer)
        home_team = Column(String(length=50))
        venue = Column(String(length=50))
        attendance = Column(Integer)
        start_time = Column(String(length=8))
        end_time = Column(String(length=8))
        duration = Column(Time)
        
        def __init__(self, game_id, game_number, season, game_type, date, dow, status, away_team, away_score, home_score, home_team, venue, attendance, start_time, end_time, duration): 
                self.game_id = game_id
                self.game_number = game_number
                self.season = season
                self.game_type = game_type
                self.date = date
                self.dow = dow
                self.status = status
                self.away_team = away_team
                self.away_score = away_score
                self.home_score = home_score
                self.home_team = home_team
                self.venue = venue
                self.attendance = attendance
                self.start_time = start_time
                self.end_time = end_time
                self.duration = duration


class Official(Base):
        __tablename__ = 'officials'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        name = Column(String(length=50))
        number = Column(Integer)
        role = Column(String(length=8))

        def __init__(self, game_id, name, number, role):
                self.game_id = game_id
                self.name = name
                self.number = number
                self.role = role


class Boxscore(Base):
        __tablename__ = 'boxscores'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        period = Column(String(length=2))
        home_goals = Column(String(length=2))
        away_goals = Column(String(length=2))
        home_shots = Column(String(length=3))
        away_shots = Column(String(length=3))

        def __init__(self, game_id, period, home_goals, away_goals, home_shots, away_shots):
                self.game_id = game_id
                self.period = period
                self.home_goals = home_goals
                self.away_goals = away_goals
                self.home_shots = home_shots
                self.away_shots = away_shots


class Star(Base):
        __tablename__ = 'stars'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=35))
        side = Column(String(length=4))
        star_number = Column(String(length=3))
        name = Column(String(length=50))
        jersey_number = Column(String(length=2))
        

        def __init__(self, game_id, team, side, star_number, name, jersey_number):
                self.game_id = game_id
                self.team = team
                self.side = side
                self.star_number = star_number
                self.name = name
                self.jersey_number = jersey_number
                

class Coach(Base):
        __tablename__ = 'coaches'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=50))
        side = Column(String(length=4))
        role = Column(String(length=20))
        name = Column(String(length=50))

        def __init__(self, game_id, team, side, role, name):
                self.game_id = game_id
                self.team = team
                self.side = side
                self.role = role
                self.name = name


class Penalty_Statline(Base):
        __tablename__ = 'penalty_summaries'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=35))
        side = Column(String(length=4))
        pp_goals = Column(String(length=2))
        pp_opps = Column(String(length=2))
        pims = Column(String(length=4))
        infracs = Column(String(length=3))

        def __init__(self, game_id, team, side, pp_goals, pp_opps, pims, infracs):
                self.game_id = game_id
                self.team = team
                self.side = side
                self.pp_goals = pp_goals
                self.pp_opps = pp_opps
                self.pims = pims
                self.infracs = infracs


class Player_Scoreline(Base):
        __tablename__ = 'player_scorelines'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=35))
        side = Column(String(length=4))
        opponent = Column(String(length=35))
        jersey_number = Column(String(length=2))
        letter = Column(String(length=1))
        name = Column(String(length=50))
        player_id = Column(Integer)
        position = Column(String(length=2))
        goals = Column(String(length=2))
        assists = Column(String(length=2))
        pims = Column(String(length=3))
        shots = Column(String(length=2))
        plus_minus = Column(String(length=3))

        def __init__(self, game_id, team, side, opponent, jersey_number, letter, name, player_id, position, goals, assists, pims, shots, plus_minus):
                self.game_id = game_id
                self.team = team
                self.side = side
                self.opponent = opponent
                self.jersey_number = jersey_number
                self.letter = letter
                self.name = name
                self.player_id = player_id
                self.position = position
                self.goals = goals
                self.assists = assists
                self.pims = pims
                self.shots = shots
                self.plus_minus = plus_minus


class Top_Scorer(Base):
        __tablename__ = 'top_scorers'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=35))
        side = Column(String(length=4))
        player = Column(String(length=50))
        statline = Column(String(length=50))

        def __init__(self, game_id, team, side, player, statline):
                self.game_id = game_id
                self.team = team
                self.side = side
                self.player = player
                self.statline = statline


class Recent_Game(Base):
        __tablename__ = 'recent_games'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=35))
        side = Column(String(length=4))
        game_info = Column(String(length=50))

        def __init__(self, game_id, team, side, game_info):
                self.game_id = game_id
                self.team = team
                self.side = side
                self.game_info = game_info


class Matchup_Statline(Base):
        __tablename__ = 'matchup_statlines'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=35))
        side = Column(String(length=4))
        season_record = Column(String(length=15))
        last_10_games = Column(String(length=15))
        streak = Column(String(length=15))
        last_game = Column(String(length=75))
        home_record = Column(String(length=15))
        away_record = Column(String(length=15))
        goals_for = Column(Integer)
        goals_against = Column(Integer)
        power_plays = Column(String(length=20))
        power_plays_home = Column(String(length=20))
        power_plays_away = Column(String(length=20))
        penalty_killing = Column(String(length=20))
        penalty_killing_home = Column(String(length=20))
        penalty_killing_away = Column(String(length=20))
        
        def __init__(self, game_id, team, side, season_record, last_10_games, streak, last_game, home_record, away_record, goals_for, goals_against, power_plays, power_plays_home, power_plays_away, penalty_killing, penalty_killing_home, penalty_killing_away):
                self.game_id = game_id
                self.team = team
                self.side = side
                self.season_record = season_record
                self.last_10_games = last_10_games
                self.streak = streak
                self.last_game = last_game
                self.home_record = home_record
                self.away_record = away_record
                self.goals_for = goals_for
                self.goals_against = goals_against
                self.power_plays = power_plays
                self.power_plays_home = power_plays_home
                self.power_plays_away = power_plays_away
                self.penalty_killing = penalty_killing
                self.penalty_killing_home = penalty_killing_home
                self.penalty_killing_away = penalty_killing_away


class Head2Head_Statline(Base):
        __tablename__ = 'head2head_statlines'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=35))
        versus = Column(String(length=35))
        previous_season = Column(String(length=11))
        current_season = Column(String(length=11))
        last_5_seasons = Column(String(length=11))

        def __init__(self, game_id, team, versus, previous_season, current_season, last_5_seasons):
                self.game_id = game_id
                self.team = team
                self.versus = versus
                self.previous_season = previous_season
                self.current_season = current_season
                self.last_5_seasons = last_5_seasons


class Previous_Meeting(Base):
        __tablename__ = 'previous_meetings'

        id = Column(Integer, primary_key = True)#, autoincrement=True)
        game_id = Column(Integer)
        away_team = Column(String(length=35))
        away_score = Column(String(length=2))
        home_team = Column(String(length=35))
        home_score = Column(String(length=2))
        date = Column(Date)

        def __init__(self, game_id, away_team, away_score, home_team, home_score, date):
                self.game_id = game_id
                self.away_team = away_team
                self.away_score = away_score
                self.home_team = home_team
                self.home_score = home_score
                self.date = date


class Goalie_Change(Base):
        __tablename__ = 'goalie_changes'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        pbp_id = Column(String(length=4))
        event = Column(String(length=14))
        team = Column(String(length=35))
        side = Column(String(length=4))
        opponent = Column(String(length=35))
        goalie_number = Column(String(length=2))
        goalie_name = Column(String)
        action = Column(String(length=3))
        time = Column(Time)
        period = Column(String(length=4))

        def __init__(self, game_id, pbp_id, event, team, side, opponent, goalie_number, goalie_name, action, time, period):
                self.game_id = game_id
                self.pbp_id = pbp_id
                self.event = event
                self.team = team
                self.side = side
                self.opponent = opponent
                self.goalie_number = goalie_number
                self.goalie_name = goalie_name
                self.action = action
                self.time = time
                self.period = period


class Shot(Base):
        __tablename__ = 'shots'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        pbp_id = Column(String(length=4))
        event = Column(String(length=12))
        team = Column(String(length=35))
        side = Column(String(length=4))
        opponent = Column(String(length=35))
        team_manpower = Column(Integer)
        opponent_manpower = Column(Integer)
        state_certainty = Column(Boolean, default=True)
        player_number = Column(String(length=2))
        player_name = Column(String(length=50))
        goalie_number = Column(String(length=2), default=None)
        goalie_name = Column(String(length=50))
        time = Column(Time)
        period = Column(String(length=4))
        result = Column(String(length=4), default="")

        def __init__(self, game_id, pbp_id, event, team, side, opponent, team_manpower, opponent_manpower, state_certainty, player_number, player_name, goalie_name, time, period, goalie_number=None, result=""):
                self.game_id = game_id
                self.pbp_id = pbp_id
                self.event = event
                self.team = team
                self.side = side
                self.opponent = opponent
                self.team_manpower = team_manpower
                self.opponent_manpower = opponent_manpower
                self.state_certainty = state_certainty
                self.player_number = player_number
                self.player_name = player_name
                self.goalie_number = goalie_number
                self.goalie_name = goalie_name
                self.time = time
                self.period = period
                self.result = result


class Penalty_Call(Base):
        __tablename__ = 'penalties'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        pbp_id = Column(String(length=4))
        event = Column(String(length=7))
        team = Column(String(length=35))
        side = Column(String(length=4))
        opponent = Column(String(length=35))
        team_manpower = Column(Integer)
        opponent_manpower = Column(Integer)
        player_number = Column(String(length=2))
        player_name = Column(String(length=50))
        penalty = Column(String(length=100))
        pim = Column(String(length=2))
        pp = Column(String(length=2))
        time = Column(Time)
        period = Column(String(length=3))

        def __init__(self, game_id, pbp_id, event, team, side, opponent, team_manpower, opponent_manpower, player_number, player_name, penalty, pim, pp, time, period):
                self.game_id = game_id
                self.pbp_id = pbp_id
                self.event = event
                self.team = team
                self.side = side
                self.opponent = opponent
                self.team_manpower = team_manpower
                self.opponent_manpower = opponent_manpower
                self.player_number = player_number
                self.player_name = player_name
                self.penalty = penalty
                self.pim = pim
                self.pp = pp
                self.time = time
                self.period = period


class Goal(Base):
        __tablename__ = 'goals'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        pbp_id = Column(String(length=4))
        event = Column(String(length=4))
        team = Column(String(length=35))
        side = Column(String(length=4))
        opponent = Column(String(length=35))
        team_manpower = Column(Integer)
        opponent_manpower = Column(Integer)
        player_number = Column(String(length=2))
        player_name = Column(String(length=50))
        season_total = Column(String(length=3))
        time = Column(Time)
        period = Column(String(length=3))
        assist1_number = Column(String(length=2), default=None)
        assist1_name = Column(String(length=50), default=None)
        assist1_total = Column(String(length=3), default=None)
        assist2_number = Column(String(length=2), default=None)
        assist2_name = Column(String(length=50), default=None)
        assist2_total = Column(String(length=3), default=None)
        ppg = Column(Boolean, default=False)
        shg = Column(Boolean, default=False)
        eng = Column(Boolean, default=False)
        gwg = Column(Boolean, default=False)
        insurance = Column(Boolean, unique=False, default=False)
        psg = Column(Boolean, unique=False, default=False)

        def __init__(self, game_id, pbp_id, event, team, side, opponent, team_manpower, opponent_manpower, player_number, player_name, season_total, time, period, assist1_number=None, assist1_name=None, assist1_total=None, assist2_number=None, assist2_name=None, assist2_total=None, ppg=False, shg=False, eng=False, gwg=False, insurance=False, psg=False):
                self.game_id = game_id
                self.pbp_id = pbp_id
                self.event = event
                self.team = team
                self.side = side
                self.opponent = opponent
                self.team_manpower = team_manpower
                self.opponent_manpower = opponent_manpower
                self.player_number = player_number
                self.player_name = player_name
                self.season_total = season_total
                self.time = time
                self.period = period
                self.assist1_number = assist1_number
                self.assist1_name = assist1_name
                self.assist1_total = assist1_total
                self.assist2_number = assist2_number
                self.assist2_name = assist2_name
                self.assist2_total = assist2_total
                self.ppg = ppg
                self.shg = shg
                self.eng = eng
                self.gwg = gwg
                self.insurance = insurance
                self.psg = psg


class Onice_Event(Base):
        __tablename__ = 'onice_events'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        pbp_id = Column(String(length=4))
        event = Column(String(length=5))
        side = Column(String(length=4))
        team = Column(String(length=35))
        opponent = Column(String(length=35))
        player_number = Column(String(length=2))
        player_name = Column(String(length=50))
        plus_minus = Column(String(length=2))
        time = Column(Time)
        period = Column(String(length=3))
 
        def __init__(self, game_id, pbp_id, event, team, side, opponent, player_number, player_name, plus_minus, time, period):
                self.game_id = game_id 
                self.pbp_id = pbp_id
                self.event = event
                self.team = team
                self.side = side
                self.opponent = opponent
                self.player_number = player_number
                self.player_name = player_name
                self.plus_minus = plus_minus
                self.time = time
                self.period = period


class Shootout_Attempt(Base):
        __tablename__ = 'shootout_attempts'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        pbp_id = Column(String(length=4))
        event = Column(String(length=16))
        team = Column(String(length=35))
        side = Column(String(length=4))
        opponent = Column(String(length=35))
        player_number = Column(String(length=2))
        player_name = Column(String(length=50))
        goalie_number = Column(String(length=2))
        goalie_name = Column(String(length=50))
        result = Column(String(length=7))
        period = Column(String(length=3))
        gwg = Column(Boolean, default=False)

        def __init__(self, game_id, pbp_id, event, team, side, opponent, player_number, player_name, goalie_number, goalie_name, result, period, gwg=False):
                self.game_id = game_id
                self.pbp_id = pbp_id
                self.event = event
                self.team = team
                self.side = side
                self.opponent = opponent
                self.player_number = player_number
                self.player_name = player_name
                self.goalie_number = goalie_number
                self.goalie_name = goalie_name
                self.result = result
                self.period = period
                self.gwg = gwg


class Pin(Base):
        __tablename__ = 'pins'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        pbp_id = Column(String(length=4))
        pin_id = Column(String(length=4))
        event = Column(String(length=4))
        team = Column(String(length=35))
        side = Column(String(length=4))
        opponent = Column(String(length=35))
        top_position = Column(Float)
        left_position = Column(Float)
        player_number = Column(String(length=2))
        player_name = Column(String(length=50))
        goalie_number = Column(String(length=2), default=None)
        goalie_name = Column(String(length=50))
        time = Column(Time)
        period = Column(String(length=3))
        result = Column(String(length=4), default="")
 
        def __init__(self, game_id, pbp_id, pin_id, event, team, side, opponent, top_position, left_position, player_number, player_name, goalie_name, time, period, goalie_number=None, result=""):  
                self.game_id = game_id
                self.pbp_id = pbp_id
                self.pin_id = pin_id
                self.event = event
                self.team = team
                self.side = side
                self.opponent = opponent
                self.top_position = top_position
                self.left_position = left_position
                self.player_number = player_number
                self.player_name = player_name
                self.goalie_number = goalie_number
                self.goalie_name = goalie_name
                self.time = time
                self.period = period
                self.result = result



 
        # def __init__(self, game_id, event, result, side, team, top_position, left_position, player_number, player_name, goalie_number, goalie_name, time, period):  
        #         self.game_id = game_id
        #         self.event = event
        #         self.result = result
        #         self.side = side
        #         self.team = team
        #         self.top_position = top_position
        #         self.left_position = left_position
        #         self.player_number = player_number
        #         self.player_name = player_name
        #         self.goalie_number = goalie_number
        #         self.goalie_name = goalie_name
        #         self.time = time
        #         self.period = period


def db_commit(game):
        thismodule = sys.modules[__name__]

        if "_missing_games" in vars(game):
                for game in game._missing_games:
                        session.add(getattr(thismodule, "missing_games")(**game))
        else:
                for key in vars(game):
                        if isinstance(vars(game)[key], list) and key[:1] == "_":
                                for item in vars(game)[key]:
                                        tbl_name = key[1:].replace("_"," ").title().replace(" ","_")[:-1] if key != "_coaches" else "Coach"
                                        session.add(getattr(thismodule, tbl_name)(**item))
        print(f'Game #{vars(game)["_game_id"]}: committing {len(session.new)} rows to database.')
        session.commit()

def get_last_game_in_db():#session, meta):
        
        query1 = session.query(func.max(Game.game_id))
        query2 = session.query(func.max(Missing_Game.game_id))

        last_game = max(int(query1.first()[0] or 0), int(query2.first()[0] or 0))

        return last_game

def drop_all_tables():
        
        Base.metadata.drop_all(bind=engine)

#run when module is loaded
Base, engine, session, meta = connect()
atexit.register(lambda: session.close())
atexit.register(lambda: engine.dispose())

#run if module is main
if __name__ == "__main__":
        # pass
        drop_all_tables()
        # print("All tables in database have been dropped.")
