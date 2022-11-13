from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id , username,fullname, password) -> None:
        self.id = id
        self.username = username
        self.fullname = fullname
        self.password = password

    @classmethod
    def check_password(self,  hashed_password,password):
        return check_password_hash(hashed_password,password)