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
from functools import wraps

#from data import Articles


app = Flask(__name__)

# Config MySQL #NOTE: insert your MYSQL_USER and MYSQL_PASSWORD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = '...' # !!!
app.config['MYSQL_PASSWORD'] = '...' # !!!
app.config['MYSQL_DB'] = 'simple_blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)

# Temporary articles
#Articles = Articles()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        return render_template('articles.html')


@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articles WHERE id=%s", [id])
    article = cur.fetchone()
    return render_template('article.html', article=article)


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

        # Validate email and pass
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        for u in users:
            if email == u['email']:
                flash('This email already exists', 'danger')
                return render_template('register.html', form=form)
            elif username == u['username']:
                flash('This username already exists', 'danger')
                return render_template('register.html', form=form)      
        
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Get form fieds
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            cur.close()

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                #error = 'Invalid login'
                flash('Invalid login', 'danger')
                return render_template('login.html')
        else:
            cur.close()
            #error = 'Username not found'
            flash('Username not found', 'danger')
            return render_template('login.html')

    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized. Please, log in', 'danger')
            return redirect(url_for('login'))
    return wrapper


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        return render_template('dashboard.html')

class ArticleForm(Form):
    title = StringField('Title', validators=[validators.Length(min=1, max=205)])
    body = TextAreaField('Content', validators=[validators.Length(min=30)])


@app.route('/add_article', methods=['POST', 'GET'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))
        mysql.connection.commit()
        cur.close()

        flash('Article created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


if __name__ == "__main__":
    app.secret_key = 'super-secret-key'
    app.run(debug=True)