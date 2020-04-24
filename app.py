from flask import Flask, render_template,request
import re
from routes import *

app = Flask(__name__)

#secret key for the session
app.secret_key = "super secret key"

#for testing
@app.route('/')
@app.route('/index')
def index():
    return index_r()
    
#login page
@app.route('/login', methods=['GET','POST'])
def log():
   
    if request.referrer.endswith('register') :
            username = request.form.get('username')
            password = request.form.get('password')
            email    = request.form.get('email')
            fullname = request.form.get('fullname')
            
            return log_r(username,password,email,fullname)

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
