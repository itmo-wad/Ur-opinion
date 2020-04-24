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
    
    
    if request.method == 'POST':
        
        #check if from reg page
        if request.referrer.endswith('register') :
                username = request.form.get('username')
                password = request.form.get('password')
                email    = request.form.get('email')
                fullname = request.form.get('fullname')
                return reg_r(username,password,email,fullname)
        
        #check if from login page
        elif request.referrer.endswith('login'):
                username = request.form.get('username')
                password = request.form.get('password')
                return log_r(username,password)
            
    #if method is Get
    else:
        return render_template('login.html')

#register pasge
@app.route('/register')
def reg():
    return render_template('register.html')  

    

#error page    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
      

   
if __name__ == '__main__':

    app.run( port='5000',threaded=True)
