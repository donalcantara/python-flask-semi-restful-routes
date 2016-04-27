from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
# the "re" module will let us perform some regular expression operations
import re
import datetime
# create a regular expression object that we can use run operations on
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector('semi-restful')

@app.route('/')
def index():
	users = mysql.fetch("SELECT * FROM users")
	for user in users:
		user['created_at'] = user['created_at'].strftime('%B %d %Y %-I:%M:%S %p')
	return render_template('index.html', users=users)

@app.route('/showuserpage/<id>')
def showuserpage(id):
	users = mysql.fetch("SELECT * FROM users WHERE id = '{}' LIMIT 1".format(id))
	for user in users:
		user['created_at'] = user['created_at'].strftime('%B %d %Y %-I:%M:%S %p')
	return render_template('show.html', users=users)

@app.route('/adduserpage')
def adduserpage():
	return render_template('/add.html')

@app.route("/edituserpage/<id>")
def edituserpage(id):
	users = mysql.fetch("SELECT * FROM users WHERE id = '{}' LIMIT 1".format(id))
	return render_template('edit.html', users=users)

@app.route('/adduser', methods=['POST'])
def adduser():
	query = "INSERT INTO users (name, email, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(request.form['name'], request.form['email'])
	print query
	mysql.run_mysql_query(query)
	return redirect('/')

@app.route('/delete/<id>')
def destroy(id):
	query = "DELETE FROM users WHERE id = '{}'".format(id)
	print query
	mysql.run_mysql_query(query)
	return redirect('/')

@app.route('/edituser/<id>', methods=['POST'])
def edituser(id):
	query = "UPDATE users SET name = '{}', email = '{}' WHERE id = '{}'".format(request.form['name'], request.form['email'],id)
	print query
	mysql.run_mysql_query(query)
	return redirect('/')

@app.route('/back')
def logout():
	return redirect('/')

app.run(debug=True)