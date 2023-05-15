#importowanie niezbędnych bibliotek
from flask import Flask,render_template, request, jsonify, Blueprint, redirect, session, g, url_for, flash
from flask_mail import Mail
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String  
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import check_password_hash
import smtplib
import functools
import operator
import numpy as np
import os
import bcrypt
import sqlite3
import secrets


#przypisanie nazwy aplikacji oraz folderów
app = Flask(__name__, static_folder='static', static_url_path='/static')
    
#automatyczne debugowanie - nie ma potrzeby restartować flaska po każdej zmianie kodu
if __name__ == '__app__':
    app.run(debug=True)


#ustawienia bazy danych
DATABASE = '..\db\zombie-apocalypse.db'

#obsługa wysyłania emailów do użytkowników
app.secret_key = "f09da1a4f9569ae3f19c9710c57999ea"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'PrzemSad99@gmail.com'
app.config['MAIL_PASSWORD'] = 'xxx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']

#strona główna
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET','POST'])
def zarejestruj_uzytkownika():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm-password']
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM user WHERE user_username = ?', (username,))
        if cursor.fetchone():   
            flash('Username already exists')
            return redirect(url_for('register'))
        elif password != confirm:
            flash('''Given passwords don't match''')
            return redirect(url_for('register'))

        haslo_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute('INSERT INTO user (user_email, user_username, user_pass_hash,user_premium_points,user_coins,user_topscore) VALUES (?, ?, ?,0,100,0)', (email,username, haslo_hash))
        db.commit()
        db.close()
        flash('User registered successfully')
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM user WHERE user_username = ?', (username,))
        if cursor.fetchone():
            cursor.execute('SELECT user_pass_hash FROM user WHERE user_username = ?', (username,))
            query_output = cursor.fetchone()
            if query_output and check_password_hash(query_output[0],password):
                session['username'] = username
                print("username: ",session['username'])
                db.close()
                return redirect(url_for('index'))
            else:
                flash("Incorrect password")
                db.close()
                return redirect(url_for('login'))
        db.commit()
        db.close()
    return render_template('login.html')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/highestscores")
def highestscores():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT user_username, user_topscore FROM user ORDER BY user_topscore DESC LIMIT 10')
    highestscores = cursor.fetchall()
    db.close()
    return render_template('highestscores.html', scores=highestscores )

@app.route("/community")
def community():
    return render_template('community.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/account")
def account():
    g.user = session['username']
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT user_premium_points, user_coins, user_topscore from user WHERE user_username = ?", (g.user,) )
    acc_info = cursor.fetchall()
    premium_points, user_coins, user_topscore = acc_info[0]
    return render_template('account.html', premium_points = premium_points, user_coins=user_coins, user_topscore=user_topscore)

@app.route("/static/css/style.css")
def style():
    return app.send_static_file("css/style.css")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


