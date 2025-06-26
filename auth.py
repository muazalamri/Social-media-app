#--------------load libs-----------
from flask import Flask,abort,session, render_template, request, redirect, url_for,flash,jsonify,send_file
from model import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from flask_wtf.csrf import CSRFProtect
from os import urandom,path
from appUtlits import *
from datetime import datetime
from app import *

@app.route('/sign-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid username or password')
    return render_template('sign-in.html')

@app.route('/sign-out')
def logout():
    logout_user()
    return redirect(app.config['domain']+'/sign-in') 
@login_required
@app.route('/resetpw')
def resetpw():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Send email with password reset link
            pass
        else:
            flash('Invalid email')
    else:return render_template('recoverpw.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            add_to_db(User,username=username,password=password,email=email)
            return redirect('/sign-in')
        else:
            flash('Username already exists')
    return render_template('sign-up.html')