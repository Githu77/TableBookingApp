from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb.cursors
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'githu'
app.config['MYSQL_PASSWORD'] = 'githu_Sql87%'
app.config['MYSQL_DB'] = 'Mandala'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		phone_number = request.form['phone_number']
		
		cur = mysql.connection.cursor()
		
		cur.execute("INSERT INTO Users (username, email, password, phone_number) VALUES (%s, %s, %s, %s)", (username, email, password, phone_number))
		
		mysql.connection.commit()
		
		cur.close()
	msg = 'Sign up seccessful!'
	return render_template('signup.html')
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)
	
if __name__ == "__main__":
	app.run(debug=True, port=8000)

