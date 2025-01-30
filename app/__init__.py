from flask import Flask
from flask_login import LoginManager

from connection import create_torrent_table, create_game_table, create_system_req_game_table, create_user_table


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "q"
create_torrent_table()
create_game_table()
create_system_req_game_table()
create_user_table()
