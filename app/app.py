from flask import Flask
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import logging
from flask import request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from data import Articles


app = Flask(__name__)

# Config MySQL #NOTE: insert your MYSQL_USER and MYSQL_PASSWORD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = '...' # !!!
app.config['MYSQL_PASSWORD'] = '...' # !!!
app.config['MYSQL_DB'] = 'simple_blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)


Articles = Articles()


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    name = StringField('Name', validators=[validators.Length(min=1, max=50)])
    username = StringField('Username', validators=[validators.Length(min=4, max=25)])
    email = StringField('Email', validators=[validators.Length(min=6, max=50)])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm password')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        for u in users:
            if email == u['email']:
                flash('This email already exists', 'danger')
                return redirect(url_for('register'))
            elif username == u['username']:
                flash('This username already exists', 'danger')
                return redirect(url_for('register'))
                
        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password)\
                    VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit db
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.secret_key = 'super-secret-key'
    app.run(debug=True)