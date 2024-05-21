from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb.cursors
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'githu'
app.config['MYSQL_PASSWORD'] = 'githu_Sql87%'
app.config['MYSQL_DB'] = 'Mandala'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('adminsignup.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/signup',methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		
		cur = mysql.connection.cursor()
		hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		cur.execute("INSERT INTO admin (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
		
		mysql.connection.commit()
		
		cur.close()
	msg = 'Sign up seccessful!'
	return render_template('adminsignup.html')
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account and bcrypt.checkpw(password.encode('utf-8'), account['password'].encode('utf-8')):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            msg = 'Logged in successfully!'
            return redirect(url_for('admindashboard'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('adminsignup.html', msg=msg)

@app.route('/reservations')
@login_required
def reservations():
    if 'loggedin' not in session:
        return redirect(url_for('adminsignup'))
    
    username = session['username']
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Reservations')
    reservations = cur.fetchall()
    
    cur.close()
    
    return render_template('reservations.html', reservations=reservations)	

@app.route('/admindashboard')
@login_required
def admindashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Reservations')
    reservations = cur.fetchall()
    cur.close()
    return redirect(url_for('reservations'))
    return render_template('admindashboard.html', reservations=reservations)
	
@app.route('/logout')
@login_required
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return render_template('adminsignup.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0')
