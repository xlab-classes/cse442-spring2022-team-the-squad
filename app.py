from flask import Flask, flash, render_template, redirect, request, session, url_for

#changed MySQL connector
from flaskext.mysql import MySQL

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
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), username VARCHAR(255), pwd VARCHAR(255), pwdhint VARCHAR(255))")
    cursor.execute("SELECT * from users where username = %s AND pwd = %s", (u_username, u_password))
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

    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), username VARCHAR(255), pwd VARCHAR(255), pwdhint VARCHAR(255))")

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
        cursor.execute("INSERT INTO users(email, pwd, username) VALUES (%s, %s, %s)", (u_email, u_password, u_username))
        connection.commit()
        flash("User successfully added!") #SUCCESSFULLY REGISTER
        return redirect(url_for('login'))

#############################

@app.route('/landingPage/index.html', methods=['GET'])
def landingPage():
    return render_template('landingPage/index.html')


#############################


if __name__ == '__main__':
    #app.run(host='128.205.32.39', port=7321)
    app.run(host='0.0.0.0', port=7321)	
