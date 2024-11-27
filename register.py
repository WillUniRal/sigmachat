from __main__ import app
from flask import Flask, render_template, jsonify, request, redirect

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
        email = request.form.get("email")
        print(user,password, email)
        return redirect("/")
        
    return render_template('register.html')
