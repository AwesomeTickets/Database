#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql as mdb
import os
import random
import hashlib

DB_NAME = 'awesome_tickets'
USER = 'root'
PSWD = '123456'
GEN_SOLD_SEATS = True
TEST_SHOW_DATE = ['2017-05-01', '2017-05-02', '2017-05-03']
TEST_SHOW_TIME = ['10:05:00', '13:20:00', '16:35:00', '19:50:00', '22:05:00']
TEST_PRICE = [20.5, 22.5, 28, 35, 37, 41.5]
TEST_PHONE = '18812345678'
TEST_TICKET_CODE = "1000000000"

os.system("mysql -u%s -p%s < ./sql/create_db.sql"
          % (USER, PSWD))
os.system("mysql -D%s -u%s -p%s < ./sql/create_table.sql"
          % (DB_NAME, USER, PSWD))
os.system("mysql -D%s -u%s -p%s < ./sql/insert_data.sql"
          % (DB_NAME, USER, PSWD))

conn = mdb.connect(host='localhost',
                   user=USER,
                   password=PSWD,
                   db=DB_NAME,
                   charset='utf8')

try:
    with conn.cursor() as cursor:

        # Print database info
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print("MySQL version: %s" % data)

        # Find available movies
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
        print("movies:", movies)

        # Find available cinema halls
        print("Finding available cinema halls...")
        cursor.execute("""
            SELECT cinema_hall_id
            FROM CinemaHall
        """)
        cinema_hall_ids = []
        for entry in cursor.fetchall():
            cinema_hall_ids.append(entry[0])
        print("cinema_hall_ids:", cinema_hall_ids)

        # Add on show movies
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

        # Add seats
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
                    if GEN_SOLD_SEATS:
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

        # Add test user
        print("Adding test user...")
        cursor.execute("""
            INSERT INTO User (phone_num) VALUES (%s)
        """ % TEST_PHONE)
        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchall()[0][0]
        print("user_id: %d" % user_id)

        # Add test ticket
        print("Adding test ticket...")
        digest = hashlib.md5(TEST_TICKET_CODE.encode("utf-8")).hexdigest()
        cursor.execute("""
            INSERT INTO Ticket (user_id, digest) VALUES (%d, '%s')
        """ % (user_id, digest))
        cursor.execute("SELECT LAST_INSERT_ID()")
        ticket_id = cursor.fetchall()[0][0]
        print("ticket_id: %d" % ticket_id)
        cursor.execute("""
            INSERT INTO TicketCode (code) VALUES ('%s')
        """ % TEST_TICKET_CODE)

        # Bind ticket to seats
        print("Binding ticket to seats...")
        cursor.execute("""
            UPDATE Seat SET ticket_id=%d WHERE seat_id in (1, 2, 3)
        """ % ticket_id)

    conn.commit()
    print("Done.")
finally:
    conn.close()
