from flask import Flask, render_template, redirect, jsonify, make_response, request
from tables import credentials,sessions
import bcrypt
from flask_socketio import SocketIO

app = Flask(__name__)
io = SocketIO(app)

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

class Member :
    def __init__(self,sesID):
        self.socket_session = sesID

class Channel :
    def __init__(self, id):
        self.id = id
        self.seats = []

    def add_member(self, member : Member):
        self.seats.append(member)
    
    def remove_member(self, member : Member):
        self.seats.remove(member)

class Server :
    def __init__(self):
        #iterating through an array of channels will be O(n)
        #using binary search or linked lists will be better
        self.channels = []
    
    def add_channel(self,id):
        channel, pos = self.get_channel(id)
        if channel is None :
            channel = Channel(id)
            self.channels.insert(pos,channel)
        return channel

    def get_channel(self, id, left=None,right=None) :
        
        

        if not self.channels : return None, 0
        #binary search
        if left is None : 
            left = 0
            right = len(self.channels)

        if left >= right:
            return None, left

        middle_index = (left + right) // 2
        middle_val = self.channels[middle_index].id
        
        
        if middle_val == id : return self.channels[middle_index], left
        #0-5-10--->0-5
        if middle_val > id : right = middle_index
        #0-5-10--->6-10
        else : left = middle_index + 1

        return self.get_channel(id,left,right)

if __name__ == '__main__':
    io.run(app,host='0.0.0.0',port=80,debug=True)

