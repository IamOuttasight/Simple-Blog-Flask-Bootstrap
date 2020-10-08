from flask import Blueprint
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import logging
from flask import request
from passlib.hash import sha256_crypt
from functools import wraps

from forms import RegisterForm
from forms import ArticleForm
from app import mysql


blog = Blueprint('blog', __name__)


def is_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized. Please, log in', 'danger')
            return redirect(url_for('blog.login'))
    return wrapper


def is_author(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        article_id = kwargs['id']
        cur = mysql.connect.cursor()
        cur.execute("SELECT * FROM articles WHERE id=%s", [article_id])
        article = cur.fetchone()
        cur.close()
        if session['username'] == article['author']:
            return f(*args, **kwargs)
        else:
            flash('Permission denied. You are not the author of the article', 'danger')
            return redirect(url_for('blog.dashboard'))
    return wrapper


@blog.route('/')
def index():
    return render_template('home.html')


@blog.route('/about/')
def about():
    return render_template('about.html')


@blog.route('/articles/')
def articles():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        return render_template('articles.html')


@blog.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articles WHERE id=%s", [id])
    article = cur.fetchone()
    return render_template('article.html', article=article)


@blog.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        # Validate email and pass
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        for u in users:
            if email == u['email']:
                flash('This email already exists', 'danger')
                return render_template('register.html', form=form)
            elif username == u['username']:
                flash('This username already exists', 'danger')
                return render_template('register.html', form=form)      
        
        # Add new user
        cur.execute("INSERT INTO users(name, email, username, password)\
                    VALUES(%s, %s, %s, %s)", (name, email, username, password))
        mysql.connection.commit()
        cur.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('blog.login'))
    
    return render_template('register.html', form=form)


@blog.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            cur.close()

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('blog.dashboard'))
            else:
                flash('Invalid login', 'danger')
                return render_template('login.html')
        else:
            cur.close()
            flash('Username not found', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@blog.route('/logout/')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('blog.login'))


@blog.route('/dashboard/')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE author=%s", [session['username']])
    articles = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        return render_template('dashboard.html')


@blog.route('/add_article/', methods=['POST', 'GET'])
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
        return redirect(url_for('blog.dashboard'))

    return render_template('add_article.html', form=form)


@blog.route('/edit_article/<string:id>/', methods=['POST', 'GET'])
@is_logged_in
@is_author
def edit_article(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articles WHERE id=%s", [id])
    article = cur.fetchone()

    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", [title, body, id])
        mysql.connection.commit()
        cur.close()

        flash('Article edited successfully', 'success')
        return redirect(url_for('blog.dashboard'))

    return render_template('edit_article.html', form=form)


@blog.route('/delete_article/<string:id>/', methods=['POST'])
@is_logged_in
@is_author
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    
    flash('Article deleted', 'success')
    return redirect(url_for('blog.dashboard'))