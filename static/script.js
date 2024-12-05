path = window.location.pathname
let id= 0
if (path.includes('/msg')) {
  const parts = path.split('/'); 
  id = parseInt(parts[parts.length - 1], 10); // base 10 decimal
}


document.addEventListener('DOMContentLoaded', (event) => {

    let socket = io();

    socket.on('connect', function() {

      console.log('Connected to server');
      let json = JSON.stringify({ type: "connection", session: getCookie("session"),channelid: id });
      socket.send(json)
    });

    const chat = document.getElementById('chat')
    socket.on('message', function(msg) {

      const data = JSON.parse(msg);

      
      let message = document.createElement("li")
      let user = document.createElement("div")
      let header = document.createElement("h3")
      
      header.append(document.createTextNode(data.username))
      user.append(header)

      let contents = document.createTextNode(data.message)
      message.append(user)
      message.append(contents)
      chat.append(message)
      

    });

    socket.on('disconnect', function() {

        console.log('Disconnected from server');

    });

    const button = document.getElementById('send')
    const msgBox = document.getElementById('message')

    function send() {
      

      let msg = document.getElementById('message').value;
      if(msg == "") return;
      let json = JSON.stringify({ type: "msg",message: msg, session: getCookie("session"),channelid: id });
      
      socket.send(json)
      document.getElementById('message').value = ""

    }
    
    onkeydown = (event) => {
      if(event.shiftKey) return;
      if(event.key == "Enter") send();
    };

    button.addEventListener("click",send)


    
});

if (getCookie("session") == "") window.location.replace("/")


function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }