# import scrapers
# from sqlalchemy import create_engine

import psycopg2

# connect to the db
conn = psycopg2.connect(
        host = "localhost",
        database = "AHLdb",
        user="postgres",
        password="Olafur84!"
)

# create a cursor
c = conn.cursor()

c.execute("CREATE TABLE TEAMS (id int, location varchar(255), team_name varchar(255))")

conn.commit()


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
c.close()

# close the connection
conn.close()

# if __name__ == "__main__":
#     print("hello World")