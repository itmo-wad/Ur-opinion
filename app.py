from flask import Flask, render_template,request,redirect
import re
import requests
from logging.handlers import RotatingFileHandler
import logging

from routes import *

app = Flask(__name__)
app.url_map.strict_slashes = False

#secret key for the session
app.secret_key = "super secret key"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static/img", "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.before_request
def clear_trailing():
    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])
    if rp.endswith("index"):
        return redirect(rp[:-5])

#main page
@app.route('/')
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
                username = request.form.get('username').strip()
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
                username = request.form.get('username').strip()
                password = request.form.get('password')
                email    = request.form.get('email').strip()
                fullname = request.form.get('fullname').strip()
                if reg_r(username,password,email,fullname):
                     return redirect("/login")
                 
         #if get method , or user already exists        
        return render_template('register.html')  


#new team div    
@app.route('/teams')
def teams():
      # use the host of the server
         # if (request.remote_addr != "127.0.0.1") :
         #     return render_template('error.html'), 404
         # return render_template('teams.html')  
    
    #for testing on heroku
    if (request.referrer != "https://ur-opinion.herokuapp.com/") :
      return render_template('error.html'), 404    
    return render_template('teams.html')
 
 
#route to add new teams 
@app.route('/addteam',methods=['POST'])    
def addteam():
     #for loggined users
    if session.get('logged_in'):
          name = request.form.get('teamname').strip()
          desc = request.form.get('teamdesc').strip()
          members = request.form.get('mem_list').strip()
          
          addteam_r(name , desc , members)
          session["msg"]="loadteams"
          return redirect("/")
       
    else:
        return redirect("/login", code=302)   
       
    
#new task div    
@app.route('/newtask')
def newtask():
      # use the host of the server
         if (request.remote_addr != "127.0.0.1") :
             return render_template('error.html'), 404
         return render_template('newtask.html')  
    
    #for testing on heroku
    #if (request.referrer != "https://ur-opinion.herokuapp.com/") :
     # return render_template('error.html'), 404    
   # return render_template('teams.html')    
 
    
#logout page    
@app.route('/logout')
def logout():
     session['logged_in'] = False
     return redirect("/login")

#error page    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

 
@app.errorhandler(500)
def internal_error(e):
    requests.post("https://notify.bot.codex.so/u/1L9N0D7I", {"message": f"*Exception* on the server: '{str(e)}'" , "parse_mode":"Markdown"})
    #Team 3
    #requests.post("https://notify.bot.codex.so/u/8B2LDPRZ", {"message": f"*Exception* on the server: '{str(e)}'" , "parse_mode":"Markdown"})
    return str(e), 500
    
# logging     
handler = logging.handlers.RotatingFileHandler('logs/app.log',maxBytes=32 , backupCount=2)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s [in %(pathname)s:%(lineno)d]: %(message)s'))

app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
app.logger.info('This message goes to stderr and app.log')   


if __name__ == '__main__':

    app.run(host='0.0.0.0', port='5000',threaded=True)
