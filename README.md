# Simple blog on Flask with Bootstrap
## Description
This is a pretty simple blog. This application will let you create an account and create/edit/delete your articles.

* Python version is 3.5.2
* Frontend framework - Bootstrap v4.5.2
* As DBMS was chosen MySQL v5.7.31
* As WYSIWYG text editor was taken CKEditor v4.15.0, standart
## Installation:
1. At first, you should install _mysql-server_ and _libmysqlclient-dev_:  
```sudo apt-get install mysql-server libmysqlclient-dev```
2. Clone this repository to your computer and open the folder
3. **Open** file 'app/config.py', set required data (host, user, pass, db) and then close the file
4. Install _pipenv_:  
```pip install pipenv```
5. Install required packages using pipenv (keep staying in the root folder of the project):  
```pipenv install```
6. Execute 'app/config.py' (this will create a new database automatically):  
```python3 app/config.py```
7. Launch 'app/main.py':  
```python3 app/main.py```