import os
from flask import Flask

import logging
logging.basicConfig(level=logging.INFO)


app=Flask(__name__,instance_relative_config=True)
app.secret_key = 'dev'

@app.route('/hello')
def hello():
    return "Hello, World!"

from flaskr import auth
app.register_blueprint(auth.bp)

from flaskr import blog
app.register_blueprint(blog.bp)
app.add_url_rule('/',endpoint='index')

if __name__ == '__main__':
    app.run()
    