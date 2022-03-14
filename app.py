from flask import Flask, render_template, request
from flask_mysqldb import MySQL

# initialize global mySQL connection
app = Flask(__name__, template_folder='templates')
app.config['MYSQL_HOST'] = "oceanus.cse.buffalo.edu"
app.config['MYSQL_USER'] = "anprimos"
app.config['MYSQL_PASSWORD'] = "50184265"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = "cse442_2022_spring_team_x_db"
mysql = MySQL(app)

# insert email / pwd / username into the users table
def mySQL_insert(email, pwd, username):
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), pwd VARCHAR(255), username VARCHAR(255))")
    cur.execute("INSERT INTO users(email, pwd, username) VALUES (%s, %s, %s)", (email, pwd, username))
    mysql.connection.commit()
    cur.close()

# check the users pass to see if it matches
# returns True or False
def mySQL_check_pass(user, pwd):
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), pwd VARCHAR(255), username VARCHAR(255))")
    cur.execute("SELECT * FROM users WHERE username = '"+user+"'")
    rows = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return rows[0][1] == pwd


# check if username / email exists already in the database
# returns True of False
def mySQL_check_key_exists(key, value):
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255), pwd VARCHAR(255), username VARCHAR(255))")
    cur.execute("SELECT * FROM users WHERE "+key+" = '"+value+"'")
    rows = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return len(rows) > 0


#-------------------------------------
#           -FLASK ROUTING-
#-------------------------------------
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def create_user():
    u_email = request.form['email']
    u_username = request.form['username']
    u_password = request.form['password']

    if not (mySQL_check_key_exists("username",u_username)):
        mySQL_insert(u_email, u_password, u_username)
    else:
        return 'User already exists!' #DO NOT ALLOW TO REGISTER, USERNAME ALREADY EXISTS
    return 'User successfully added!' #SUCCESSFULLY REGISTER


if __name__ == '__main__':
    app.run(debug=True)