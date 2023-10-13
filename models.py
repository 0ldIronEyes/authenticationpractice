from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    """User Model"""
    __tablename__ = "users"
    
    username= db.Column(db.Text(12), unique=True, nullable=False, primary_key= True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(50), nullable=False, unique= True)
    first_name = db.Column(db.Text(30), nullable=False)
    last_name = db.Column(db.Text(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete")

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """register a new user"""
        hash = bcrypt.generate_password_hash(password)
        hashed_utf8 = hash.decode("utf8")
        user = cls(username = username, password = hashed_utf8, first_name = first_name,
                   last_name = last_name, email= email)
        db.session.add(user)
        return user



    @classmethod
    def authenticate(cls, username, pwd):
        """validate user and password""" 

        user = User.query.filter_by(username = username).first()

        if user  and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        

class Feedback(db.Model):
    """Feedback Model"""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content= db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"),nullable=False)
