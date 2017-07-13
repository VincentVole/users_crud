from flask import Flask, render_template, request, redirect#, flash, session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# app.secret_key = 'sdf1j3kjf02i9efhwj'
mysql = MySQLConnector(app,'usersdb')

@app.route('/')
def index():
	return redirect('/users')
@app.route('/users')
def users():
	users = mysql.query_db("SELECT * FROM users")
	return render_template('/index.html', users=users)
@app.route('/users/new')
def add():
	return render_template('/add.html')
@app.route('/users/<id>/edit')
def edit(id):
	query = "SELECT * FROM users WHERE id = :id"
	data = {
		'id': id
	}
	user = mysql.query_db(query, data)
	user = user[0]
	return render_template('/edit.html', id=id, user=user)

@app.route('/users/<id>')
def show(id):
	query = "SELECT * FROM users WHERE id = :id"
	data = {
		'id': id
	}
	user = mysql.query_db(query, data)
	user = user[0]
	return render_template('/show.html', user=user)

@app.route('/users/create', methods=['POST'])
def create():
	query = "INSERT INTO users(first_name, last_name, email, created_at, updated_at) VALUES(:first_name, :last_name, :email, NOW(), NOW())"
	data = {
		'first_name': request.form['first_name'],
		'last_name': request.form['last_name'],
		'email': request.form['email']
	}
	user_id = mysql.query_db(query, data)
	return redirect('/users/' + str(user_id))

@app.route('/users/<id>/destroy')
def destory(id):
	query = "DELETE FROM users WHERE id = :id"
	data = {
		'id': id
	}
	mysql.query_db(query, data)
	return redirect('/users')

@app.route('/users/<id>/alter', methods=['POST'])
def alter(id):
	query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id"
	data = {
		'first_name': request.form['first_name'],
		'last_name': request.form['last_name'],
		'email': request.form['email'],
		'id': id
	}
	print 'hello'
	mysql.query_db(query, data)
	return redirect('/users/' + id)

app.run(debug=True)