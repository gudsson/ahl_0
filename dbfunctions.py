# import scrapers
# from sqlalchemy import create_engine

import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Time, Date, MetaData, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connect to the db
# conn = psycopg2.connect(
#         host = "localhost",
#         database = "AHLdb",
#         user="postgres",
#         password="Olafur84!"
# )

# Base = declarative_base()

# engine = create_engine(
#     "postgresql+psycopg2://postgres:Olafur84!@localhost/AHLdb",
#     executemany_mode='batch')
Base = declarative_base()

# class Games(Base):
def connect():
        

        engine = create_engine(
        "postgresql+psycopg2://postgres:Olafur84!@localhost/AHLdb",
        executemany_mode='batch')


        Session = sessionmaker(bind=engine)
        session = Session()
        meta = MetaData()
        Base.metadata.create_all(engine)

        return engine, session

class Game(Base):
        __tablename__ = 'games'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        game_number = Column(String(length=4))
        dow = Column(String(length=9))
        date = Column(Date)
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
        
        def __init__(self, game_id, game_number, dow, date, status, away_team, away_score, home_score, home_team, venue, attendance, start_time, end_time, duration): 
                self.game_id = game_id
                self.game_number = game_number
                self.dow = dow
                self.date = date
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
        star_number = Column(String(length=3))
        name = Column(String)
        jersey_number = Column(String(length=2))
        team = Column(String)

        def __init__(self, game_id, star_number, name, jersey_number, team):
                self.game_id = game_id
                self.star_number = star_number
                self.name = name
                self.jersey_number = jersey_number
                self.team = team


class Coach(Base):
        __tablename__ = 'coaches'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        role = Column(String)
        name = Column(String)

        def __init__(self, game_id, team, role, name):
                self.game_id = game_id
                self.team = team
                self.role = role
                self.name = name


class Penalty_Summary(Base):
        __tablename__ = 'penalty_summaries'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=4))
        pp_goals = Column(String(length=2))
        pp_opps = Column(String(length=2))
        pims = Column(String(length=4))
        infracs = Column(String(length=3))

        def __init__(self, game_id, team, pp_goals, pp_opps, pims, infracs):
                self.game_id = game_id
                self.team = team
                self.pp_goals = pp_goals
                self.pp_opps = pp_opps
                self.pims = pims
                self.infracs = infracs


class Player_Scoreline(Base):
        __tablename__ = 'player_scorelines'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        jersey_number = Column(String(length=2))
        letter = Column(String(length=1))
        name = Column(String)
        player_id = Column(Integer)
        position = Column(String(length=2))
        goals = Column(String(length=2))
        assists = Column(String(length=2))
        pims = Column(String(length=3))
        shots = Column(String(length=2))
        plus_minus = Column(String(length=3))

        def __init__(self, game_id, team, jersey_number, letter, name, player_id, position, goals, assists, pims, shots, plus_minus):
                self.game_id = game_id
                self.team = team
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
        team = Column(String)
        player = Column(String)
        statline = Column(String)

        def __init__(self, game_id, team, player, statline):
                self.game_id = game_id
                self.team = team
                self.player = player
                self.statline = statline


class Recent_Game(Base):
        __tablename__ = 'recent_games'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        game_info = Column(String)

        def __init__(self, game_id, team, game_info):
                self.game_id = game_id
                self.team = team
                self.game_info = game_info


class Matchup_Statline(Base):
        __tablename__ = 'matchup_statlines'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        season_record = Column(String)
        last_10 = Column(String)
        streak = Column(String)
        last_game = Column(String)
        home_record = Column(String)
        away_record = Column(String)
        goals_for = Column(Integer)
        goals_against = Column(Integer)
        pp = Column(String)
        pp_home = Column(String)
        pp_away = Column(String)
        pk = Column(String)
        pk_home = Column(String)
        pk_away = Column(String)
        
        def __init__(self, game_id, team, last_10, streak, last_game, home_record, away_record, goals_for, goals_against, pp, pp_home, pp_away, pk, pk_home, pk_away):
                self.game_id = game_id
                self.team = team
                self.last_10 = last_10
                self.streak = streak
                self.last_game = last_game
                self.home_record = home_record
                self.away_record = away_record
                self.goals_for = goals_for
                self.goals_against = goals_against
                self.pp = pp
                self.pp_home = pp_home
                self.pp_away = pp_away
                self.pk = pk
                self.pk_home = pk_home
                self.pk_away = pk_away


class Head2Head_Statline(Base):
        __tablename__ = 'head2head_statlines'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        previous_season = Column(String)
        current_season = Column(String)
        last_5_seasons = Column(String)

        def __init__(self, game_id, team, previous_season, current_season, last_5_seasons):
                self.game_id = game_id
                self.team = team
                self.previous_season = previous_season
                self.current_season = current_season
                self.last_5_seasons = last_5_seasons


class Previous_Meeting(Base):
        __tablename__ = 'previous_meetings'

        id = Column(Integer, primary_key = True)#, autoincrement=True)
        game_id = Column(String(length=5))
        away_team = Column(String(length=50))
        away_score = Column(String(length=2))
        home_team = Column(String(length=50))
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
        event = Column(String)
        side = Column(String(length=7))
        team = Column(String)
        goalie_number = Column(String(length=2))
        goalie_name = Column(String)
        action = Column(String(length=3))
        time = Column(Time)
        period = Column(String(length=3))

        def __init__(self, game_id, event, side, team, goalie_number, goalie_name, action, time, period):
                self.game_id = game_id
                self.event = event
                self.side = side
                self.team = team
                self.goalie_number = goalie_number
                self.goalie_name = goalie_name
                self.action = action
                self.time = time
                self.period = period


class Shot(Base):
        __tablename__ = 'shots'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        event = Column(String(length=4))
        result = Column(String(length=4))
        side = Column(String(length=7))
        team = Column(String)
        player_number = Column(String(length=2))
        player_name = Column(String)
        goalie_number = Column(String(length=2))
        goalie_name = Column(String)
        time = Column(Time)
        period = Column(String(length=3))

        def __init__(self, game_id, event, side, team, goalie_number, goalie_name, action, time, period):
                self.game_id = game_id
                self.event = event
                self.result = result
                self.side = side
                self.team = team
                self.player_number = player_number
                self.player_name = player_name
                self.goalie_number = goalie_number
                self.goalie_name = goalie_name
                self.time = time
                self.period = period


class Penalty(Base):
        __tablename__ = 'penalties'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        event = Column(String(length=7))
        side = Column(String(length=7))
        team = Column(String)
        player_number = Column(String(length=2))
        player_name = Column(String)
        penalty = Column(String(length=2))
        pim = Column(String(length=2))
        pp = Column(String(length=2))
        Time = Column(Time)
        period = Column(String(length=3))

        def __init__(self, game_id, event, side, team, player_number, player_name, penalty, pim, pp, time, period):
                self.game_id = game_id
                self.event = event
                self.side = side
                self.team = team
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
        event = Column(String(length=4))
        side = Column(String(length=7))
        team = Column(String)
        player_number = Column(String(length=2))
        player_name = Column(String)
        season_total = Column(String(length=3))
        assist1_number = Column(String(length=2))
        assist1_name = Column(String)
        assist1_total = Column(String(length=3))
        assist2_number = Column(String(length=2))
        assist2_name = Column(String)
        assist2_total = Column(String(length=3))
        Time = Column(Time)
        period = Column(String(length=3))
        ppg = Column(String)
        shg = Column(String)
        eng = Column(String)
        gwg = Column(String)
        gtg = Column(String)

        def __init__(self, game_id, event, side, team, player_number, player_name, season_total, assist1_number, assist1_name, assist1_total, assist2_number, assist2_name, assist2_total, time, period, ppg, shg, eng, gwg, gtg):
                self.game_id = game_id
                self.event = event
                self.side = side
                self.team = team
                self.player_number = player_number
                self.player_name = player_name
                self.season_total = season_total
                self.assist1_number = assist1_number
                self.assist1_name = assist1_name
                self.assist1_total = assist1_total
                self.assist2_number = assist2_number
                self.assist2_name = assist2_name
                self.assist2_total = assist2_total
                self.time = time
                self.period = period
                self.ppg = ppg
                self.shg = shg
                self.eng = eng
                self.gwg = gwg
                self.gtg = gtg


class Onice_Event(Base):
        __tablename__ = 'onice_events'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        event = Column(String(length=5))
        side = Column(String(length=7))
        team = Column(String)
        player_number = Column(String(length=2))
        player_name = Column(String)
        plus_minus = Column(String(length=2))
        Time = Column(Time)
        period = Column(String(length=3))
 
        def __init__(self, game_id, event, side, team, player_number, player_name, plus_minus, time, period):
                self.game_id = game_id 
                self.event = event
                self.side = side
                self.team = team
                self.player_number = player_number
                self.player_name = player_name
                self.plus_minus = plus_minus
                self.time = time
                self.period = period


class Pin(Base):
        __tablename__ = 'pins'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        event = Column(String(length=5))
        result = Column(String(length=4))
        side = Column(String(length=7))
        team = Column(String)
        top_position = Column(Float)
        left_position = Column(Float)
        player_number = Column(String(length=2))
        player_name = Column(String)
        goalie_number = Column(String(length=2))
        goalie_name = Column(String)
        Time = Column(Time)
        period = Column(String(length=3))
 
        def __init__(self, game_id, event, result, side, team, top_position, left_position, player_number, player_name, goalie_number, goalie_name, time, period):  
                self.game_id = game_id
                self.event = event
                self.result = result
                self.side = side
                self.team = team
                self.top_position = top_position
                self.left_position = left_position
                self.player_number = player_number
                self.player_name = player_name
                self.goalie_number = goalie_number
                self.goalie_name = goalie_name
                self.time = time
                self.period = period

# create a cursor
# c = conn.cursor()

def get_last_game_in_db(session, meta):
        
        query = session.query(func.max(Game.game_id))

        # for _res in query.all():
        #         print(_res)

        print(query.first()[0])

def get_last_meeting(session, meta):
        
        query = session.query(func.max(Previous_Meeting.game_id))

        # for _res in query.all():
        #         print(_res)

        print(query.first()[0])


# def create_table(engine, meta):
        

#         # c.execute("CREATE TABLE TEAMS (id int, location varchar(255), team_name varchar(255))")

#         # conn.commit()

#         new_table = Table(
#                 'officials', meta, 
#                 Column('id', Integer, primary_key = True),
#                 Column('game_id', Integer),

#         )


#         #         test_table = Table(
#         #         'games', meta, 
#         #         Column('id', Integer, primary_key = True),
#         #         Column('game_id', Integer),
#         #         Column('game_number', Integer),
#         #         Column('dow', String),
#         #         Column('date', Date),
#         #         Column('status', String),
#         #         Column('away_team', String),
#         #         Column('away_score', Integer), 
#         #         Column('home_score', Integer), 
#         #         Column('home_team', String), 
#         #         Column('venue', String), 
#         #         Column('attendance', Integer), 
#         #         Column('start_time', String), 
#         #         Column('end_time', String),
#         #         Column('duration', Time), 
#         # )

#         meta.create_all(engine)

# create_table(engine, meta)

# create_table(engine)


# Session = sessionmaker(bind=engine)
# session = Session()
# meta = MetaData()
# Base.metadata.create_all(engine)


# previous_mtg = Previous_Meeting(game_id=69, away_team='Toronto Marlies', away_score=5, home_team='Utica Comets', home_score=4, date='March 26, 2020')

# # get_last_meeting(session, meta)

# session.add(previous_mtg)


# # print(session.new)

# session.commit()
# # # Create 
# # doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")  
# # session.add(doctor_strange)  
# # session.commit()

# # # Read
# # films = session.query(Film)  
# # for film in films:  
# #     print(film.title)

# # # Update
# # doctor_strange.title = "Some2016Film"  
# # session.commit()

# # # Delete
# # session.delete(doctor_strange)  
# # session.commit()  





# # game = Game(game_id=7682145, game_number=989, dow="Tuesday", date="March 10, 2020", status="Final", away_team="San Jose Barracuda", away_score="7", home_score="4", home_team="Stockton Heat", venue="Stockton Arena", attendance=1639, start_time="7:01 pm", end_time="9:16 pm")
# # session.add(game)
# # session.commit()

# session.close()
# engine.dispose()

# c.execute("select * from Teams")

# c.commit()

# rows = c.fetchall()

# for r in rows:
#     print(f"id {r[0]} location {r[1]} name {r[2]}")

# c.execute('''SELECT * FROM public."TEAMS_test"''')

# c.fetchall()

# c.execute("""SELECT table_name FROM information_schema.tables
#        WHERE table_schema = 'public'""")
# for table in c.fetchall():
#     print(table)



# close the cursor
# c.close()

# # close the connection
# conn.close()

# if __name__ == "__main__":
#     print("hello World")