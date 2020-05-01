from flask import Flask, render_template,request,send_from_directory,session,flash,redirect
import re
from db import *
 

def index_r():
    msg = session.get("msg")
    print("dddddddddddddddddddd")
    print(msg)
    return render_template('index.html',msg=msg) 

#login page
def reg_r(username,password,email,fullname):
    
    #check if user already exsits
    if check_user_in_db(username) :
                     flash('Username aleady exists!')
                     session['logged_in'] = False
                     return False
    else:
        add_user_to_db(username, password,email,fullname)
        session['logged_in'] = False
        return True
    
  #  return render_template('login.html')

#register page
def log_r(username,password):
    if check_user_in_db(username):
            if check_pass_in_db(username, password):
                session['logged_in'] = True
                session['username'] = username
                return True
            else :
                flash('Wrong Password!')
                session['logged_in'] = False
    else:
            flash('User not exsit!!')
            session['logged_in'] = False
                    
    return False



#add new team
def addteam_r(teamname , desc , members):
    
   #split members by spaces 
   memlist = members.splitlines()
   username  = session.get('username')
   
   if check_exist_team(teamname,username):
       flash('Team already exists!')
       return False
   
   add_team(username,teamname,desc,"taskid") 
   flash('Team was added successfully!')
   return True    