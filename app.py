#--------------load libs-----------
from flask import Flask,abort,session, render_template, request, redirect, url_for,flash,jsonify,send_file
from model import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from flask_wtf.csrf import CSRFProtect
from os import urandom,path
from appUtlits import *
from datetime import datetime
class App(Flask):
    ranker=None
    dm=None
#--------------initizing--------
app = App(__name__)


app.config['SECRET_KEY']= urandom(24)
#csrf = CSRFProtect(app)
# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Netapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] ='uploads/'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024  # 4 GB limit
app.config['domain'] = "http://127.0.0.1:5000/"
"""def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = urandom(24).hex()
    return session['_csrf_token']

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        token_from_request = request.form.get('_csrf_token') or request.headers.get('X-CSRFToken')
        if not token or token != token_from_request:
            abort(403)

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    return jsonify({'csrf_token': generate_csrf_token()})"""
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@login_manager.request_loader
def load_user_from_request(request):
    # Implement your logic to load a user from the request
    return None
# Initialize the database


#---------------erorr hander-----------
@app.errorhandler(500)
def internal_server_error(error):return render_template('500.html'), 500
