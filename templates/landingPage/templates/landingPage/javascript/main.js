// Use a test username until the actual user is retrieved from the server.
var USERNAME="TestUser"
var TOKEN="5788ygGUYGUG86g5r7KGHJHB"
// The default recipient (and corresponding picture) is the Shoutbox.
var RECIPIENT="Shoutbox"
var RECIPIENT_PICTURE="./images/crown_a.png"

// A template for the message html. This template can be inserted
// into the chatbox in order to render a new message.
function gen_message_template(sender, message) {
	return `
		<div class="message">
			<div class="message-sender">${sender}</div>
			<div class="message-text">${message}</div>
		</div>
		<hr/>
	`;
}

// Populates the default information when the page loads.
function on_load() {
	populate_values()
}

// The purpose of this function is to set all of the different values
// on the page. It is expected that when this is called, all global
// variables have their proper values.
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

	// Indicate that messages recieved from the server will go here
	recieve_message("*** Load Messages From Server For " + RECIPIENT + " ***");
}

// Deletes all child elements of the message box, clearing it.
function clear_messages() {
	message_frame = document.getElementById('message-frame');
	while (message_frame.hasChildNodes()) {
		    message_frame.removeChild(message_frame.lastChild);
	};
}

// Placeholder fuction for the logout button.
function logout() {
	alert("Logged out");
}

// Send a message to the server.
function send_message() {
	console.log("Send message");
	var message = document.getElementById("input-field").value;
	// AJAX Send message
	recieve_message(message);
}

// Recieve a message from the server.
function recieve_message(message) {
	// AJAX Get message
	message_frame = document.getElementById('message-frame');
	message_frame.insertAdjacentHTML('beforeend', gen_message_template(USERNAME, message));
}

// The "onclick" event when selecting a friend. Based on which friend is selected, that friend's
// name and the link to their profile picture is stored, then the site repopulated.
function select_friend(object) {
	RECIPIENT = object.innerHTML;
	RECIPIENT_PICTURE = object.parentElement.getElementsByClassName('friend-photo-image')[0].src;
	populate_values();
}
