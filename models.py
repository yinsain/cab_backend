#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
import datetime

class UsersMeta(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    id_proof = db.Column(db.String(20), nullable=False, unique=True)
    rating = db.Column(db.Integer, nullable=False, default=0)
    doreg = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr(self):
        return f"UsersMeta('{self.uid}', '{self.email}', '{self.phone}', '{self.name}', '{self.id_proof}', '{self.rating}')"

class UserCreds(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"UserCreds('{self.uid}', '{self.name}', '{self.password}')"
