# -*- coding: utf-8 -*-
# --------------------------------------
#       @Time    : 2018/8/2 下午3:40
#       @Author  : cxy =.= 
#       @File    : hello.py
#       @Software: PyCharm
# --------------------------------------
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)



@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'Hello %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath
