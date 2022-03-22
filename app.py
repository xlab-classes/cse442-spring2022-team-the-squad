# NOTE: In this proof of concept, for simplicity, all routes that are not the
# landing page were removed allong will all usage of the SQL database.
#
from flask import Flask, flash, render_template, redirect, request, session, url_for
import json

app = Flask(__name__, template_folder='templates')

CURRENT_MESSAGE_ID = 0
MOCK_DATABASE = {
    "messages": [
    
    ]
}


# When an AJAX post request is recieved and there is no data to be sent back,
# a status post request will be sent. This indicates the success or failure
# of the operation that was performed. The two statuses are 0 (success) or
# 1 (failure).
def construct_status(status, location, reason):
    return {
        "type": "status",
        "data": {
            "status": status,
            "message": "{} [{}]".format(location, reason)
        }
    }


# Used to simulate a write to the SQL database. This is called
# whenever a client sends a message to the server.
def add_message_to_database(sender, message):
    global CURRENT_MESSAGE_ID
    MOCK_DATABASE["messages"].append(
        {
            "id": CURRENT_MESSAGE_ID,
            "sender": sender,
            "message": message
        }
    )
    CURRENT_MESSAGE_ID += 1


# Returns a list of all messages that were sent after the message
# with the given index. If a client reports that it recieved
# message id 3, this will return all messages with an id of
# 4 or higher.
def get_messages_since(message_id):
    return MOCK_DATABASE["messages"][message_id+1:]


@app.route('/landingPage/index.html', methods=['GET'])
def landingPage():
    print(request.values)
    return render_template('landingPage/index.html')


# This is called every time the client sends a new message to
# the server.
@app.route('/landingPage/message', methods=['POST'])
def recieve_message():
    data = json.loads(request.get_data().decode('utf8'))

    if data.get("type") == "message":
        sender = data["data"]["sender"].strip()
        message = data["data"]["message"].strip()

        if message == "":
            return construct_status(1, "Message send failure", "blank message")

        add_message_to_database(sender, message)

        print('[message] : [{}] {}'.format(sender, message))
        return construct_status(0, "Message send success", "")

    # This return statement is irrelevant, it is not used by
    # the client, but the function is requred to return a
    # string.
    return construct_status(1, "Message send failure", "missing \"type\" \"message\"")


# This is called every time the client pings the server for new
# messages. It returns every message since the most recent that
# the client reports that it recieved.
@app.route('/landingPage/sync', methods=['POST'])
def sync_client():
    data = json.loads(request.get_data().decode('utf8'))

    if data.get("type") == "sync":
        last_message_recieved = data["data"]["last_message"]

        return_data = {
            "type": "sync",
            "data": get_messages_since(last_message_recieved)
        }

        return json.dumps(return_data)
    return construct_status(1, "Sync failure", "missing \"type\" \"sync\"")


if __name__ == '__main__':
    # Add some test messages to the mock database so that the
    # client has messages to pull when it first connects.
    add_message_to_database("Test User", "Hello guys, how's it going?")
    add_message_to_database("Other User", "Pretty good, how are you?")
    add_message_to_database("Mr. Gamer", "I just beat my game guys!")

    app.run(host='127.0.0.1', port=7321)	
