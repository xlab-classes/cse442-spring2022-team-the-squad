from flask import Flask, render_template, request

from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "ready2learn1"
app.config['MYSQL_DB'] = "blabbr"

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def create_user():
    u_email = request.form['email']
    u_username = request.form['username']
    u_password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(email, pwd, username) VALUES (%s, %s, %s)", (u_email, u_password, u_username))
    mysql.connection.commit()
    cur.close()
    return 'User successfully added!'
    

if __name__ == '__main__':
    app.run(debug=True)