from flask import Flask, render_template,request,send_from_directory,session,flash,redirect
import re
from db import *
 

def index_r():
    msg = session.get("msg")
    session["msg"]=""
    
    #get fullname
    username  = session.get('username')
    fullname = get_full_name(username)
    teamslist = getteams("nodetails")
    return render_template('index.html',msg=msg,username=username,fullname=fullname,teamslist = teamslist) 


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


#return teams list
def teams_r():    
    teamslist = getteams("details")
    
    return render_template('teams.html',teamslist = teamslist)  


#add new team
def addteam_r(teamname , desc , members):    
   #split members by spaces 
   memlist = members.splitlines()
   manager  = session.get('username')
   
   if check_exist_team(manager,teamname):
       flash('Team already exists!')
       return False
   
   #check members
   nomembers=""
   notfound = False
   for username in memlist:
       if (not check_user_in_db(username)):
           nomembers = nomembers + username +", "
           notfound = True

   if notfound :
       flash('Failed! No such usernames: ' + nomembers)
       return False
   
   if add_team(manager,teamname,desc,memlist) :
       flash('Team was added successfully!')
       return True    
   
   else:
       flash("Unable to add the new team")
       return False 


#remove team
def removeteam_r(teamid):
    
    if remove_team(teamid) :
       flash('Team was removed successfully!')
       return True    
   
    else:
       flash("Unable to remove the team")
       return False 


#add new task
def addtask_r(name , desc , teamid , datepub, eachperiod):
    manager  = session.get('username')
    
    if check_exist_task(manager,name):
        flash('Task already exists!')
        return False

    if add_task(manager,name,desc,teamid ,datepub,eachperiod,"current_editor") :
        flash('Task was added successfully!')
        return True    
    
    else:
        flash("Unable to add the new Task")
        return False 


#remove task
def removetask_r(taskid):
        if remove_task(taskid) :
            flash('Task was removed successfully!')
            return True    
   
        else:
           flash("Unable to remove the task")
           return False 
    
    
#skip current member
def skipmember_r(taskid):    
    if skip_member(taskid) :
       flash('Current member was skipped successfully!')
       return True    
   
    else:
       flash("Unable to skip current member")
       return False 
    
    
#return tasks
def getcards(taskslist):
    username = session.get("username")
    return render_template('cards.html', taskslist=taskslist,username=username)

    
#function to return data to in progress option
def in_progress_r():
    username = session.get("username")
    
    taskslist = get_tasks_in_progress(username) 
    
    return getcards(taskslist)
    

#function to return data to created by me option
def created_by_me_r():
    manager = session.get("username")
    
    taskslist = get_tasks_created_by_me(manager)   
    return getcards(taskslist)


#function to return data to shared with me option
def shared_with_me_r():
    member = session.get("username")
    
    taskslist = get_tasks_shared_with_me(member)
        
    return getcards(taskslist)
  
    
# add idea
def addidea_r(memidea,taskid):    
    if (memidea == ""):
        member = session.get("username")
        return render_template("cards.html") 
    
    else:
        writer = session.get("username")
        
        if addidea(memidea,writer,taskid):
            
           flash('New comment was added successfully!')
           return True    
    
        else:
           flash("Unable to add the new comment")
           return False 
        
    
#function to return data to setting
def setting_r():
    username = session.get("username")
    settinglist= get_setting(username)
    return render_template("setting.html",settinglist=settinglist)
             
#save settings
def savesetting_r(current_pass,password,email,fullname):
    username = session.get("username")
    if check_pass_in_db(username, current_pass):
        
        if save_setting(password,email,fullname):        
           flash('Setting saved successfully!')       
           return True    
    
        else:
           flash("Unable save new settings")
           return False  
       
    else :
           flash("Wrong Password!!")
           return False  