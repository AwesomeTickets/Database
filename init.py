#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import os
import random

DB_HOST = 'localhost'
DB_NAME = 'awesome_tickets'
DB_USER = 'root'
DB_PSWD = '123456'
DB_CHARSET = 'utf8'
DB_CONN_SOCKET = '/var/run/mysqld/mysqld.sock'
GEN_RAND_SOLD_SEATS = False
TEST_SHOW_DATE = ['2017-05-01', '2017-05-02', '2017-05-03']
TEST_SHOW_TIME = ['10:05:00', '13:20:00', '16:35:00', '19:50:00', '22:05:00']
TEST_PRICE = [20.5, 22.5, 28, 35, 37, 41.5]
TEST_PHONE = '18813572468'

os.system("mysql --default-character-set=%s -u%s -p%s"
          % (DB_CHARSET, DB_USER, DB_PSWD) +
          "< ./sql/create_db.sql")
os.system("mysql --default-character-set=%s -D%s -u%s -p%s"
          % (DB_CHARSET, DB_NAME, DB_USER, DB_PSWD) +
          "< ./sql/create_table.sql")
os.system("mysql --default-character-set=%s -D%s -u%s -p%s"
          % (DB_CHARSET, DB_NAME, DB_USER, DB_PSWD) +
          "< ./sql/insert_data.sql")

conn = pymysql.connect(host=DB_HOST,
                       user=DB_USER,
                       password=DB_PSWD,
                       db=DB_NAME,
                       charset=DB_CHARSET,
                       unix_socket=DB_CONN_SOCKET)

try:
    with conn.cursor() as cursor:

        # Print database info
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print("MySQL version: %s" % data)

        print("Finding available movies...")
        cursor.execute("""
            SELECT movie_id, country_name
            FROM (Movie NATURAL JOIN MovieStatus) NATURAL JOIN Country
            WHERE status_name='on'
        """)
        movies = []
        for entry in cursor.fetchall():
            entry = list(entry)
            if (entry[1] != u"中国"):
                entry[1] = u"英语"
            else:
                entry[1] = u"国语"
            movies.append(entry)
        print("movies amount:", len(movies))

        print("Finding available cinema halls...")
        cursor.execute("""
            SELECT cinema_hall_id
            FROM CinemaHall
        """)
        cinema_hall_ids = []
        for entry in cursor.fetchall():
            cinema_hall_ids.append(entry[0])
        print("cinema_hall amount:", len(cinema_hall_ids))

        print("Adding on show movies...")
        candidate_movies = []
        for cinema_hall_id in cinema_hall_ids:
            for date in TEST_SHOW_DATE:
                for time in TEST_SHOW_TIME:
                    if (len(candidate_movies) == 0):
                        candidate_movies = list(movies)
                    pos = random.randrange(len(candidate_movies))
                    movie = candidate_movies.pop(pos)
                    price = TEST_PRICE[random.randrange(
                        len(TEST_PRICE))]
                    cursor.execute("""
                        INSERT INTO MovieOnShow
                        (movie_id, cinema_hall_id, lang,
                         show_date, show_time, price)
                        VALUES (%d, %d, '%s', '%s', '%s', %f)
                    """ % (movie[0], cinema_hall_id, movie[1],
                           date, time, price))

        print("Adding seats...")
        cursor.execute("""
            SELECT movie_on_show_id, seat_layout
            FROM MovieOnShow NATURAL JOIN CinemaHall
        """)
        for entry in cursor.fetchall():
            movie_on_show_id = entry[0]
            seat_layout = entry[1]
            seat_rows = seat_layout.split(',')
            for i, row in enumerate(seat_rows):
                col = 1
                for char in row:
                    if GEN_RAND_SOLD_SEATS:
                        available = random.randrange(5)
                    else:
                        available = 1
                    if (char != '0'):
                        cursor.execute("""
                            INSERT INTO Seat
                            (movie_on_show_id, row, col, available)
                            VALUES (%d, %d, %d, %d)
                        """ % (movie_on_show_id, i + 1, col, available))
                        col += 1

        print("Adding test users...")
        cursor.execute("""
            INSERT INTO User (phone_num, password, remain_purchase)
            VALUES ('%s', '', %d)
        """ % (TEST_PHONE, 0))

    conn.commit()
    print("Done.")
finally:
    conn.close()
