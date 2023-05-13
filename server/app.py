#importowanie niezbędnych bibliotek
from flask import Flask,render_template, request, jsonify, Blueprint, redirect, session
from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_mail import Message
from mysql.connector import connect, Error
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


#przypisanie nazwy aplikacji oraz folderów
app = Flask(__name__, static_folder='static', static_url_path='/static')
#automatyczne debugowanie - nie ma potrzeby restartować flaska po każdej zmianie kodu
if __name__ == '__app__':
    app.run(debug=True)

#ustawienia bazy danych
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vr'
mysql = MySQL(app)

#obsługa wysyłania emailów do użytkowników
app.secret_key = "sekretny-klucz"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'PrzemSad99@gmail.com'
app.config['MAIL_PASSWORD'] = 'xxx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#strona główna
@app.route("/")
def index():
    session.clear()
    return render_template('index.html')

@app.route("/register")
def zarejestruj_uzytkownika():
    return render_template('register.html')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/highestscores")
def highestscores():
    return render_template('highestscores.html')

@app.route("/community")
def community():
    return render_template('community.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/static/css/style.css")
def style():
    return app.send_static_file("css/style.css")

@app.route("/zarejestruj", methods=['POST'])
def zarejestruj():
    #status_rej = 'default'
    mail = request.form['mail']
    haslo = request.form['haslo']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from uzytkownik WHERE email=%s", (mail,))
    wynik_query = cursor.fetchone()
    wynik = int(wynik_query[0])
    if (wynik>0):
        print("uzytkownik istnieje")
        status_rej = 'error'
    else:
        haslo_hash = bcrypt.hashpw(haslo.encode("utf-8"), bcrypt.gensalt())
        cursor.execute("INSERT INTO uzytkownik(id_uzytkownik,email,hasło) VALUES(default,%s,%s)", 
                       (mail,haslo_hash))
        mysql.connection.commit()
        cursor.close()
        status_rej = 'success'
    session['status_rej'] = status_rej
    return redirect("/rejestracja")
    
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        identyfikator = request.form['mail']
        haslo = request.form['haslo']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT hasło from uzytkownik WHERE email=%s", (identyfikator,))
        wynik = cursor.fetchone()
        # Sprawdź czy podane dane są zgodne
        if wynik and check_password_hash(wynik[0],haslo):
            session['username'] = identyfikator
            return render_template('uzytkownik_zmiana.html')
        else:
            return 'Invalid credentials'
    else:
        return render_template('login.html')

@app.route("/unity_logowanie", methods=["POST", "GET"])
def unity_logowanie():
    email = request.form.get("email")
    haslo = request.form.get("haslo")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT hasło from uzytkownik WHERE email=%s", (email,))
    wynik = cursor.fetchone()
    print(wynik)
    if wynik and check_password_hash(wynik[0],haslo):
        return "Sukces!"
    else:
        return "Blad!"

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route("/dodaj_email", methods=["POST"])
def dodaj_email():
    email = request.form["email"]
    haslo = request.form["haslo"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"INSERT INTO uzytkownik(id_uzytkownik,email,hasło,opis) VALUES (default,'{email}','{haslo}')")
    mysql.connection.commit()
    cursor.close()
    return "Dodano email"
