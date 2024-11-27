import sqlite3
from flask import Flask, render_template, jsonify, request
from credentials import secrets
import bcrypt

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
        print(user,password)
        with secrets() as credentials_table:
            creds = credentials_table.getUserDetails(user) 
            password = password.encode()
            hashed_password = bcrypt.hashpw(password, creds[3])
            if hashed_password == creds[2] : print("successful login")
            else: print("unsucessful login")


    return render_template('home.html')

import register

if __name__ == '__main__':
    app.run(debug=True) 

