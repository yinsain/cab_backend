#!/usr/bin/env python3
from flask import Flask, request, jsonify, session, flash, redirect, url_for, make_response
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
    otp = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"UserCreds('{self.uid}', '{self.name}', '{self.password}')"

class RidesMeta(db.Model):
    rid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    src = db.Column(db.String(250), nullable=False)
    dest = db.Column(db.String(250), nullable=False)
    rdate = db.Column(db.DateTime, nullable=False)
    seats = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    hour = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"RidesMeta('{self.rid}', '{self.src}', '{self.dest}', '{self.rdate}', '{self.seats}', '{self.price}', '{self.hour}')"

class Rider(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    car_model = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.Integer, nullable=False, default=0)
    avlbl_seats = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=False, default=0)
    rides_given = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"Rider('{self.uid}', '{self.car_model}', '{self.seats}', '{self.avlbl_seats}', '{self.rating}', '{self.rides_given}')"

class RidesGiven(db.Model):
    idx = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    rid = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"RidesGiven('{self.idx}', '{self.uid}', '{self.rid}')"

class RidesBooked(db.Model):
    idx = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    rid = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"RidesBooked('{self.idx}', '{self.uid}', '{self.rid}')"

class Subscriptions(db.Model):
    idx = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"Subscriptions('{self.idx}', '{self.uid}', '{self.pid}')"

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        for k, x in request.headers.items():
            print(k, ':', x)
        if 'application/json' in request.headers['Content-type']:
            x = request.get_json()
            print(x)
            a = UsersMeta(email=x['user-mail'], phone=x['user-mob'], \
            name=x['user-name'])
            db.session.add(a)
            code = otp_send(x['user-mail'])
            b = UserCreds(uid=a.uid, name=x['user-mail'], password=x['user-pass'], otp=code)
            db.session.add(b)
            db.session.commit()
            return jsonify({'status':'success'})
        return jsonify({'status':'error'})

@app.route('/verify', methods = ['POST'])
def verifycode():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            x = request.get_json()
            email = x['user-mail']
            code = x['otp']
            print('data--------', email, code)
            res = UserCreds.query.filter_by(name=x['user-mail']).first()
            if res.name == email and res.otp == code:
                print('correct')
                return jsonify({'status':'otp-correct'})
            else:
                return jsonify({'status':'otp-wrong'})

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            for t,x in request.headers.items():
                print(t,x)
            print(len(request.cookies))
            for t,x in request.cookies.items():
                print(t,x)
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
def logout():
    if request.method == 'POST':
        session.clear()
        return jsonify({'status':'logout-success'})

@app.route('/profile', methods = ['POST'])
def profile():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            x = request.get_json()
            r = UsersMeta.query.filter_by(email=x['userMail']).first()
            return jsonify({
                'userMail': r.email,
                'userMob' : r.phone,
                'userName' : r.name,
                'userRating' : r.rating,
                'userDoj' : r.doreg,
                'userId' : r.uid
            })
    else:
        return jsonify({'status':'profile-failed'})

@app.route('/offer', methods = ['POST'])
def offer_ride():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            x = request.get_json()

            tdate = x['date'].split('/')
            dobj = datetime.datetime(int(tdate[2]), int(tdate[1]), int(tdate[0]))

            a = RidesMeta(src=x['source'], dest=x['dest'], \
            rdate=dobj, \
            seats=int(x['seats']), \
            price=x['price'], \
            hour=int(x['hour']), \
            )
            db.session.add(a)
            db.session.commit()
            #b = Rides_given(uid=session['uid'], rid=a.rid)
            print(a)
            b = RidesGiven(uid=1, rid=a.rid)
            db.session.add(b)
            db.session.commit()

            return jsonify({'status' : 'ride-added'})
        else:
            return jsonify({'status' : 'ride-offer-failed'})

@app.route('/find', methods = ['POST'])
def find_ride():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            rides_list = list()
            x = request.get_json()
            tdate = x['date'].split('/')
            dobj = datetime.datetime(int(tdate[2]), int(tdate[1]), int(tdate[0]))
            src = x['source']
            dest=x['dest']
            rdate=dobj
            hour=int(x['hour'])
            seats = int(x['seats'])
            res =  RidesMeta.query.filter(
            RidesMeta.src.startswith(x['source']),
            RidesMeta.dest.startswith(x['dest']),
            RidesMeta.rdate == dobj,
            RidesMeta.hour >= hour - 2,
            RidesMeta.hour <= hour + 2,
            RidesMeta.seats >= seats
            ).all()
            for x in res:
                print('TESTING===', x.rid)
                rm =  RidesMeta.query.filter_by(rid=x.rid).first()
                rg = RidesGiven.query.filter_by(rid=x.rid).first()
                u = UsersMeta.query.filter_by(uid=rg[0].uid).first()
                rides_list.append({
                'rid' : rm.rid,
                'source' : rm.src,
                'dest' : rm.dest,
                'date' : rm.rdate,
                'seats' : rm.seats,
                'price' : rm.price,
                'hour' : rm.hour,
                'name' : u[0].name
                })
            return jsonify({'rides' : rides_list})
        else:
            return jsonify({'rides' : 'no-rides'})

@app.route('/offered', methods = ['GET'])
def offered_ride():
    if request.method == 'GET':
        res = RidesGiven.query.filter_by(uid=1)
        res_name = UsersMeta.query.filter_by(email='yashdeep.saini@students.iiit.ac.in').first()
        rides_list = list()
        for x in res:
            print('TESTING===', x.rid)
            rm =  RidesMeta.query.filter_by(rid=x.rid).first()
            rg = RidesGiven.query.filter_by(rid=x.rid).first()
            u = UsersMeta.query.filter_by(uid=rg[0].uid).first()
            rides_list.append({
            'rid' : rm.rid,
            'source' : rm.src,
            'dest' : rm.dest,
            'date' : rm.rdate,
            'seats' : rm.seats,
            'price' : rm.price,
            'hour' : rm.hour,
            'name': res_name.name,
            'name' : u[0].name,
            'phone' : u[0].phone
            })
        return jsonify({'rides' : rides_list})
    else:
        return jsonify({'rides' : 'no-rides'})

@app.route('/subscribe', methods = ['POST'])
def subscribe():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            x = request.get_json()
            s = Subscriptions(uid=1, pid=int(x['rider-id']))
            db.session.add(s)
            db.session.commit()
            return jsonify({'subscribe' : 'added'})
        else:
            return jsonify({'subscribe' : 'failed'})

@app.route('/notifications', methods = ['POST'])
def notifiy():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            rides_list = list()
            slist = Subscriptions.query.filter_by(uid=1)
            for sx in slist:
                res = RidesGiven.query.filter_by(uid=sx.pid)
                for x in res:
                    print('TESTING===', x.rid)
                    rm =  RidesMeta.query.filter_by(rid=x.rid).first()
                    rides_list.append({
                    'rid' : rm.rid,
                    'source' : rm.src,
                    'dest' : rm.dest,
                    'date' : rm.rdate,
                    'seats' : rm.seats,
                    'price' : rm.price,
                    'hour' : rm.hour
                    })
            return jsonify({'rides' : rides_list})
        else:
            return jsonify({'rides' : 'nothing-new'})

@app.route('/booked', methods = ['POST'])
def booked():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            rides_list = list()
            slist = RidesBooked.query.filter_by(uid=1)
            for sx in slist:
                res = RidesGiven.query.filter_by(uid=sx.rid)
                for x in res:
                    print('TESTING===', x.rid)
                    rm =  RidesMeta.query.filter_by(rid=x.rid).first()
                    rides_list.append({
                    'rid' : rm.rid,
                    'source' : rm.src,
                    'dest' : rm.dest,
                    'date' : rm.rdate,
                    'seats' : rm.seats,
                    'price' : rm.price,
                    'hour' : rm.hour
                    })
            return jsonify({'rides' : rides_list})
        else:
            return jsonify({'rides' : 'nothing-new'})

@app.route('/book', methods = ['POST'])
def book():
    if request.method == 'POST':
        if 'application/json' in request.headers['Content-type']:
            x = request.get_json()
            s = RidesBooked(uid=x['userId'], rid=int(x['rid']))
            db.session.add(s)
            db.session.commit()
            return jsonify({'ride' : 'booked'})
        else:
            return jsonify({'ride' : 'booking-failed'})

if __name__ == '__main__':
    #db.drop_all()
    db.create_all()
    app.run(debug=True)
