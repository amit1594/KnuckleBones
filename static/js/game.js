// var url = 'http://' + document.domain + ':' + location.port + "/game";
var url = window.location.protocol + '//' + document.domain + ':' + location.port + "/game";
var socket = io.connect(url, {transports: ['websocket']});

socket.on( 'connect', function() {
    console.log("connected to " + url);
    socket.emit('connect_to_game')
})

socket.on('update_turn',  function(msg) {
    var turn_h = document.getElementById("turn_h");
    turn_h.innerText = "Player " + msg.player + "'s turn!";
    if (msg.player == 1) {
        turn_h.style.color = "blue";
    } else {
        turn_h.style.color = "red";
    }
    var turn_dice = document.getElementById("turn_dice");
    turn_dice.src = "static/images/dice" + msg.dice + ".png";
    var p1Title = document.getElementById("p1_board_title");
    p1Title.innerText = "Player 1: " + msg.p1sum;
    var p1Title = document.getElementById("p2_board_title");
    p1Title.innerText = "Player 2: " + msg.p2sum;
})

socket.on('winning_message',  function(msg) {
    document.getElementById("winning_message").innerText = msg.text;
    document.getElementById("winning_modal").classList.add("is-active");
})

socket.on('update_column',  function(msg) {
    console.log("updating column:");
    console.log(msg.dices);
    var newText = "";
    var col = document.getElementById("p" + msg.board_index + "col" + msg.column_index);
    newText = "<p class=\"column_score\">" + msg.sum + "</p>";
    for (var dice in msg.dices) {
        // alert(dice);
        newText += create_img(msg.dices[dice]);
    }
    if (newText !== col.innerHTML) {
        col.innerHTML = newText;
        var audio = new Audio('static/audio/dice.mp3');
        audio.play();
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

socket.on('reset_game',  function() {
    document.getElementById("winning_message").innerText = "";
    for (var player = 1; player <= 2; player++) {
        for (var column = 1; column <= 3; column++) {
            var curr = "p" + player + "col" + column;
            document.getElementById(curr).innerHTML = "<p class=\"column_score\">0</p>";
        }
        var title = document.getElementById("p" + player + "_board_title");
        title.innerText = "Player " + player + ": 0";
    }

})


function clicked_column(board, column) {
    console.log(column);
    socket.emit('chose_column', {board: board, column: column} );
}

function request_reset() {
    socket.emit('request_reset');
}

function request_to_become_a_player(player) {
    socket.emit('become_a_player', {player: player});
}

// CHAT

document.getElementById("chatForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var iChat = document.getElementById("inputChat");
    if (iChat.value.length > 0) {
        socket.emit( 'new_chat_message', {message: iChat.value} );
        iChat.value = "";
    }
});

function chat_handler(message) {
    // updates the chat according to the given data
    var mDiv = document.getElementById("messages");
    var myP = document.createElement("p");
    myP.innerText = message;
    myP.style.color = 'black';
    mDiv.appendChild(myP);
    var scrollIntoViewOptions = { behavior: "smooth", block: "center" };
    mDiv.scrollIntoView(scrollIntoViewOptions);
}

socket.on('new_chat_message',  function(msg) {
    chat_handler(msg.msg)
})

// MODALS

document.addEventListener('DOMContentLoaded', () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add('is-active');
  }

  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener('keydown', (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) { // Escape key
      closeAllModals();
    }
  });
});