import psycopg2
import csv
conn = psycopg2.connect(
    "host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=    dc4ua1h8pt5m05 user=pxondfbtekevjh password=eb9a343232a10bb904c71b3c94669edcaad8f15e77796d4e9f47543b885ed875")


cur = conn.cursor()
# cur.execute("""DROP TABLE users""")

# cur.execute("""CREATE TABLE users (id SERIAL PRIMARY KEY, username varchar(20) NOT NULL, password varchar(20) NOT NULL)""")
# insert_query = "INSERT INTO users  (username, password) VALUES ('admin','123passhaha')"
# cur.execute(insert_query)
# # print("pr1: ", cur.fetchall())
# insert_query = "INSERT INTO users  (username, password) VALUES ('mikewaz','testpass')"
# cur.execute(insert_query)
cur.execute("""SELECT * from users """)
print("pritn2 ", cur.fetchall())

conn.commit()
# cur.execute("""
#     CREATE TABLE users(
#     id integer PRIMARY KEY,
#     username text,
#     password text
# )
# """)
# insert_query = "INSERT INTO users VALUES {}".format(
#     "(1, 'admin', '12345pass')")
# cur.execute(insert_query)
# cur.execute('SELECT * FROM books limit 100')
