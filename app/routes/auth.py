import psycopg2

from flask import render_template, request, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user

from connection import get_postgresql_connection
from app import app, login_manager
from ..models import User



@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with ID {user_id}")
    curs, conn = get_postgresql_connection()
    curs.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = curs.fetchone()
    conn.close()
    curs.close()
    if user:
        return User(id=user[0], username=user[1], password=user[2])
    return None




@app.get("/login/")
def get_login():
    return render_template("login.html")

@app.post("/login/")
def post_login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "@dm1n":
        curs, conn = get_postgresql_connection()
        curs.execute("SELECT * FROM users WHERE username = %s", (username,))
        admin_user = curs.fetchone()
        conn.close()
        curs.close()
        
        if admin_user:
            admin_obj = User(id=admin_user[0], username=admin_user[1], password=admin_user[2])
            login_user(admin_obj)
            return redirect(url_for("admin_page"))

    curs, conn = get_postgresql_connection()
    curs.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = curs.fetchone()
    conn.close()
    curs.close()

    if user and user[2] == password:
        user_obj = User(id=user[0], username=user[1], password=user[2])
        login_user(user_obj)
        return redirect(url_for("menu_page"))
    
    error_message = "Invalid username or password"
    return render_template("login.html", error_message=error_message)




@app.get("/signup/")
def get_signup():
    return render_template("signup.html")

@app.post("/signup/")
def post_signup():
    username = request.form["username"]
    password = request.form["password"]
        
    curs, conn = get_postgresql_connection()

    curs.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = curs.fetchone()

    if existing_user:
        error_message = "User with this username already exists"
        return render_template("signup.html", error_message=error_message)

    try:
        insert_user_query = """INSERT INTO users 
        (username, password) 
        VALUES (%s, %s);"""
        curs.execute(insert_user_query, (username, password))
        conn.commit()
        print("New user successfully added")
    except psycopg2.IntegrityError:
        print("Error: Integrity constraint violated.")
    except psycopg2.Error as error:
        print("Error", error)
    finally:
        if conn:
            conn.close()
        if curs:
            curs.close()
        
    return redirect(url_for("get_login"))



@app.get("/logout/")
@login_required
def logout():
    print("Log out user")
    logout_user()
    return redirect(url_for("get_login"))
