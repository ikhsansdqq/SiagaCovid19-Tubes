import os
import psycopg2

conn = psycopg2.connect (
    host = "localhost",
    database = "siagacovid",
    user = os.environ['postgres'],
    password = os.environ['12345']
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS siagacovid;")
cur.execute('CREATE TABLE siagacovid ()')