
document.addEventListener('DOMContentLoaded', (event) => {

    let socket = io();

    socket.on('connect', function() {

        console.log('Connected to server');

    });

    const chat = document.getElementById('chat')
    socket.on('message', function(msg) {

      let message = document.createElement("li")
      let contents = document.createTextNode(msg)
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
      let payload = JSON.stringify({ message: msg, session: getCookie("session") });
      
      console.log(msg)
      socket.send(payload)
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