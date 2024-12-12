from flask import Flask, render_template, redirect, jsonify, make_response, request
from tables import credentials,sessions
import bcrypt
from flask_socketio import SocketIO

app = Flask(__name__)
io = SocketIO(app)

@app.before_request
def ipchecker() :
    if request.remote_addr == "banned ip  here" : 
        return deny_access()

@app.route('/.git/<path:filename>')
@app.route('/.git')
@app.route('/admin/<path:filename>')
@app.route('/admin')
@app.route('/cgi-bin/<path:filename>')
def deny_access(filename=None):
    print("Sending attacker brainrot...")
    brainrot= """Bro was posted up in the Tilted Towers lobby, hitting the griddy IRL,
    when Kai Cenat pulled up in a Skibidi Toilet doing the "gyat-certified" emote like it’s 2019 Fortnite all over again.
    Not gonna lie, the rizz was immaculate, but then someone yelled, "Sheesh, that’s an NPC move!"
    right before a Victory Royale popped on-screen, and Gyat Queen herself slid into those DMS.
    Bro hit a double pump so fast it had me thinking this wasn’t a battle bus but a rizz train straight to Rizzler City.
    W cap or nah? Livvy duune has max level GYAT ong. I aint capping when i say i am the sigma, you couldn't rizz livvy
    if you had 100 chances. only the sigmas jump for the raw beef. that raw chicken got straight ohio vibes ong fr. 
    """
    return brainrot*2**20

@app.route('/', methods = ['GET','POST'])
def login():

    error=""
    if request.method == 'POST' :
        user = request.form.get("user")
        password = request.form.get("password")
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
    def __init__(self,sesID,usrID):
        self.socket_session = sesID
        self.user_id = usrID

class Channel :
    def __init__(self, id):
        self.id = id
        self.seats = []

    def add_member(self, member : Member):
        self.seats.append(member)
    
    def remove_member(self, member : Member):
        self.seats.remove(member)
    
    def get_member(self, sid) :
        for members in self.seats:
            if members.socket_session == sid : return members


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
    
    def get_member_ses(self, userid) :
        sessions = None
        for channels in self.channels :
            for index, seats in enumerate(channels.seats):
                if seats.user_id == userid : 
                    sessions.append(channels.seats[index])

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

