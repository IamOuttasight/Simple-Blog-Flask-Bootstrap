from app import app
from app import mysql
from views import blog

app.register_blueprint(blog, url_prefix='/')

if __name__ == "__main__":
    app.secret_key = 'super-secret-key'
    app.run()