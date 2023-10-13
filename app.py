from flask import Flask, url_for, render_template, redirect, flash, jsonify, session


from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LogInForm, DeleteForm, FeedbackForm
from models import db, connect_db, User, Feedback
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretttkeeyyy"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    return redirect("/register")


@app.route('/register', methods= ["GET", "POST"])
def register_page():
    form = RegisterUserForm()

    if form.validate_on_submit():
         user = User.register(username= form.username.data, password= form.password.data, email= form.email.data,
                     first_name=form.firstname.data, last_name=form.lastname.data)
         db.session.commit()
         session['username'] = user.username
         flash("Successfully created Account")
         return(f"/users/{user.username}")
    else:
        return render_template("register.html",form=form)
    


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LogInForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid Username/Password"]
            return render_template("Login.html", form=form)
   
    return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    """logout"""

    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>")
def secret_page(username):
    """information page when logged in"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    user = User.query.get(username)
    render_template("user_detail.html", user=user)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """delete user"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')

    return redirect('/login')

@app.route("users/<username>/feedback/new", methods = ["GET", "POST"])
def new_feedback(username):
    """create new feedback"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback( title=title, content=content, username= username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template("add_feedback", form = form)
    
@app.route("feedback/<feedback-id>/update", methods = ["GET", "POST"])
def update_feedback(feedback_id):
    """update the feedback"""
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("edit_feedback", form=form, feedback = feedback)
    

@app.route("feedback/<feedback-id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """delete feedback"""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        
        return redirect(f"/users/{feedback.username}")