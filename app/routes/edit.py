from flask import render_template, abort, request, url_for, flash, redirect
from app.routes import app
from connection import get_postgresql_connection


@app.get("/<int:game_id>/edit/")
def get_edit(game_id):
    game = get_game_id(game_id)
    if not game:
        flash("Game not found!")
        return redirect(url_for("menu_page"))
    return render_template("edit.html", game=game)



@app.post("/<int:game_id>/edit/")
def post_edit(game_id):
    game = get_game_id(game_id)
    if not game:
        flash("Game not found!")
        return redirect(url_for("menu_page"))
    
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
    
    if not name or len(name) < 4:
        flash("Name is not required!")
        return render_template("edit.html", game=game)
    else:
        curs, conn = get_postgresql_connection()
        curs.execute("UPDATE games SET name = %s, author = %s, release = %s, description = %s, genre = %s, os = %s, processor = %s, ram = %s, video = %s, space_on_pc = %s, photo = %s, price = %s WHERE id = %s",
                     (name, author, description, genre, release, os, processor,
                      int(ram), video, int(space_on_pc), photo, int(price), game_id))
        curs.close()
        conn.close()
        return redirect(url_for("menu_page"))

    

@app.post("/<int:game_id>/delete/")
def game_delete(game_id):
    curs, conn = get_postgresql_connection()
    curs.execute("DELETE FROM games WHERE game_id = %s", (game_id,))
    curs.close()
    conn.close()
    return redirect(url_for("menu_page"))
    
    
def get_game_id(game_id):
    curs, conn = get_postgresql_connection()
    if curs is None:
        return None
    curs.execute("SELECT * FROM games WHERE game_id = %s", (game_id,))
    game = curs.fetchone()
    curs.close()
    conn.close()
    return game
