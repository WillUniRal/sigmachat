from __main__ import app,io
from app import Server,Channel,Member
import sqlite3 as mysql
from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import send
from tables import sessions

import json

server = Server()
@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')
@app.route('/msg/<int:id>', methods = ['GET'])
def dm(id):
    print(id) 
    return render_template('home.html')

@io.on('connect')

def handle_connect():
    print(f'Client connected {request.sid}')
    

@io.on('disconnect')

def handle_disconnect():

    print(f'Client connected {request.sid}')

@io.on('message')

def handle_message(msg):
    data = json.loads(msg) 
    type = data["type"]

    session = data["session"]
    channel = data["channelid"]

    if type == "connection" :
        newchannel : Channel = server.add_channel(channel)
        member = Member(request.sid)
        newchannel.add_member(member)
        return
    
    with sessions() as sessionTable :
        try :
            username = sessionTable.getUser(session)[0]
        except TypeError:
            return
        
    message = data["message"]

    data = {
        "username":username,
        "message":message,
    }
    channel , __ = server.get_channel(channel)

    for members in channel.seats :
        print(members)
        send(json.dumps(data),to=members.socket_session)

