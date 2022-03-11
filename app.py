from flask import Flask, render_template, request

from flask_mysqldb import MySQL


def mySQL_Connect(app):
    
    app.config['MYSQL_HOST'] = "oceanus.cse.buffalo.edu"
    app.config['MYSQL_USER'] = "anprimos"
    app.config['MYSQL_PASSWORD'] = "50184265"
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_DB'] = "cse442_2022_spring_team_x_db"
    return app

app = Flask(__name__, template_folder='templates')
app = mySQL_Connect(app)


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