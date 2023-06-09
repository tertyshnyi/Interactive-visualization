import datetime
import threading
import time

from flask import Flask, render_template, redirect, url_for, request
import dash
from dash import html, dcc
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
import pandas as pd
import dash_bootstrap_components as dbc

from backend import time_update
from templates import dashboard_layout
from callbacks import callback_
from components import navbar

articles_data = pd.read_csv('data/correct_articles.csv')
authors_locations_data = pd.read_csv('data/correct_authors_locations.csv')

nav = navbar.navbar()

server = Flask(__name__)
db = SQLAlchemy(server)
bcrypt = Bcrypt(server)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
server.config['SECRET_KEY'] = 'eor125ihjerelhnerop4574572irykmj23626klKJNERLHNER$@1KM'

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)


db.create_all()


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(max=40), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('That email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(max=40)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@server.route('/', methods=['GET'])
def root():
    return redirect(url_for('login'))


@server.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/dashboard')
    return render_template('login.html', form=form)


@server.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@server.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@server.route('/journal')
@login_required
def journal():
    return render_template('journal.html')


dash_app = dash.Dash(__name__, server=server,
                     external_stylesheets=[dbc.themes.BOOTSTRAP],
                     meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                     suppress_callback_exceptions=True
                     )

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='dashboard-content')
])


def display_dashboard(pathname):
    if not current_user.is_authenticated or pathname != '/dashboard':
        return redirect(url_for('login'))
    return [nav, dashboard_layout.layout(articles_data)]


dash_app.callback(
    dash.dependencies.Output('dashboard-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)(display_dashboard)

callback_(dash_app, articles_data, authors_locations_data)


def update_data_periodically():
    while True:
        now = datetime.datetime.now()
        if 2 <= now.hour <= 4:
            print(f"Time for update data!")
            time_update()
            print('Data updated!')
            time.sleep(3600)
        time.sleep(3600)


if __name__ == "__main__":
    threading.Thread(target=update_data_periodically).start()
    server.run(host='147.232.182.91', debug=True, port=8030)
