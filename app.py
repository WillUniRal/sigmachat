import sqlite3
from flask import Flask, render_template, redirect, jsonify, make_response, request
from tables import credentials,sessions
import bcrypt

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def login():
    error=""
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
        print(user,password)
        with credentials() as credentials_table:

            credentials_table.create()
            
            creds = credentials_table.getUserDetails(user) 
            password = password.encode()

            if creds is not None and bcrypt.checkpw(password,creds[2]) :
                print("successful login")
                with sessions() as session :
                    session.create()
                    sessionID = session.login(user)
                    response = make_response(redirect('/home'))
                    response.set_cookie("session",sessionID)
                    return response

            else: 
                print("unsucessful login")
                error = "The password or username was incorrect"


    return render_template('login.html',error=error)

import register
import home

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True) 

