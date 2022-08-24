var url = window.location.protocol + '//' + document.domain + ':' + location.port + "/index";
var socket = io.connect(url, {transports: ['websocket']});

socket.on( 'connect', function() {
    console.log("connected to " + url);
})

socket.on( 'username_changed', function(msg) {
    var title = document.getElementById("hello_title");
    title.innerHTML = "Hello " + msg.username;
})

function send_username() {
    var username = document.getElementById("username").value;
    socket.emit('change_username', {username: username});
}

function request_current_username() {
    socket.emit('request_current_username');
}