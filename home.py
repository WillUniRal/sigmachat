from __main__ import app
import sqlite3 as mysql
from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import SocketIO,send
from tables import sessions

import json

socketio = SocketIO(app)

@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')
@app.route('/msg/<int:id>', methods = ['GET'])
def dm(id):
    print(id) 
    return render_template('home.html')

@socketio.on('connect')

def handle_connect():
    print(f'Client connected {request.sid}')
    

@socketio.on('disconnect')

def handle_disconnect():

    print(f'Client connected {request.sid}')

@socketio.on('message')

def handle_message(msg):
    data = json.loads(msg) 
    message = data["message"]
    session = data["session"]
    channel = data["channelid"]

    print(session+message)
    with sessions() as sessionTable :
        try :
            username = sessionTable.getUser(session)[0]
        except TypeError:
            return

    data = {
        "username":username,
        "message":message,
        "channel": channel
    }

    send(json.dumps(data),broadcast=True)

socketio.run(app, debug=True)