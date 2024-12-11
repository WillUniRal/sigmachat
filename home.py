from __main__ import app,io
from app import Server,Channel,Member
from tables import messages,profile,friend_requests
import sqlite3 as mysql
from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import send
from tables import sessions, profile, messages

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
    print(f'Client disconnected {request.sid}')
    global server
    for channels in server.channels :
        for index, seats in enumerate(channels.seats):
            if seats.socket_session == request.sid : 
                del channels.seats[index]

@io.on('message')
def handle_message(msg):
    data = json.loads(msg) 
    type = data["type"]

    # print(str()+"yes dingus it does send cookies with every request")
    session = request.cookies["session"]

    with sessions() as sessionTable :
        try :
            username = sessionTable.getUser(session)[0]
        except TypeError:
            return

    with profile() as client:
        clientid = client.get_userid(username)

    
    if type == "add" :
        reciever = data["user"]
        with friend_requests() as rq :
            rq.create()
            rq.send_request(clientid,reciever)
        reciever_sessions = server.get_member_ses(reciever)
        if reciever_sessions :
            data = {
                "type": "add",
                "userID": clientid
            }
            for sess in reciever_sessions :
                send(data,to=sess)
        return
        

    channel = data["channelid"]

    if type == "connection" :
        newchannel : Channel = server.add_channel(channel)
        member = Member(request.sid,clientid)
        newchannel.add_member(member)
        send(clientid)
        send_history(channel)
        return
    if type == "update" :
        send_history(channel,data["msgID"])
        return
    
    message = data["message"]

    if type == "delete":
        with messages() as msgTb :
            msgTb.delete_msg(message,clientid)
        channel , __ = server.get_channel(channel)
        data = {
            "type": "delete",
            "message": message
        }
        for members in channel.seats :
            send(json.dumps(data),to=members.socket_session)
        return
    
    with profile() as user:
        id = user.get_userid(username)

    with messages() as msgTable :
        msgTable.create()
        msgID = msgTable.add_message(id,message,channel)

    data = {
        "ID": msgID,
        "username":username,
        "message":message,
        "userID":id,
        "before":False
    }
    channel , __ = server.get_channel(channel)
    print(message)
    for members in channel.seats :
        send(json.dumps(data),to=members.socket_session)

def send_history(channel,before=None) :

    
    with messages() as msgTB :
        msgTB.create()
        if before is None :
            chat = msgTB.get_messages(channel)
        else :
            chat = msgTB.get_messages_before(channel,before)

        chunk = []
        for lotsofmessages in chat :
            with profile() as user:
                name = user.get_username(lotsofmessages[1])
            data = {
                "ID": lotsofmessages[0],
                "username":name,
                "message":lotsofmessages[2],
                "userID":lotsofmessages[1],
                "before":True
            }
        
            chunk.insert(0,data)
        send(json.dumps(chunk))
    return

