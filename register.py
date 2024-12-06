from __main__ import app
import sqlite3 as mysql
from flask import Flask, render_template, jsonify, request, redirect
from tables import credentials,profile
import bcrypt

@app.route('/register', methods = ['GET','POST'])
def register():
    error=""
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
        email = request.form.get("email")

        password = password.encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        try:
            with credentials() as credentials_table:
                credentials_table.create()
                credentials_table.register(user,email,hashed_password)
        except mysql.IntegrityError as error : 
            if "email" in error:
                error="The email is already in use"
            if "username" in error:
                error="username is taken"
            
            return render_template('register.html',error=error)
        
        with profile() as newProfile:
            newProfile.create()
            newProfile.create_profile(user)
        
        return redirect("/")
        
    return render_template('register.html',error="")
