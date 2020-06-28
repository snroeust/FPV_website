from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():

    #mock Objects
    user = {'username' : 'fpv'}
    posts = [{'author':{'username': 'John'},
              'body': "ka was hier stehen soll, die website ist kacke"},
             {'author': {'username': 'lol'},
              'body': "eig ganz nice"}
             ]
    return render_template('index.html', title='Home', user=user, posts=posts)