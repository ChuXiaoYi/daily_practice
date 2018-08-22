# -*- coding: utf-8 -*-
# --------------------------------------
#       @Time    : 2018/8/2 下午5:06
#       @Author  : cxy =.= 
#       @File    : 02_url_for.py
#       @Software: PyCharm
# --------------------------------------
from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/login')
def login():
    return 'login'


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
