#!/usr/bin/env python3
from flask import Flask, request, jsonify, session, flash, redirect, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_site.db'
db = SQLAlchemy(app)

class UsersMeta(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    doreg = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr(self):
        return f"UsersMeta('{self.uid}', '{self.email}', '{self.phone}', '{self.name}', '{self.rating}')"

class UserCreds(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"UserCreds('{self.uid}', '{self.name}', '{self.password}')"

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return 'Logged Out!!'
    return wrap

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        if request.headers['Content-type'] == 'application/json':
            x = request.get_json()
            a = UsersMeta(email=x['user-mail'], phone=x['user-mob'], \
            name=x['user-name'])
            db.session.add(a)
            db.session.commit()
        return jsonify({'status':'success'})

@app.route('/login', methods = ['POST'])
def login():
    print('Im in login functions!!!!')
    if request.method == 'POST':
        if request.headers['Content-type'] == 'application/json':
            x = request.get_json()
            session['user'] = x['user']
            session['logged_in'] = True
        return 'LI'

@app.route('/logout', methods = ['POST'])
@is_logged_in
def logout():
    if request.method == 'POST':
        if request.headers['Content-type'] == 'application/json':
            x = request.get_json()
            print(x['user'])
            session.pop('user')
            session.pop('logged_in')
        return 'LO'

@app.route('/profile', methods = ['POST'])
@is_logged_in
def profile():
    if request.method == 'POST':
        if request.headers['Content-type'] == 'application/json':
            x = request.get_json()
            print(type(x))
            return jsonify(x)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
