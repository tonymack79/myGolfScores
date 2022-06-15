import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, CourseForm, ScoreForm
from models import db, connect_db, User, Course, Score

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///mygolfscores'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

#########################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Thank you, Come again!", "primary")
    
    return redirect('/login')
  
##############################################################
# Add and select course

@app.route('/course/add', methods=["GET", "POST"])  
def add_course():
    """Add a course"""
    form = CourseForm()
    
    if form.validate_on_submit():
        course_name = form.course_name.data
        par = form.par.data
        course = Course(course_name=course_name, par=par)
        db.session.add(course)
        db.session.commit()
        
        return redirect('/course')
    
    return render_template('course/add.html')
  
@app.route('/course')
def select_course():
    """Select course to input score for"""
    search = request.args.get('q')
    
    if not search:
        courses = Course.query.all()
    else:
        courses = Course.query.filter(Course.course_name.like(f"%{search}")).all()
        
    return render_template('course/select.html')
    
#############################################################
# Add scores

@app.route('/score')
def add_score():
    """Add a score"""
    form = ScoreForm()
    
    if form.validate_on_submit():
        user_id = session[CURR_USER_KEY]
        course_id = form.course_id.data
        score = form.score.data
        date = form.date.data
        
        new_score = Score(user_id=user_id, course_id=course_id, score=score, date=date)
        db.session.add(new_score)
        db.session.commit()
        
        return redirect('/')
    
    return render_template('score.html', form=form)
    
##############################################################
# Homepage

@app.route('/')
def homepage():
    """Homepage"""
    
    if g.user:
        scores = Score.query.filter_by(user_id=session[CURR_USER_KEY]).all()
        user = g.user
        
        return render_template('home.html', scores=scores, user=user)
    
    else:
        return redirect('/login')