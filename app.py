#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "first text"

if __name__ == '__main__':
    app.run(debug=True)
