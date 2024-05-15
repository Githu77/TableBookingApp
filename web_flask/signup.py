from flask import Flask, render_template, request

from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'githu'
app.config['MYSQL_PASSWORD'] = 'githu_Sql87%'
app.config['MYSQL_DB'] = 'Mandala'

mysql = MySQL(app)


@app.route('/',methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		phone_number = request.form['phone_number']
		
		cur = mysql.connection.cursor()
		
		cur.execute("INSERT INTO Users (username, email, password, phone_number) VALUES (%s, %s, %s, %s)", (username, email, password, phone_number))
		
		mysql.connection.commit()
		
		cur.close()
	
	return render_template('signup.html')
	
if __name__ == "__main__":
	app.run(debug=True, port=8000)

