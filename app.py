import sqlite3
from flask import Flask, render_template, jsonify, request
from credentials import secrets
import bcrypt

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def home():
    error=""
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
        print(user,password)
        with secrets() as credentials_table:
            
            creds = credentials_table.getUserDetails(user) 
            password = password.encode()
            
            if creds is not None and bcrypt.checkpw(password,creds[2]) :
                print("successful login")
                error = "This service is not available yet"
            else: 
                print("unsucessful login")
                error = "The password or username was incorrect"


    return render_template('home.html',error=error)

import register

if __name__ == '__main__':
    app.run(debug=True) 

