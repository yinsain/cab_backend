#!/usr/bin/env python3
from flask import Flask, request, jsonify, session, flash, redirect, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import datetime
from otputils import otp_send

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
        for k, x in request.headers.items():
            print(k, ':', x)
        if request.headers['Content-type'] == 'application/json;':
            x = request.get_json()
            print(x)
            a = UsersMeta(email=x['user-mail'], phone=x['user-mob'], \
            name=x['user-name'])
            db.session.add(a)
            b = UserCreds(uid=a.uid, name=x['user-mail'], password=x['user-pass'])
            db.session.add(b)
            db.session.commit()
            return jsonify({'status':'success'})
        return jsonify({'status':'error'})

@app.route('/getverify', methods = ['POST'])
def gencode():
    if request.method == 'POST':
        if request.headers['Content-type'] == 'application/json':
            x = request.get_json()
            email = x['user-mail']
            code = otp_send(email)
            return jsonify({'status':'otp-sent', 'code':code})

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        if request.headers['Content-type'] == 'application/json':
            x = request.get_json()
            res = UserCreds.query.filter_by(name=x['user-mail']).first()
            if res.password == x['user-pass'] and res.name == x['user-mail']:
                session['uid'] = res.uid
                session['name'] = res.name
                session['logged_in'] = True
                return jsonify({'status':'login-success'})
            else:
                return jsonify({'status':'login-failed'})

@app.route('/logout', methods = ['POST'])
@is_logged_in
def logout():
    if request.method == 'POST':
        if request.headers['Content-type'] == 'application/json':
            x = request.get_json()
            print(x['user'])
            session.pop('name')
            session.pop('uid')
            session.pop('logged_in')
        return 'LO'

@app.route('/profile', methods = ['GET'])
@is_logged_in
def profile():
    if request.method == 'GET':
        r = UsersMeta.query.filter_by(email=session['name']).first()
        return jsonify({
            'user-mail': r.email,
            'user-mob' : r.phone,
            'user-name' : r.name,
            'user-rating' : r.rating,
            'user-doj' : r.doreg
        })
    else:
        return jsonify({'status':'profile-failed'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
