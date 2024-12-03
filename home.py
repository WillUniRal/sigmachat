from __main__ import app
import sqlite3 as mysql
from flask import Flask, render_template, jsonify, request, redirect
from flask_socketio import SocketIO,send
from tables import sessions

import json

socketio = SocketIO(app)

@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')
@app.route('/msg/<int>:id',)
@app.route('/home', methods = ['GET'])
def dm(id):
    pass

@socketio.on('connect')

def handle_connect():

    print('Client connected')


@socketio.on('disconnect')

def handle_disconnect():

    print('Client disconnected')

@socketio.on('message')

def handle_message(msg):
    data = json.loads(msg) 
    message = data["message"]
    session = data["session"]

    print(session+message)
    with sessions() as sessionTable :
        username = sessionTable.getUser(session)[0]

    

    send(f"{username}: {message}", broadcast=True)

socketio.run(app, debug=True)