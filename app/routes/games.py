import psycopg2

from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required

from app import app
from connection import get_postgresql_connection



def get_all_games():
    curs, conn = get_postgresql_connection()
    curs.execute("SELECT * FROM games")
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
    context = {"games": games}
    if current_user.username == "admin" and current_user.password == "@dm1n":
        return redirect(url_for("admin_page"))
    return render_template("menu.html", **context)



@app.get("/add_game/")
def add_page():
    return render_template("add.html")



@app.get("/admin/")
def admin_page():
    games = get_all_games()
    context = {"games": games}
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
    price = request.form.get("price")
    
    try:
        curs, conn = get_postgresql_connection()

        inser_query = """INSERT INTO games 
        (name, author, photo, description, genre, release, os, processor, ram, video, space_on_pc, price) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        curs.execute(inser_query, (name, author, photo, description, genre, release, os, processor,
                                   int(ram), video, int(space_on_pc), int(price)))
        conn.commit()
        print("New game successfully added to bd!")


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
