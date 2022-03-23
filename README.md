# AJAX Proof of Concept

The goal of this proof of concept is to show that it is possible to send AJAX 
messages between the client and the server without reloading the webpage. 
Furthermore, the client should be able to render AJAX messages that it receives 
from the server without having to reload the webpage. Finally, the client should 
poll the server every `x` seconds in order to retrieve new messages which it 
hasn't yet retrieved in order to render them to the page. This proof of concept 
uses only the Python Flask server and javascript to handle the AJAX 
communication.

# AJAX Message Overview

Every AJAX post request that is sent between the client and the server (in 
either direction) will be in the JSON format. All JSON messages will contain a 
`type` key, and a `data` key. The `type` key is used to determine what type of 
message the data is so that it can be handled properly. The `data` key will 
contain the message data for the respective type. The format of the `data` 
section must be consistent between each message type. There are three message 
types `message`, `sync`, and `status`. The behavior of each is determined based 
on if it is being sent from the client to the server, or from the server to the 
client. Each are defined below. In the examples below, "< >" represents where 
the respective data will be inserted, and varies between messages.

---

## Type: "message" (client -> server)

A message of type "message" that is being sent from the client to the server 
represents a message that the user wants to send. The `data` section of this 
message will contain a `sender` key and a `message` key. The `sender` key will 
be the username of the user who sent the message. The `message` key will be the 
actual message text that the user wishes to send. An example as is follows

```
{
	"type": "message",
	"data": {
		"sender": <username>,
		"message": <message>
	}
}
```

## Type: "message" (server -> client)

There is no message of type "message" that may be sent from the server to the 
client. This is only used for one-way communication where the client sends a 
message to the server.

---

## Type: "sync" (client -> server)

A message of type "sync" that is being sent from the client to the server 
represents when the client wants to receive all "new" messages from the server. 
The `data` section of this message will contain a `last_message` key. The 
`last_message` key will be the id of the most recent message that the client 
received. An example as is follows

```
{
	"type": "sync",
	"data": {
		"last_message": <message id>,
	}
}
```

## Type: "sync" (server -> client)

A message of type "sync" that is being sent from the server to the client 
represents when the server is sending all "new" messages back to the client. The 
`data` section of this message will contain a list of messages. Each element in 
the list will be a dictionary with an `id`, `sender`, and `message` key. The 
`id` key will be the id of the given message. The `sender` key will be the user 
who sent the given message. The `message` key will be the actual message text 
that the user sent. The messages in the list must be ordered by the server such 
that the first element is of the lowest id, and the last element is of the 
highest id. An example as is follows

```
{
	"type": "sync",
	"data": [
		{
			"id": <lowest message id>,
			"sender": <sender>,
			"message": <message>
		},
		{
			"id": <message id>,
			"sender": <sender>,
			"message": <message>
		},
		{
			"id": <highest message id>,
			"sender": <sender>,
			"message": <message>
		},
		...
	]
}
```

---

## Type: "status" (client -> server)

There is no message of type "status" that may be sent from the server to the 
client. This is only used for one-way communication where the client sends a 
message to the server.

## Type: "status" (server -> client)

A message of type "status" that is being sent from the server to the client 
represents if a action that the server took on the client's behalf was 
successful. The `data` section of this message will contain a `status` key and a 
`message` key. The `status` key will be a 0 if the operation succeeded, or a 1 
if the operation failed. The `message` key will be a description of where and 
why the operation failed, or where the operation succeeded. An example as is 
follows

```
{
	"type": "status",
	"data": {
		"status": <status value>,
		"message": <message>
	}
}
```
