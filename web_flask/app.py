from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb.cursors
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_pyfile('config.py')


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
			session['email'] = account['email']
			msg = 'Logged in successfully!'
			return redirect(url_for('history'))
		return render_template('dashboard.html', username=session['username'])
	else:
		msg = 'Incorrect username/password!'
	return render_template('signup.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Reservations WHERE username = %s', (username,))
    reservations = cur.fetchall()
    cur.close()
    return redirect(url_for('history'))
    return render_template('dashboard.html', reservations=reservations)
	
@app.route('/book',methods=['GET', 'POST'])
def book():
	if request.method == 'POST':
		guests = request.form['guests']
		seating_preference = request.form['seating_preference']
		reservation_date = request.form['reservation_date']
		reservation_time = request.form['reservation_time']
		special_request = request.form['special_request']

		username = session.get('username')
		email = session.get('email')

		if not username or not email:
			return "User information not found in session.", 400

		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO Reservations (username, email, guests, seating_preference, reservation_date, reservation_time, special_request) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, email, guests, seating_preference, reservation_date, reservation_time, special_request))

		mysql.connection.commit()

		cur.close()
		msg = 'Successful'
		return redirect(url_for('history'))
		return render_template('dashboard.html')
	
@app.route('/history')
def history():
    if 'loggedin' not in session:
        return redirect(url_for('signup'))
    
    username = session['username']
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Reservations WHERE username = %s', (username,))
    reservations = cur.fetchall()
    
    cur.close()
    
    return render_template('history.html', reservations=reservations)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('signup'))

if __name__ == "__main__":
	app.run(debug=True, port=8000)

