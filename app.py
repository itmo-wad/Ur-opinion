from flask import Flask, render_template,request,redirect
import re
from routes import *

app = Flask(__name__)

#secret key for the session
app.secret_key = "super secret key"

#main page
@app.route('/')
@app.route('/index')
def index():
    
      #check if the user logged in, if not redirect to login html
    if session.get('logged_in'):
        return index_r()
          
          
    else:
        return redirect("/login", code=302)
        
    
    
#login page
@app.route('/login', methods=['GET','POST'])
def log():
    
    #for loggined users
    if session.get('logged_in'):
          return redirect("/")
    
    # otherwise
    else:
         #post method
        if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                if log_r(username,password) :
                    return redirect("/")
                
        #if get method , or wrog logging in 
        return render_template('login.html')
    


#register page
@app.route('/register', methods=['GET','POST'])
def reg():
     #for loggined users
    if session.get('logged_in'):
         return redirect("/")
    
    # otherwise
    else:
        #post method
        if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                email    = request.form.get('email')
                fullname = request.form.get('fullname')
                if reg_r(username,password,email,fullname):
                     return redirect("/login")
                 
         #if get method , or user already exists        
        return render_template('register.html')  

#logout page    
@app.route('/logout')
def logout():
     session['logged_in'] = False
     return redirect("/login")

#error page    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
      

   
if __name__ == '__main__':

    app.run( port='5000',threaded=True)
