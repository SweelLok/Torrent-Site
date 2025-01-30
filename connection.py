import psycopg2

def get_postgresql_connection():
    connection = psycopg2.connect(
        host="127.0.0.1", 
        dbname="Torrent", 
        user="postgres", 
        password="@dm1n", 
        port=5432
    )
    curs = connection.cursor()
    return curs, connection


def create_torrent_table():
    curs, conn = get_postgresql_connection()
    try:
        curs.execute("""CREATE TABLE IF NOT EXISTS Torrent (
        id INTEGER GENERATED ALWAYS AS IDENTITY UNIQUE NOT NULL,
        name text NOT NULL UNIQUE,
        author text NOT NULL,
        photo TEXT NOT NULL);""")
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        curs.close()
        conn.close()


def create_game_table():
    curs, conn = get_postgresql_connection()
    try:
        curs.execute("""CREATE TABLE IF NOT EXISTS Game (
        id INTEGER GENERATED ALWAYS AS IDENTITY UNIQUE NOT NULL,
        name text NOT NULL UNIQUE,
        description text NOT NULL UNIQUE,
        genre text NOT NULL,
        release date NOT NULL);""")
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        curs.close()
        conn.close()


def create_system_req_game_table():
    curs, conn = get_postgresql_connection()
    try:
        curs.execute("""CREATE TABLE IF NOT EXISTS System_req (
        id INTEGER GENERATED ALWAYS AS IDENTITY UNIQUE NOT NULL,
        os text NOT NULL,
        processor INTEGER NOT NULL,
        ram INTEGER NOT NULL,
        video INTEGER NOT NULL,
        space_on_pc INTEGER NOT NULL);""")
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
        id INTEGER GENERATED ALWAYS AS IDENTITY UNIQUE NOT NULL,
        username VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(150) NOT NULL);""")
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        curs.close()
        conn.close()
        