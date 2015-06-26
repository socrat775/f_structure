var socket = new WebSocket("ws://localhost:8888/websocket/")
var list_functions = [Directory];

socket.onopen = function() {
    alert("connect!");
    window.handler = new Directory(); //global handler, becerfull!1
}

socket.onmessage = function(event) {
    data = JSON.parse(event.data);

    for (var key in data)
       { handler[key](data[key]);
         alert(path); }
}

socket.onclose = function() {
    alert("Connection is closed");
}

/////////////////////////////////////
function Directory() {
    var path = [["root", "dir"]];

    this.callback = function(name) {
       if (name.type == "workspace")
          { name.p.push([name.value, name.nametype]); }
       else if (name.type == "pathspace") {
          while (path.length != name.p.length)
               { path.pop(); } 
          }
       var response_data = {"DIRECTORY": {"show": name.p}};
       return socket.send(JSON.stringify(response_data));
    }

    this.SHOW_ELEMENTS = function(data) {
       var node = document.getElementById("show_path");
       var children = node.childNodes;
       while (children.length)
          { node.removeChild(children[0]); }

       var count = 0;
       while (count < path.length) {
          var el_p = document.createElement("div");
          el_p.type = "pathspace";
          el_p.appendChild(document.createTextNode(path[count][0]));
          el_p.p = [];
          for (var i = 0; i <= count; i ++)
             { el_p.p.push([path[i][0], path[i][1]]); }
          el_p.setAttribute('id', 'elementofpath');
          el_p.setAttribute('onclick', 'handler.callback(this)');
          document.getElementById("show_path").appendChild(el_p);
          count ++;
       }


       var node = document.getElementById("element");
       var children = node.childNodes;
       while (children.length)
          { node.removeChild(children[0]); }

       for (var i=0; i < data.length; i++) {
          var el = document.createElement('div');
          el.type = "workspace";
          el.p = path;
          el.value = data[i][0];
          el.nametype = data[i][1];
          el.setAttribute('id', 'new_element');
          el.appendChild(document.createTextNode(data[i][0]));
          el.appendChild(document.createTextNode(data[i][1]));
          el.setAttribute('onclick', 'handler.callback(this)');
          document.getElementById("element").appendChild(el);
       }
    }

    this.MAKE_ELEMENT = function() {
       var copy = []
       for (var i = 0; i < path.length; i ++)
          { copy.push(path[i]); }

       copy.push([prompt("name:"), prompt("type:")]);
       return socket.send(JSON.stringify({"DIRECTORY": {"add": copy}}));
    }

    this.MAKE_DIR = function() {
       var el = document.createElement('div');
       el.type = "workspace";
       el.nametype = "dir";
       el.value = prompt();
       el.setAttribute('id', 'new_element');
       el.appendChild(document.createTextNode(el.value));
       el.appendChild(document.createTextNode("dir"));
       document.getElementById("element").appendChild(el);

       var copy = []
       for (var i = 0; i < path.length; i ++)
          { copy.push(path[i]); }
       copy.push([el.value, "dir"]);

       return socket.send(JSON.stringify({"DIRECTORY": {"add": copy}}));
    }

    this.ERROR = function(er) {
       alert(er);
    }
}

