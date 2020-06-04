import psycopg2
import csv
conn = psycopg2.connect(
    "host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=    dc4ua1h8pt5m05 user=pxondfbtekevjh password=eb9a343232a10bb904c71b3c94669edcaad8f15e77796d4e9f47543b885ed875")


cur = conn.cursor()
cur.execute("""
    CREATE TABLE books(
    isbn text PRIMARY KEY,
    title text,
    author text,
    year integer
)
""")
with open('books.txt', 'r') as f:
    next(f)  # Skip the header row.
    cur.copy_from(f, 'books', sep='\t')

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
conn.commit()
