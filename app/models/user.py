from flask_login import UserMixin, login_user, login_required, logout_user, current_user


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
