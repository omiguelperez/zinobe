import os
import sqlite3
from datetime import datetime
from sqlite3.dbapi2 import Error


def get_connection():
    connection = sqlite3.connect('out/db.sqlite3')
    return connection


def migrate_countrydata_table(con):
    c = con.cursor()
    try:
        c.execute("CREATE TABLE IF NOT EXISTS zinobe_countrydata (country_name text, city_name text, language text, time real, created_at datetime)")
        con.commit()
    except Error:
        print('There was an error creating countrydata table')


def save_countrydata_rows(rows):
    for row in rows:
        conn.execute(f'INSERT INTO zinobe_countrydata (country_name, city_name, language, time, created_at) VALUES (?, ?, ?, ?, ?)', (row['country_name'], row['city_name'], row['language'], row['time'], datetime.now()))
        conn.commit()


conn = get_connection()
migrate_countrydata_table(conn)
