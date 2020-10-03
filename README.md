# Simple blog on Flask with Bootstrap

---
## Description
This is a pretty simple blog. This application will let you create an account and create/edit/delete your articles.

* Python version is 3.5.2
* Frontend framework - Bootstrap v4.5.2
* As DBMS was chosen MySQL
* As WYSIWYG text editor was taken CKEditor v4.15.0, standart

---
## Installation:
1. At first, you should install _mysql-server_ and _libmysqlclient-dev_:
```sudo apt-get install mysql-server libmysqlclient-dev
```
2. Enter mysql:
```mysql -u root -p
```
3. Create a new database 'simple_blog':
```CREATE DATABASE simple_blog;
```
4. Choose that database:
```USE simple_blog;
```
5. Create 'users' table:
```CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100) UNIQUE, username VARCHAR(50) UNIQUE, password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```
6. Create 'articles' table:
```CREATE TABLE articles(id INT(11) AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(100), body TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```
7. Clone this repository to your computer and open the folder
8. Open _config.py_ and set MYSQL_PASSWORD using your root password
9. Install _pipenv_:
```pip install pipenv
```
10. Install required packages using pipenv:
```pipenv install
```
11. Launch 'main.py':
```python3 main.py
```