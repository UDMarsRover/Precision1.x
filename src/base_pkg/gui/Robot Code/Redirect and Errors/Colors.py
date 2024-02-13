'''
Created on Nov 8, 2022

@author: jdunh
'''
from multiprocessing import Process
import time
from markupsafe import escape
from flask import Flask, render_template, request, Response, session

app = Flask(__name__)

from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(418)



    
    #return render_template('file2.html')
    return render_template(app.abort(101))



app.run()