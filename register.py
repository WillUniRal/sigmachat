from __main__ import app
import sqlite3 as mysql
from flask import Flask, render_template, jsonify, request, redirect
from credentials import secrets
import bcrypt

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
        email = request.form.get("email")

        password = password.encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        with secrets() as credentials_table:
            credentials_table.create()
            credentials_table.register(user,email,hashed_password)
        
        print(user,password, email)
        return redirect("/")
        
    return render_template('register.html')
