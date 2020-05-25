# import scrapers
# from sqlalchemy import create_engine

import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, Time, Date, MetaData, select, func
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