import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
        print(user,password)
        
    return render_template('home.html')

import register

if __name__ == '__main__':
    app.run(debug=True) 

