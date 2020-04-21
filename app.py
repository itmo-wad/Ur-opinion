from flask import Flask, render_template,request
import re
from routes import *

app = Flask(__name__)


#for testing
@app.route('/')
@app.route('/index')
def index():
    return log_r()
    
#login page
@app.route('/login')
def log():
    return log_r()

#register pasge
@app.route('/register')
def reg():
    return reg_r()
    

#error page    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
      

   
if __name__ == '__main__':

    app.run( port='5000',threaded=True)
