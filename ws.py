#--------------load libs-----------
from flask import render_template
from flask_login import current_user
from appUtlits import *
from app import *

@app.route('/vid')
def index():
    return render_template('vid.html')