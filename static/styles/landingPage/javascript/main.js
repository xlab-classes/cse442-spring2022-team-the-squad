const SYNC_DELAY = 1500
const SERVER_SYNC_PATH = "/landingPage/sync"
const SERVER_MESSAGE_PATH = "/landingPage/message"

// The username is retrieved from the server through a URL parameter.
var USERNAME = ""
var TOKEN = "5788ygGUYGUG86g5r7KGHJHB"
// The default recipient is the Shoutbox.
var RECIPIENT = "Shoutbox"
// The default recipient picture is that of the Shoutbox becuase that
// is the default recipient.
var RECIPIENT_PICTURE = "/static/styles/landingPage/images/crown_a.png"
// The ID of the most recent message that the client recieved. This
// must be a valid message ID, or -1 if no messages have been recieved.
var LAST_MESSAGE = -1


// Create a sleep function in order to delay execution.
const sleep = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds))


// A template for the message html. This template can be inserted
// into the chatbox in order to render a new message.
function gen_message_template(sender, message) {
	// escape html characters
	message = message.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;")
	return `
		<div class="message">
			<div class="message-sender">${sender}</div>
			<div class="message-text">${message}</div>
		</div>
		<hr/>
	`;
}


// Submit an AJAX post request to the server.
function ajaxPostRequest(path, data, callback){
    let request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState===4&&this.status ===200){
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(data);
}


// Handle all AJAX responses from the server. Since every AJAX message that
// is sent has a "type" field. The "type" field indicates what the response
// is, and that can be used to determine how to act on the contained data.
// Every time there is an ajaxPostRequest call, this function should always
// be used as the callback, as it handles all AJAX responses from the server.
function ajax_callback(response) {
	const data = JSON.parse(response);
	console.log("AJAX \"" + data["type"] + "\" message recieved");

	// The AJAX response that was recieved is a "sync" response. This means
	// that the server has sent us new messages, process those below.
	if (data["type"] == "sync") {
		const messages = data["data"];
		for (let message of messages) {
			// console.log("Message recieved : [" + message["sender"] + "] " + message["message"])
			LAST_MESSAGE = Math.max(message["id"], LAST_MESSAGE);
			create_message(message["sender"], message["message"]);
		}
		return;
	}
	// The AJAX response that was recieved is a "status" response. This means
	// that the server acted on our request and is returning the status of
	// the request
	else if (data["type"] == "status") {
		console.log(response);
		return;
	}
	// If we are here then the AJAX response did not contain a recognized
	// response "type". This should not occur becuase the server should
	// only send responses that will be recognized by the client. We will
	// warn about that here.
	console.log("WARNING: Unknown AJAX response type or JSON response " +
		"missing the \"type\" key. Response: " + response)
}


// Populates the default information when the page loads and
// initiates the asynchronous client sync function.
function gen_friend_template(friend) {
	return `
	<div class="friend" onclick="select_friend(this)">
		<div class="friend-photo">
			<img src="{{ url_for('static',filename='styles/landingPage/images/crown_a.png') }}" class="friend-photo-image">
		</div>
		<div class="friend-name">${friend}</div>
	</div>
`;
}

// Populates the default information when the page loads.
function on_load() {
	const params = new URLSearchParams(window.location.search);
	USERNAME = params.get("username");

	if (params.get("username") == null) {
		USERNAME = "Guest";
	}

	// This needs to be called before the sync_messages "thread" is started.
	// This is because the populate_values function clears the chat box, and
	// we don't want the chat box to be cleared after messages have been
	// recieved.
	populate_values()

	// Create a new "thread" so that we can recieve messages
	// from the server asynchronously. This will ping the
	// server every X seconds to have it send back all new
	// messages.
	const sync_messages = async () => {
		while (true) {
			data = {
				"type": "sync",
				"data": {
					"last_message": LAST_MESSAGE
				},
				"user": USERNAME,
				"recipeint": RECIPIENT,
			}
			data_string = JSON.stringify(data);

			ajaxPostRequest(SERVER_SYNC_PATH, data_string, ajax_callback);
			await sleep(SYNC_DELAY);
		}
	}
	sync_messages();

	// Register event listener on the "Send" button. This allows
	// messages to be sent by pressing the Enter key.
	submit_button = document.getElementById("input-field");
	submit_button.addEventListener("keydown", function (event) {
            if (event.keyCode == 13) {
		send_message();
            }
        });
}


// The purpose of this function is to set all of the different values on the
// page, with the exception of displaying messages. This includes displaying
// the user's profile name, the recpient's name, and the recipient's profile
// picture. It is expected that when this is called, all global variables have
// their proper values. This should be called any time the page is loaded or
// the selected friend chat is changed.
function populate_values() {
	// Set the profile name
	profile_name_element = document.getElementById('profile-name');
	profile_name_element.innerHTML = USERNAME;

	// Set the recipient name
	recipient_name_element = document.getElementById('recipient-name');
	recipient_name_element.innerHTML = RECIPIENT;

	// Set the recipient picture
	recipient_profile_picture_element = document.getElementById('recipient-photo-image');
	recipient_profile_picture_element.src = RECIPIENT_PICTURE;

	clear_messages();
}


// Send a message to the server. The message is retrieved from the input box
// on the page and sent to the server in an AJAX post request.
function send_message() {
	console.log("Send message");
	const message = document.getElementById("input-field").value;
	document.getElementById("input-field").value = "";

	data = {
		"type": "message",
		"data": {
			"sender": USERNAME,
			"message": message,
			"recipient": RECIPIENT
		}
	};

	data_string = JSON.stringify(data);
	ajaxPostRequest(SERVER_MESSAGE_PATH, data_string, ajax_callback);
}


// Render a new message to the page. This will create new HTML using the message
// template and insert it into the chat box after all other messages.
function create_message(sender, message) {
	message_frame = document.getElementById('message-frame');
	message_frame.insertAdjacentHTML('beforeend', gen_message_template(sender, message));
}


// Deletes all child elements of the message box, clearing it.
function clear_messages() {
	message_frame = document.getElementById('message-frame');
	while (message_frame.hasChildNodes()) {
		    message_frame.removeChild(message_frame.lastChild);
	};
}

/* Deletes all child elements of the friends list, clearing it.
function clear_friends() {
	friends_frame = document.getElementById('friends-frame');
	while (friends_frame.lastChild.innerText != "Shoutbox") {
			friends_frame.removeChild(friends_frame.lastChild);
	};
}*/

// Placeholder fuction for the logout button.
function logout() {
	window.location.href = "../logout.html";
}

function examine_add_input() {
	const selected_user = document.getElementById('selected-friend').value;
	document.getElementById("add-button").disabled =
	selected_user.length === 0 ||
	document.querySelector('option[value="' + selected_user + '"]') === null;
}

function add_friend() {
	console.log("Add friend");
	var friend = document.getElementById("selected-friend").value;
	// AJAX Send message
	list_friend(friend);
}

// Recieve a message from the server.
function list_friend(friend) {
	// AJAX Get message
	friends_frame = document.getElementById('friends-frame');
	friends_frame.insertAdjacentHTML('beforeend', gen_friend_template(friend));
}

// The "onclick" event when selecting a friend. Based on which friend is selected, that friend's
// name and the link to their profile picture is stored, then the site repopulated.
function select_friend(object) {
	// In every "friend" div there is only one object with the 'friend-name' and one object
	// with the 'friend-photo-image' class tag. The clicked "friend" div is passed in so we
	// can just find the first child of the given classes, since there should only be one
	// of each.
	RECIPIENT = object.getElementsByClassName('friend-name')[0].innerHTML;
	RECIPIENT_PICTURE = object.getElementsByClassName('friend-photo-image')[0].src;
	populate_values();

	// When the chat box is switched to a different friend, it is cleared.
	// Thus, there will be no previous messages. We need to reset the last
	// message counter so that it will display all messages.
	LAST_MESSAGE = -1;
}


