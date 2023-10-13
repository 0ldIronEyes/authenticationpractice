from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class RegisterUserForm(FlaskForm):
    """New user form"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    email = StringField("email",validators={InputRequired()} )
    firstname = StringField("first name", validators=[InputRequired()])
    lastname = StringField("last name", validators=[InputRequired()])


class LogInForm(FlaskForm):
    """Log in form"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Feedback form"""

    title = StringField("title", validators=[InputRequired()])
    content = StringField("content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """delete form"""