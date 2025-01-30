import psycopg2

from flask import render_template, redirect, url_for, request
from flask_login import current_user

from app import app
from connection import get_postgresql_connection



def get_all_games():
    curs, conn = get_postgresql_connection()
    curs.execute("SELECT * FROM torrent")
    torrents = curs.fetchall()
    curs.close()
    conn.close()
    return torrents



@app.get("/")
def start():
    if current_user.is_authenticated:
        return redirect(url_for("menu_page"))
    else:
        return redirect(url_for("get_login"))

@app.get("/menu/")
def menu_page():
    games = get_all_games()
    context = {"torrents": games}
    return render_template("menu.html", **context)



@app.get("/add_game/")
def add_page():
    return render_template("add.html")



@app.get("/admin/")
def admin_page():
    games = get_all_games()
    context = {"torrents": games}
    return render_template("admin.html", **context)



@app.post("/add_game/")
def add_game_post():
    name = request.form.get("name")
    author = request.form.get("author")
    release = request.form.get("release")
    description = request.form.get("description")
    genre = request.form.get("genre")
    os = request.form.get("os")
    processor = request.form.get("processor")
    ram = request.form.get("ram")
    video = request.form.get("video")
    space_on_pc = request.form.get("space_on_pc")
    photo = request.form.get("photo")

    try:
        curs, conn = get_postgresql_connection()

        insert_torrent_query = """INSERT INTO torrent 
        (name, author, photo) 
        VALUES (%s, %s, %s);"""
        curs.execute(insert_torrent_query, (name, author, photo))
        conn.commit()
        print("New game successfully added to torrent!")

        insert_game_query = """INSERT INTO game 
        (name, description, genre, release) 
        VALUES (%s, %s, %s, %s);"""
        curs.execute(insert_game_query, (name, description, genre, release))
        conn.commit()
        print("New game successfully added to game!")

        insert_system_req_query = """INSERT INTO system_req 
        (os, processor, ram, video, space_on_pc) 
        VALUES (%s, %s, %s, %s, %s);"""
        curs.execute(insert_system_req_query, (os, float(processor), int(ram), int(video), int(space_on_pc)))
        conn.commit()
        print("New game system requirements successfully added!")

    except psycopg2.IntegrityError:
        print("Error: Integrity constraint violated.")
    except psycopg2.Error as error:
        print("Error", error)
    finally:
        if conn:
            conn.close()
        if curs:
            curs.close()

    return render_template("add.html")
