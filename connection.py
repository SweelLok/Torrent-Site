import psycopg2
from psycopg2 import OperationalError

import psycopg2


def get_postgresql_connection():
    try:
        connection = psycopg2.connect(
            host="127.0.0.1", 
            dbname="Torrent", 
            user="postgres", 
            password="@dm1n", 
            port=5432)
        curs = connection.cursor()
        return curs, connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None


def create_game_table():
    curs, conn = get_postgresql_connection()
    try:
        curs.execute("""CREATE TABLE IF NOT EXISTS Games (
        game_id INTEGER GENERATED ALWAYS AS IDENTITY UNIQUE NOT NULL,
        name text NOT NULL UNIQUE,
        author text NOT NULL,
        photo TEXT NOT NULL,
        description text NOT NULL UNIQUE,
        genre text NOT NULL,
        release date NOT NULL,
        os text NOT NULL,
        processor text NOT NULL,
        ram INTEGER NOT NULL,
        video text NOT NULL,
        space_on_pc INTEGER NOT NULL,
        price INTEGER NOT NULL);""")
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        curs.close()
        conn.close()


def create_user_table():
    curs, conn = get_postgresql_connection()
    try:
        curs.execute("""CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER GENERATED ALWAYS AS IDENTITY UNIQUE NOT NULL,
        username VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(150) NOT NULL);""")
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        curs.close()
        conn.close()
        