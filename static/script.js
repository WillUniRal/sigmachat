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
  
      console.log(data);
      if (Array.isArray(data)) {
        data.forEach((messageData) => {
          console.log(messageData)
          addMessageToChat(messageData);
        });
      } else {
        addMessageToChat(data);
      }
    });
    
    function addMessageToChat(data) {
      const message = document.createElement("li");
      const user = document.createElement("div");
      const header = document.createElement("h3");
  
      message.setAttribute("data-message-id", data.ID);
      header.append(document.createTextNode(data.username));
      user.append(header);
  
      const contents = document.createTextNode(data.message);
      message.append(user);
      message.append(contents);
  
      if (data.before) {
          chat.prepend(message);
      } else {
          chat.append(message);
      }
    }

    socket.on('disconnect', function() {

        console.log('Disconnected from server');

    });

    const button = document.getElementById('send')
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

    const container = document.getElementById("messaging-container")
    container.addEventListener("scroll", function(){
      const atTop = Math.abs(container.scrollTop) + container.clientHeight >= container.scrollHeight;

      if (atTop) {
        console.log(container.scrollTop)
        lastmsg = chat.getElementsByTagName("li")[0].getAttribute("data-message-id")
        let json = JSON.stringify({ type: "update", session: getCookie("session"),channelid: id ,msgID : lastmsg});
        socket.send(json)
      }
    });


    
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
