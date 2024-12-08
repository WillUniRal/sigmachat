path = window.location.pathname
let id= 0
if (path.includes('/msg')) {
  const parts = path.split('/'); 
  id = parseInt(parts[parts.length - 1], 10); // base 10 decimal
}


function mouseX(evt) {
  if (evt.pageX) {
    return evt.pageX;
  } else if (evt.clientX) {
    return evt.clientX + (document.documentElement.scrollLeft ?
      document.documentElement.scrollLeft :
      document.body.scrollLeft);
  } else {
    return null;
  }
}

function mouseY(evt) {
  if (evt.pageY) {
    return evt.pageY;
  } else if (evt.clientY) {
    return evt.clientY + (document.documentElement.scrollTop ?
      document.documentElement.scrollTop :
      document.body.scrollTop);
  } else {
    return null;
  }
}




document.addEventListener('DOMContentLoaded', (event) => {
  const context = document.getElementById("rmenu");
  //right click menu
  document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    if (e.target && e.target.closest('li')) {
      var messageId = e.target.closest('li').getAttribute('message-id');
      if (messageId == null) return;
      console.log('Message ID:', messageId);
    } else {
      context.className = "hide"
      return;
    }
    context.className = "show";
    context.style.top = mouseY(e) + 'px';
    context.style.left = mouseX(e) + 'px';
  }, false);

  document.addEventListener("click", function(e) {
    context.className = "hide"
  });

    let socket = io();

    socket.on('connect', function() {

      console.log('Connected to server');
      let json = JSON.stringify({ type: "connection",channelid: id });
      socket.send(json)
    });

    const chat = document.getElementById('chat')
    socket.on('message', function(msg) {
      const data = JSON.parse(msg);
  
      if (Array.isArray(data)) {
        data.forEach((messageData) => {
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
  
      message.setAttribute("message-id", data.ID);
      message.setAttribute("user-id", data.userID);
  
      const contents = document.createTextNode(data.message);
      message.append(user);
      message.append(contents);
      let lines = chat.getElementsByTagName("li")

      if (data.before) {
        header.append(document.createTextNode(data.username));
        user.append(header);
        let prevusr = null
        if(lines.length != 0) {
          let prevtxt= lines[0];
          let userHead= prevtxt.querySelector("h3");
          if(userHead) prevusr = userHead.textContent;
        }
        if(prevusr == data.username) {
          console.log("rm")
          let div = lines[0].querySelector("div");
          if (div) div.remove();
        }
        
        chat.prepend(message);

      } else {
        
        let lastusr= message.getAttribute("user-id");
        if(lastusr != data.userID) {
          header.append(document.createTextNode(data.username));
          user.append(header);
        }
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
      let json = JSON.stringify({ type: "msg",message: msg, channelid: id });
      
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
      // console.log("pos "+(Math.abs(container.scrollTop) + container.clientHeight).toString())
      // console.log(container.scrollHeight)
      let oldHeight = container.scrollHeight;
      if (atTop) {

        lastmsg = chat.getElementsByTagName("li")[0].getAttribute("message-id")
        // console.log(lastmsg)
        let json = JSON.stringify({ type: "update",channelid: id ,msgID : lastmsg});
        socket.send(json)
      }
      // socket.once("message", () => {
      //   setTimeout(() => {
      //     console.log(oldHeight)
      //     container.scrollTop = oldHeight; // Adjust to compensate for added height
      //   }, 3000);
      // });
      
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
