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
  const home_button = document.getElementById("home")
  if(id==0) {
    home_button.className = home_button.className.toggle_class("selected")
  } else {
    home_button.addEventListener("click", function(e) {
      window.location.replace("/home")
    });
  }

  const context = document.getElementById("rmenu");
  //right click menu
  let selectedMSG = null;
  let user = null;
  let msg = null;
  
  document.addEventListener('contextmenu', function(e) {
    msg = e.target.closest('li')
    // console.log(msg.previousElementSibling)
    e.preventDefault();
    if (e.target && msg) {
      selectedMSG = msg.getAttribute('message-id');
      if (selectedMSG == null) return;
      user = msg.getAttribute('user-id');
    } else {
      context.className = context.className.toggle_class("hide")
      return;
    }
    buttons = context.getElementsByTagName("li")
    if(user == localStorage.getItem("userid")) {
      buttons[0].className = ""
      buttons[1].className = "hide"
    } else {
      buttons[0].className = "hide"
      buttons[1].className = ""
    }
    context.className = "show";
    context.style.top = mouseY(e) + 'px';
    context.style.left = mouseX(e) + 'px';
  }, false);
  context.addEventListener("click", function(e) {
    if(e.target.closest('li').innerHTML == "Delete message") {
      let json = JSON.stringify({ type: "delete",message: selectedMSG,channelid: id});
      socket.send(json)
      // delete_msg(msg)
    }
    if(e.target.closest('li').innerHTML == "Add friend") {
      let json = JSON.stringify({ type: "add",user: user});
      socket.send(json)
    }
    if(e.target.closest('li').innerHTML == "Copy text" && navigator.clipboard) {
      let divIndex = msg.innerHTML.indexOf("</div>");
      let contentAfterDiv = msg.innerHTML
      if (divIndex !== -1) {
        contentAfterDiv = msg.innerHTML.substring(divIndex + 6);
      }
      navigator.clipboard.writeText(contentAfterDiv)
        .then(() => {
          console.log("Text copied to clipboard successfully!");
        })
        .catch((err) => {
          console.error("Failed to copy text to clipboard: ", err);
        });
    }
  });

  function delete_msg(msg) {
    console.log(msg)
    let thisID = msg.getAttribute("user-id")
    let nextID = null
    if(msg.nextElementSibling) {
      nextID = msg.nextElementSibling.getAttribute("user-id") 
    }
    if(msg.querySelector("div") && thisID == nextID) {
      msg.nextElementSibling.innerHTML = msg.innerHTML.substring(0,msg.innerHTML.indexOf("</div>")+6) + msg.nextElementSibling.innerHTML
    }
    msg.remove();
  }

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
    if(Number.isInteger(msg)) {
      localStorage.setItem("userid",msg);
      return;
    }
    let data;
    data = JSON.parse(msg);
    if(data.type) {
      if(data.type == "delete") {
        delete_msg(binarySearch(chat.getElementsByTagName("li"),data.message))
        return;
      } else {
        addFriendRequest(data.userID)
      }
    }
    
    if (Array.isArray(data)) {
      data.forEach((messageData) => {
        addMessageToChat(messageData);
      });
    } else {
      addMessageToChat(data);
    }
  });

  const sidebar = document.getElementById("sidebar")
  const fr = function addFriendRequest(user) {
    const newrequest = document.createElement("div");
    newrequest.className = "side-button"
    newrequest.setAttribute("user-id",user)
    sidebar.append(newrequest)
  }
  
  function addMessageToChat(data) {
    const message = document.createElement("li");
    const user = document.createElement("div");
    const header = document.createElement("h3");

    message.setAttribute("message-id", data.ID);
    message.setAttribute("user-id", data.userID);

    const contents = document.createTextNode(data.message);
    
    
    let lines = chat.getElementsByTagName("li");

    if (data.before) {
      message.append(user);
      header.append(document.createTextNode(data.username));
      user.append(header);
      let prevusr = null
      if(lines.length != 0) {
        let prevtxt= lines[0];
        let userHead= prevtxt.querySelector("h3");
        if(userHead) prevusr = userHead.textContent;
      }
      if(prevusr == data.username) {
        let div = lines[0].querySelector("div");
        if (div) div.remove();
      }
      message.append(contents);
      chat.prepend(message);

    } else {
      let lastusr = null;
      try {
      lastusr= lines[lines.length-1].getAttribute("user-id");
      } catch {

      }
      console.log(lastusr+" "+data.userID)
      if(lastusr != data.userID || lines.length == 0) {
        message.append(user);
        header.append(document.createTextNode(data.username));
        user.append(header);
      }
      message.append(contents);
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
let binarySearch = function (arr, mesg, left=0, right=arr.length) {

  if (left > right) return false;
  let mid = Math.floor((left + right) / 2);
  midvalue = arr[mid].getAttribute("message-id")
  console.log(midvalue+" finding: "+mesg)
  if (midvalue == mesg) return arr[mid];

  if (parseInt(midvalue) > parseInt(mesg))
      return binarySearch(arr, mesg, left, mid - 1);
  else
      return binarySearch(arr, mesg, mid + 1, right);
}

String.prototype.toggle_class = function(_class) {
  let classes = this.trim().split(/\s+/);
  const index = classes.indexOf(_class);

  if (index !== -1) 
    classes.splice(index, 1);
  else 
    classes.push(_class);

  return classes.join(" ");
}

