'''
Created on Nov 10, 2022

@author: jdunh
'''

from multiprocessing import Process
import time
from markupsafe import escape
from flask import Flask, render_template, request, Response, session

app = Flask(__name__)

from flask import abort, redirect, url_for

@app.route('/')
def colors():
    return(render_template('index.html'))



app.run()





