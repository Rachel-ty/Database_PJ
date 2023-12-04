from flask import Flask, render_template, redirect, url_for
import pymysql
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = "TYHuang"

db_config = {
    'host': 'localhost',
    'user': 'DB_admin',
    'password': 'DB_admin',
    'db': 'DB_PJ'
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection

    
@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


class QueryForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/query', methods=['GET', 'POST'])
@login_required
def query():
    query_form = QueryForm()
    record = None
    if query_form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(query_form.query.data)
        record = cursor.fetchall()
        
        cursor.close()
        conn.close()
        # return redirect(url_for('index'))  # how to redirect
    return render_template('query.html', form=query_form, record=record)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    @login_manager.user_loader
    def get(user_id):
        # Todo: Write query get user from database
        return User(user_id)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Todo: Write query to insert user into database; add logic checking
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Todo: validate user login info
        user = User(form.email.data)
        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)