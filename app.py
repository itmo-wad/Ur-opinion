from routes import *
from flask import Flask, render_template,request,redirect
import re
import requests
from logging.handlers import RotatingFileHandler
import logging
from datetime import date

def test_local_server():
    if ( "127.0.0.1" in request.remote_addr ) :
    #if ("ur-opinion.herokuapp.com" in request.referrer ) :    
        return True
    
    else :
        return False
    
    
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
          if (test_local_server()) :
              return teams_r() 
              
          return render_template('error.html'), 404
  
            
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



#route to remove a team 
@app.route('/removeteam',methods=['POST'])    
def removeteam():
     #for loggined users
    if session.get('logged_in'):
          teamid = request.form.get('teamid').strip()
          
          removeteam_r(teamid)
          session["msg"]="loadteams"
          return redirect("/")
       
    else:
        return redirect("/login", code=302)        
    
#when pressing new task button (to get the teams)   
# @app.route('/newtask')
# def newtask():
#       # use the host of the server
#           if (test_local_server()) :
#               return  newtask_r()  
              
#           return render_template('error.html'), 404

   
@app.route('/addtask',methods=['POST'])    
def addtask():
      #for loggined users
    if session.get('logged_in'):
          name = request.form.get('taskname').strip()
          desc = request.form.get('taskdesc').strip()
          teamid = request.form.get('slc_teams').strip()
          # datepub = request.form.get('datepublish').strip()
          #get current date from server
          datepub = str(date.today())
          eachperiod = request.form.get('eachperiod').strip()
          
          addtask_r(name , desc , teamid , datepub, eachperiod)
          
          session["msg"]="loadcreatedtasks"
          return redirect("/")
       
    else:
        return redirect("/login", code=302)  
 

#route to remove a task 
@app.route('/removetask',methods=['POST'])    
def removetask():
    #for loggined users
       if session.get('logged_in'):
           taskid = request.form.get('taskid').strip()
          
           removetask_r(taskid)
           session["msg"]="loadcreatedtasks"
           return redirect("/")
       
       else:
           return redirect("/login", code=302)  

#route to skip a member 
@app.route('/skipmember',methods=['POST'])    
def skipmember():
     #for loggined users
    if session.get('logged_in'):
          taskid = request.form.get('taskid').strip()
          
          skipmember_r(taskid)
          session["msg"]="loadcreatedtasks"
          return redirect("/")
       
    else:
        return redirect("/login", code=302)     
        
#in progress   cards 
#show tasks shared and created with only status ( not finished yet)        
@app.route('/progress')
def in_progress():
           # use the host of the server
          if (test_local_server()) :
              return  in_progress_r() 
              
          return render_template('error.html'), 404
          
  
#created by me  cards
# show tasks that I have created with status 0 or 1 (finished or not)         
@app.route('/created')
def created_by_me():
           # use the host of the server
          if (test_local_server()) :
              return  created_by_me_r()
              
          return render_template('error.html'), 404
    
      
#shared with me  cards   
#show tasks shared with mewith status 0 or 1(finished or not)      
@app.route('/shared')
def shared_with_me():
           # use the host of the server
          if (test_local_server()) :
              return  shared_with_me_r()
              
          return render_template('error.html'), 404    


#create new idea from shared with me  
@app.route('/newidea', methods=['POST'])
def addidea():
    
           #for loggined users
    if session.get('logged_in'):
              memidea = request.form.get('memidea').strip()
              taskid =  request.form.get('taskid').strip()
              
              addidea_r(memidea,taskid)
              
              return redirect("/")
      
    else:
        return redirect("/login", code=302)  

      
# archive cards
@app.route('/archived')
def archived():
           # use the host of the server
          if (test_local_server()) :
              return  archived_r() 
              
          return render_template('error.html'), 404    
    

#page about
@app.route('/about')
def about():
      # use the host of the server
          if (test_local_server()) :
              return render_template('about.html')
              
          return render_template('error.html'), 404

#page setting
@app.route('/setting')
def setting():
      # use the host of the server
          if (test_local_server()) :
              return setting_r()
              
          return render_template('error.html'), 404

#page to save settings
@app.route('/savesetting', methods=['POST'])
def savesetting():
    
    if session.get('logged_in'):
              current_pass = request.form.get('current_pass')
              email    = request.form.get('email').strip()
              fullname = request.form.get('fullname').strip()
              password = ""
              if "password" in request.form:
                  password = request.form.get('password')
                  
              savesetting_r(current_pass,password,email,fullname)
              
              return redirect("/")
      
    else:
        return redirect("/login", code=302)  

      
#logout page    
@app.route('/logout')
def logout():
     session['logged_in'] = False
     return redirect("/login")

#error page    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

#method not allowed    
@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html'), 405
 
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
