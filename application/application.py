import flask
app = flask.Flask(__name__)

import psycopg2

from .error import UserError
from .types import AllTypes, AllTypesDict

@app.route('/')
def index():
    return flask.render_template("index.html",
            types=AllTypes,
    )

@app.route('/login/<type_code>', methods=['GET', 'POST'])
def login(type_code):
    if type_code not in AllTypesDict:
        flask.abort(404)

    t = AllTypesDict[type_code]

    if flask.request.method == "GET":
        return flask.render_template("login.html", type=t)

    username = flask.request.form.get('username', '')
    if username == '':
        return flask.render_template("login.html", error="username is required", type=t)

    password = flask.request.form.get('password', '')
    if password == '':
        return flask.render_template("login.html", error="password is required", type=t)

    db = connect()

    ti = t()
    try:
        ti.login(db.cursor(), username, password)
    except UserError as err:
        return flask.render_template("login.html", error=err.message, type=t)

    return flask.render_template("success.html", type=t)

@app.route('/signup/<type_code>', methods=['GET', 'POST'])
def signup(type_code):
    if type_code not in AllTypesDict:
        flask.abort(404)

    t = AllTypesDict[type_code]

    if flask.request.method == "GET":
        return flask.render_template("signup.html", type=t)

    username = flask.request.form.get('username', '')
    if username == '':
        return flask.render_template("signup.html", error="username is required", type=t)

    password = flask.request.form.get('password', '')
    if password == '':
        return flask.render_template("signup.html", error="password is required", type=t)

    db = connect()

    ti = t()
    try:
        ti.create_account(db.cursor(), username, password)
        db.commit()
    except UserError as err:
        return flask.render_template("signup.html", error=err.message, type=t)

    return flask.render_template("signup_success.html", type=t)

def connect():
    return psycopg2.connect('')
