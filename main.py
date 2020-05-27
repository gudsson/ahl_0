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

Base = declarative_base()

engine = create_engine(
    "postgresql+psycopg2://postgres:Olafur84!@localhost/AHLdb",
    executemany_mode='batch')


# class Games(Base):


class Game(Base):
        __tablename__ = 'games'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        game_number = Column(Integer)
        dow = Column(String)
        date = Column(Date)
        status = Column(String)
        away_team = Column(String)
        away_score = Column(Integer)
        home_score = Column(Integer)
        home_team = Column(String)
        venue = Column(String)
        attendance = Column(Integer)
        start_time = Column(String)
        end_time = Column(String)
        duration = Column(Time)
        
        def __repr__(self):
                return "<Game(id='%i', game_id='%i', game_number='%i', dow='%s', date='%d', status='%s', away_team='%s', away_score='%i', home_score='%i', home_team='%s', venue='%s', attendance='%i', start_time='%s', end_time='%s', duration='%t')>" % (
                        self.game_id, self.game_number, self.dow, self.date, self.status, self.away_team, self.away_score, self.home_score, self.home_team, self.venue, self.attendance, self.start_time, self.end_time, self.duration)


class Official(Base):
        __tablename__ = 'officials'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        name = Column(String)
        number = Column(Integer)
        role = Column(Integer)

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', name='%s', number='%i', role='%s')>" % (
                        self.id, self.game_id, self.name, self.number, self.role)


class Boxscore(Base):
        __tablename__ = 'boxscores'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        period = Column(String(length=2))
        home_goals = Column(String(length=2))
        away_goals = Column(String(length=2))
        home_shots = Column(String(length=3))
        away_shots = Column(String(length=3))

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', period='%s', home_goals='%s', away_goals='%s', home_shots='%s', away_shots='%s')>" % (
                        self.id, self.game_id, self.period, self.home_goals, self.away_goals, self.home_shots, self.away_shots)


class Star(Base):
        __tablename__ = 'stars'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        star_number = Column(String(length=3))
        name = Column(String)
        jersey_number = Column(String(length=2))
        team = Column(String)

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', star_number='%s', name='%s', jersey_number='%s', team='%s')>" % (
                        self.id, self.game_id, self.star_number, self.name, self.jersey_number, self.team)


class Coach(Base):
        __tablename__ = 'coaches'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        role = Column(String)
        name = Column(String)

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', team='%s', role='%s', name='%s')>" % (
                        self.id, self.game_id, self.team, self.role, self.name)


class Penalty_Summary(Base):
        __tablename__ = 'penalty_summaries'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String(length=4))
        pp_goals = Column(String(length=2))
        pp_opps = Column(String(length=2))
        pims = Column(String(length=4))
        infracs = Column(String(length=3))

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', team='%s', pp_goals='%s', pp_opps='%s', pims='%s', infracs='%s')>" % (
                        self.id, self.game_id, self.team, self.pp_goals, self.pp_opps, self.pims, self.infracs)


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


        def __repr__(self):
                return "<Game(id='%i', game_id='%i', team='%s', jersey_number='%s', letter='%s', name='%s', player_id='%i', position='%s', goals='%s', assists='%s', pims='%s', shots='%s', plus_mins='%s')>" % (
                        self.id, self.game_id, self.team, self.jersey_number, self.letter, self.name, self.player_id, self.position, self.goals, self.assists, self.pims, self.shots, self.plus_minus)


class Top_Scorer(Base):
        __tablename__ = 'top_scorers'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        player = Column(String)
        statline = Column(String)

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', team='%s', player='%s', statline='%s')>" % (
                        self.id, self.game_id, self.team, self.player, self.statline)


class Recent_Game(Base):
        __tablename__ = 'recent_games'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        game_info = Column(String)

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', team='%s', game_info='%s')>" % (
                        self.id, self.game_id, self.team, self.game_info)


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
        
        def __repr__(self):
                return "<Game(id='%i', game_id='%i', team='%s', last_10='%s', streak='%s', last_game='%s', home_record='%s', away_record='%s', goals_for='%i', goals_against='%i', pp='%s', pp_home='%s', pp_away='%s', pk='%s', pk_home='%s', pk_away='%s')>" % (
                        self.id, self.game_id, self.team, self.last_10, self.streak, self.last_game, self.home_record, self.away_record, self.goals_for, self.goals_against, self.pp, self.pp_home, self.pp_away, self.pk, self.pk_home, self.pk_away)


class Head2Head_Statline(Base):
        __tablename__ = 'head2head_statlines'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        team = Column(String)
        previous_season = Column(String)
        current_season = Column(String)
        last_5_seasons = Column(String)

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', team='%s', previous_season='%s', current_season='%s', last_5_seasons='%s')>" % (
                        self.id, self.game_id, self.team, self.previous_season, self.current_season, self.last_5_seasons)


class Previous_Meeting(Base):
        __tablename__ = 'previous_meetings'

        id = Column(Integer, primary_key = True)
        game_id = Column(Integer)
        away_team = Column(String)
        away_score = Column(String(length=2))
        home_team = Column(String)
        home_score = Column(String(length=2))
        date = Column(Date)

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', away_team='%s', away_score='%s', home_team='%s', home_score='%s', date='%d')>" % (
                        self.id, self.game_id, self.team, self.previous_season, self.current_season, self.last_5_seasons)


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

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', event='%s', side='%s', team='%s', goalie_number='%s', goalie_name='%s', action='%s', time='%t', period='%s')>" % (
                        self.id, self.game_id, self.event, self.side, self.team, self.goalie_number, self.goalie_name, self.action, self.time, self.period)


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

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', event='%s', result='%s', side='%s', team='%s', player_number='%s', player_name='%s', goalie_number='%s', goalie_name='%s', time='%t', period='%s')>" % (
                        self.id, self.game_id, self.event, self.result, self.side, self.team, self.player_number, self.player_name, self.goalie_number, self.goalie_name, self.time, self.period)


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

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', event='%s', side='%s', team='%s', player_number='%s', player_name='%s', penalty='%s', pim='%s', pp='%s', time='%t', period='%s')>" % (
                        self.id, self.game_id, self.event, self.side, self.team, self.player_number, self.player_name, self.penalty, self.pim, self.pp, self.time, self.period)


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

        def __repr__(self):
                return "<Game(id='%i', game_id='%i', event='%s', side='%s', team='%s', player_number='%s', player_name='%s', season_total='%s', assist1_number='%s', assist1_name='%s', assist1_total='%s', assist2_number='%s', assist2_name='%s', assist2_total='%s', time='%t', period='%s', ppg='%s', shg='%s', eng='%s', gwg='%s', gtg='%s')>" % (
                        self.id, self.game_id, self.event, self.side, self.team, self.player_number, self.player_name, self.season_total, self.assist1_number, self.assist1_name, self.assist1_total, self.assist2_number, self.assist2_name, self.assist2_total, self.time, self.period, self.ppg, self.shg, self.eng, self.gwg, self.gtg)


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
 
        def __repr__(self):
                return "<Game(id='%i', game_id='%i', event='%s', side='%s', team='%s', player_number='%s', player_name='%s', plus_minus='%s', time='%t', period='%s')>" % (
                        self.id, self.game_id, self.event, self.side, self.team, self.player_number, self.player_name, self.plus_minus, self.time, self.period)


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
 
        def __repr__(self):
                return "<Game(id='%i', game_id='%i', event='%s', result='%s', side='%s', team='%s', top_position='%f', left_position='%f', player_number='%s', player_name='%s', goalie_number='%s', goalie_name='%s', time='%t', period='%s')>" % (
                        self.id, self.game_id, self.event, self.result, self.side, self.team, self.top_position, self.left_position, self.player_number, self.player_name, self.goalie_number, self.goalie_name, self.time, self.period)


# create a cursor
# c = conn.cursor()

def get_last_game_in_db(session, meta):
        
        query = session.query(func.max(Game.game_id))

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
# get_last_game_in_db(session, meta)

Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()
Base.metadata.create_all(engine)


previous_mtg = Previous_Meeting(game_id=69, away_team='Toronto Marlies', away_score='5', home_team='Utica Comets', home_score='4', date='March 26, 2020')
session.add(previous_mtg)
session.commit
# # Create 
# doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")  
# session.add(doctor_strange)  
# session.commit()

# # Read
# films = session.query(Film)  
# for film in films:  
#     print(film.title)

# # Update
# doctor_strange.title = "Some2016Film"  
# session.commit()

# # Delete
# session.delete(doctor_strange)  
# session.commit()  





# game = Game(game_id=7682145, game_number=989, dow="Tuesday", date="March 10, 2020", status="Final", away_team="San Jose Barracuda", away_score="7", home_score="4", home_team="Stockton Heat", venue="Stockton Arena", attendance=1639, start_time="7:01 pm", end_time="9:16 pm")
# session.add(game)
# session.commit()

session.close()
engine.dispose()

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