from stat import FILE_ATTRIBUTE_NO_SCRUB_DATA
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flaskext.mysql import MySQL
import json

# initialize global mySQL connection
app = Flask(__name__, template_folder='templates')

#for sessions
app.secret_key = "the squad"

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = "shawnkop"
app.config['MYSQL_DATABASE_PASSWORD'] = "50356342"
app.config['MYSQL_DATABASE_DB'] = "cse442_2022_spring_team_x_db"
app.config['MYSQL_DATABASE_HOST'] = "oceanus.cse.buffalo.edu"
app.config['MYSQL_PORT'] = 3306

mysql.init_app(app)
connection = mysql.connect()
chatconnection = mysql.connect()

# create tables if they do not exist
connection.ping(reconnect=True)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), username VARCHAR(255), pwd VARCHAR(255),  pwdhint VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS messages(id MEDIUMINT NOT NULL AUTO_INCREMENT, sender VARCHAR(255), message VARCHAR(2048), recipient VARCHAR(255), PRIMARY KEY (id))")
connection.commit()

#-------------------------------------
#           -FLASK ROUTING-
#-------------------------------------
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#######################

@app.route('/login.html', methods=['GET'])
def login():
    return render_template('login.html')    


###########################
@app.route('/login.html', methods=['POST'])
def login_user():

    u_username = request.form['uname']
    u_password = request.form['pwd']

    connection.ping(reconnect=True)
    cursor = connection.cursor()
    cursor.execute("SELECT * from users where username = %s AND PWD = %s", (u_username, u_password))
    connection.commit()
    result = cursor.fetchall()

    if len(result) == 0:
        flash("No user found with that information")
        return render_template('login.html')
    else:
        session['username'] = u_username
        return redirect(url_for('landingPage', username=session['username']))

###########################

@app.route('/logout.html')
def logout_user():
    if "username" in session:
        session.pop('username', None)

    return redirect(url_for('home'))

###########################

@app.route('/register.html', methods=['GET'])
def register():
    return render_template('register.html')

#############################

@app.route('/register.html', methods=['POST'])
def create_user():
    u_email = request.form['email']
    u_username = request.form['uname']
    u_password = request.form['pwd']
    u_pwdhint = request.form['pwdhint']

    connection.ping(reconnect=True)
    cursor = connection.cursor()
    #check if username and/or email already exists 
    cursor.execute("SELECT * from users where username = %s OR email = %s", (u_username, u_email))
    connection.commit()
    result = cursor.fetchall()

    if len(result) > 0:
        for rows in result:
            if rows[0] == u_email and rows[1] == u_username:     
                flash("A user with that email and username already exists")
                return render_template('register.html')
            if rows[0] == u_email and rows[1] != u_username:
                flash("A user with that email already exists")
                return render_template('register.html')
            if rows[1] == u_username and rows[0] != u_email:
                flash("A user with that username already exists")
                return render_template('register.html')
    else:
        cursor.execute("INSERT INTO users(email, username, pwd, pwdhint) VALUES (%s, %s, %s, %s)", (u_email, u_username, u_password, u_pwdhint))
        connection.commit()
        flash("User successfully added!") #SUCCESSFULLY REGISTER
        return redirect(url_for('login'))


###########################################################################################################################################################################################################
#                                                                                         FLASK  AJAX                                                                                                     #                             
###########################################################################################################################################################################################################


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
def add_message_to_database(sender, message, recipient):
    chatconnection.ping(reconnect=True)
    cursor = chatconnection.cursor()
    cursor.execute("INSERT INTO messages(sender, message, recipient) VALUES (%s, %s, %s)", (sender, message, recipient))
    chatconnection.commit()

# Returns a list of all messages that were sent after the message
# with the given index. If a client reports that it recieved
# message id 3, this will return all messages with an id of
# 4 or higher.
def get_messages_since(message_id, user, recipient):
    chatconnection.ping(reconnect=True)
    cursor = chatconnection.cursor()
    if recipient == "Shoutbox":
        cursor.execute("SELECT * from messages where id > %s AND recipient = %s", (message_id, recipient))
    else:
        cursor.execute("SELECT * from messages where (id > %s AND sender = %s AND recipient = %s) OR (id > %s AND recipient = %s AND sender = %s AND NOT sender = 'Shoutbox')", (message_id, user, recipient, message_id, user, recipient))
    chatconnection.commit()
    result = cursor.fetchall()
    final = []
    for i in result:
        final.append(
            {
                "id": i[0],
                "sender": i[1],
                "message": i[2]
            }
        )
    return final
    
###########################################################################################################################################################################################################


@app.route('/forgotpassword.html', methods=['GET'])
def forgot_page():
    return render_template('forgotpassword.html')

#############################

@app.route('/forgotpassword.html', methods=['POST'])
def forgot_password():
    u_email = request.form['email']

    connection.ping(reconnect=True)
    cursor = connection.cursor()
    cursor.execute("SELECT * from users where email = %s", u_email)
    connection.commit()
    result = cursor.fetchall()

    if len(result) > 0:
        #retrieve result from the result's row
        pw_hint = ""
        for rows in result:
            #flash("Password Hint:", rows[3])
            pw_hint = rows[3]
        return redirect(url_for('login', hint=pw_hint))
    else:
        flash("No user found with that information")
        return render_template('forgotpassword.html')

#############################

@app.route('/landingPage/index.html', methods=['GET'])
def landingPage():
    print(request.values)
    #code for generating add users list
    connection.ping(reconnect=True)

    
    if "username" in session:
        cursor = connection.cursor()
        cursor.execute("SELECT username from users where username != %s", session["username"])
        connection.commit()
        result = cursor.fetchall()

        if len(result) > 0:
            a_list = []
            for row in result:
                a_list.append(row[0])

        #code for generating friends list
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        cursor.execute("SELECT receiver from friends where sender = %s", session["username"])
        connection.commit()
        result = cursor.fetchall()

        if len(result) > 0:
            f_list = []
            for row in result:
                f_list.append(row[0])
            return render_template('landingPage/index.html', add_list=a_list, friend_list=f_list)
        else:
            return render_template('landingPage/index.html', add_list=a_list, friend_list=[])
    else:
        connection.ping(reconnect=True)

        return render_template('landingPage/index.html')


# This is called every time the client sends a new message to
# the server. The message is added to the database and a status
# AJAX post request is sent detailing if the message was stored
# sucessfuly.
@app.route('/landingPage/message', methods=['POST'])
def recieve_message():
    data = json.loads(request.get_data().decode('utf8'))

    # This route should only recieve AJAX post requests of type "message". Any
    # other AJAX post request type sent to this route is invalid and should
    # return a failure message.
    if data.get("type") == "message":
        sender = data["data"]["sender"].strip()
        message = data["data"]["message"].strip()
        recipient = data["data"]["recipient"].strip()

        # We don't want to store blank messages, ignore them here.
        if message == "":
            return construct_status(1, "Message send failure", "blank message")

        add_message_to_database(sender, message, recipient)

        print('[message] : [{}] {}'.format(sender, message))
        return construct_status(0, "Message send success", "")

    return construct_status(1, "Message send failure", "missing \"type\" \"message\"")


# This is called every time the client pings the server for new
# messages. It returns every message since the most recent that
# the client reports that it recieved.
@app.route('/landingPage/sync', methods=['POST'])
def sync_client():
    data = json.loads(request.get_data().decode('utf8'))

    # This route should only recieve AJAX post requests of type "sync". Any
    # other AJAX post request type sent to this route is invalid and should
    # return a failure message.
    if data.get("type") == "sync":
        last_message_recieved = data["data"]["last_message"]
        user = data["user"]
        recipient = data["recipeint"]

        return_data = {
            "type": "sync",
            "data": get_messages_since(last_message_recieved, user, recipient)
        }

        return json.dumps(return_data)
    return construct_status(1, "Sync failure", "missing \"type\" \"sync\"")


#############################

@app.route('/landingPage/index.html', methods=['POST'])
def add_friend():
    u_receiver = request.form['select_friend']
    print(u_receiver)

    connection.ping(reconnect=True)
    cursor = connection.cursor()

    cursor.execute("SELECT * from users where username = %s", u_receiver)
    connection.commit()
    result = cursor.fetchall()

    
    #add check to see if they arent already friends
    cursor.execute("SELECT * FROM friends where sender = %s AND receiver = %s", (session["username"], u_receiver))
    connection.commit()
    result = cursor.fetchall()

    if len(result) == 0:
        cursor.execute("INSERT INTO friends(sender, receiver) VALUES (%s, %s)", (session["username"], u_receiver))
        connection.commit()
        #now create second row with swapped vals
        cursor.execute("INSERT INTO friends(sender, receiver) VALUES (%s, %s)", (u_receiver, session["username"]))
        connection.commit()
    

    #code for generating friends list
    cursor.execute("SELECT receiver from friends where sender = %s", session["username"])
    connection.commit()
    result = cursor.fetchall()


    if len(result) > 0:
        f_list = []
        for row in result:
            f_list.append(row[0])
    
    #code for generating add users list
    cursor.execute("SELECT username from users where username != %s", session["username"])
    connection.commit()
    result = cursor.fetchall()

    if len(result) > 0:
        a_list = []
        for row in result:
            a_list.append(row[0])
    
    return render_template('landingPage/index.html', friend_list=f_list, add_list=a_list)
    
    


if __name__ == '__main__':
    #app.run(host='128.205.32.39', port=7321)
    app.run(host='0.0.0.0', port=7321)	
