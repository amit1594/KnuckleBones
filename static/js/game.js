var socket = io.connect('http://' + document.domain + ':' + location.port + "/game");

socket.on( 'connect', function() {
    console.log("connected");
    socket.emit('connect_to_game')
})

socket.on('update_turn',  function(msg) {
    var turn_h = document.getElementById("turn_h");
    turn_h.innerText = "Player " + msg.player + "'s turn!";
    if (msg.player == 1) {
        turn_h.style.color = "green";
    } else {
        turn_h.style.color = "red";
    }
    var turn_dice = document.getElementById("turn_dice");
    turn_dice.src = "static/images/dice" + msg.dice + ".png";
})

socket.on('winning_message',  function(msg) {
    alert(msg.text)
})

socket.on('update_column',  function(msg) {
    console.log("updating column:");
    console.log(msg.dices);
    var col = document.getElementById("p" + msg.board_index + "col" + msg.column_index);
    col.innerHTML = "<p class=\"column_score\">" + msg.sum + "</p>";
    for (var dice in msg.dices) {
        // alert(dice);
        col.innerHTML += create_img(msg.dices[dice]);
    }
})

socket.on('new_command',  function(msg) {
    var num =  msg.number;
    console.log("new number: " + num);
    var my_div = document.getElementById("p1col" + msg.column);
    my_div.innerHTML += create_img(num);
})


function create_img(num) {
    var pic = "dice" + num + ".png";
    var text = "";
    text += "<img class=\"dice\" src=\"static/images/" + pic + "\"/>";
    return text
}


function clicked_column(board, column) {
    console.log(column);
    socket.emit('chose_column', {board: board, column: column} );
}