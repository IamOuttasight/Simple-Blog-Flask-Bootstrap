class Configuration:
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root' # Set your MySQL login
    MYSQL_PASSWORD = 'toor' # Set your MySQL password
    MYSQL_DB = 'autocreated' # Make up a database name
    MYSQL_CURSORCLASS = 'DictCursor'
    SECRET_KEY = 'super-secret-key' # Make up a secret key


if __name__ == "__main__":
    import MySQLdb
    db = MySQLdb.connect(
        Configuration.MYSQL_HOST,
        Configuration.MYSQL_USER,
        Configuration.MYSQL_PASSWORD,
    )
    cur = db.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8 COLLATE utf8_unicode_ci;".format(Configuration.MYSQL_DB))
    cur.execute("USE {}".format(Configuration.MYSQL_DB))
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100) UNIQUE, username VARCHAR(50) UNIQUE, password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
    cur.execute("CREATE TABLE IF NOT EXISTS articles(id INT(11) AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(100), body TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

    db.commit()
    cur.close()
    db.close()