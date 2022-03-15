from flask import Flask, render_template, request

#changed MySQL connector
from flaskext.mysql import MySQL

# initialize global mySQL connection
app = Flask(__name__, template_folder='templates')

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = "shawnkop"
app.config['MYSQL_DATABASE_PASSWORD'] = "50356342"
app.config['MYSQL_DATABASE_DB'] = "cse442_2022_spring_team_x_db"
app.config['MYSQL_DATABASE_HOST'] = "oceanus.cse.buffalo.edu"
app.config['MYSQL_PORT'] = 3306

mysql.init_app(app)

connection = mysql.connect()

# insert email / pwd / username into the users table
"""
def mySQL_insert(email, pwd, username):
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), pwd VARCHAR(255), username VARCHAR(255))")
    cur.execute("INSERT INTO users(email, pwd, username) VALUES (%s, %s, %s)", (email, pwd, username))
    mysql.connection.commit()
    cur.close()
"""

# check the users pass to see if it matches
# returns True or False
"""
def mySQL_check_pass(user, pwd):
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), pwd VARCHAR(255), username VARCHAR(255))")
    cur.execute("SELECT * FROM users WHERE username = '"+user+"'")
    rows = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return rows[0][1] == pwd
"""

# check if username / email exists already in the database
# returns True of False
"""
def mySQL_check_key_exists(key, value):
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), pwd VARCHAR(255), username VARCHAR(255))")
    cur.execute("SELECT * FROM users WHERE "+key+" = '"+value+"'")
    rows = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return len(rows) > 0
"""

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
    msg = ""

    u_username = request.form['uname']
    u_password = request.form['pwd']
    cursor = connection.cursor()

    cursor.execute("SELECT * from users where username = %s AND PWD = %s", (u_username, u_password))
    connection.commit()
    result = cursor.fetchall()

    if len(result) == 0:
        msg = "No user found with that information"
    else:
        msg = "Logged in!"

    return render_template('login.html', login_msg=msg)


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
    msg = ""

    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(email, pwd, username) VALUES (%s, %s, %s)", (u_email, u_password, u_username))
    connection.commit()

    #if not (mySQL_check_key_exists("username",u_username)):
    #    mySQL_insert(u_email, u_password, u_username)
    #else:
    #    return 'User already exists!' #DO NOT ALLOW TO REGISTER, USERNAME ALREADY EXISTS
    msg = "User successfully added!" #SUCCESSFULLY REGISTER
    
    
    return render_template('register.html', report_msg=msg)



if __name__ == '__main__':
    app.run(host='128.205.32.39', port=7321)