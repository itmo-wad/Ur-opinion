from flask import Flask, render_template,request,send_from_directory,session,flash
import re
import os
from datetime import datetime
from datetime import timedelta  
import pymongo
from bson import ObjectId
from apscheduler.schedulers.background import BackgroundScheduler

#start the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

#connect to datatbase

# client = pymongo.MongoClient(os.environ.get('MongoDb', None))
# db = client.get_default_database()
client = pymongo.MongoClient("mongodb://admin:P29069921@ds141952.mlab.com:41952/heroku_kmd3257w?retryWrites=false&w=majority")
db = client.get_default_database()

#get users' collection
users = db["users"]
users.create_index("username")

#get teams collection
teams = db["teams"]

#get teammembers collection
teammembers = db["teammembers"]

#get taskmembers collection
taskmembers = db["taskmembers"]

#get tasks collection
tasks = db["tasks"]

#get ideas collection
ideas = db["ideas"]

#add user from register
def add_user_to_db(username, password,email,fullname):
      users.insert({
            "username": username,
            "password": password,
            "email"   : email,
            "fullname": fullname
        })
 
    
#check if username already exists    
def check_user_in_db(username):
    # user = users.find({"username":username})
    user = users.find_one({"username":username})
    if user : 
        return True
    else:
        return False


#check if the passowrd is correct
def check_pass_in_db(username,password):
        user=users.find_one({"username":username})
        if user["password"] == password:
            return True
  
      
#return full name of ausername
def get_full_name(username):
    user = users.find_one({"username":username})
    if user : 
       
        return user.get("fullname")


#get the teams list for a username        
def getteams(details):
    manager  = session.get('username')
    teamslist = []
    memberslist=[]
    
    obj = teams.find({"manager":manager})
    for team in obj:
        teamdic={}    
        members=[]
        memberdic={}
        memberslist=[]
        
        #get info for each team
        teamdic["teamid"]=str(team["_id"])
        teamdic["teamname"]=team["teamname"]
        
        #send details when click my teams
        if (details=="details"):            
            teamdic["manager"]=team["manager"]
            teamdic["desc"]=team["desc"]
            
            #get team members
            members = teammembers.find({"teamid":str(team["_id"])})
            
            for member in members:
                memberdic={}
                memberdic["username"]=member.get("username")
                memberdic["status"]=member.get("status")            
    
                memberslist.append(memberdic)
                
            teamdic["members"]=memberslist   
 
        teamslist.append(teamdic)     
               
    return teamslist


#return teamid according member usernamename
def getmemteam(member):
    teamsidlist = []
    obj = teammembers.find({"username":member})
    for team in obj:
        teamsidlist.append(team["teamid"])        
          
    return teamsidlist


#return members of a team
def getteammembers(teamid):
    memberslist = []
    obj = teammembers.find({"teamid":str(teamid)})
    for member in obj:
        memberslist.append(member["username"])        
          
    return memberslist

 
# #get team id for specific manager
def getteamid(manager , teamname):
      team = teams.find_one({
    '$and': [
        {'manager': manager},
        {'teamname': teamname} ]})      
      
      return team.get("_id")    
 

#get number of team members
def getcountteam(teamid):
    count = teammembers.count({"teamid":teamid})
    
    return count
  
       
#check if a team already exists for this username    
def check_exist_team(manager,teamname):

        team = teams.find_one({
    '$and': [
        {'manager': manager},
        {'teamname': teamname} ]})

        if team:
            return True
        else :
            return False
   
    
# create team for a username        
def add_team(manager,teamname,desc,memlist) :
    _id = teams.insert({
            "manager": manager,
            "teamname": teamname,
            "desc"   : desc            
        })
        
    #create members according the team
    #use the str to store id as string only  
    for member in memlist:
        teammembers.insert({
            "username": member,
            "teamid": str(_id),
            "status":0
        })
                
    return True


#remove team
# so remove all members and tasks related to theis team 
def remove_team(teamid) :
    
    teams.remove({"_id":ObjectId(teamid)})
    
    teammembers.remove({"teamid":teamid})
    
    taskmembers.remove({"teamid":teamid})
    
    #delete ideas of each task
    obj = tasks.find({"teamid":str(teamid)})
    
    for task in obj:
        ideas.remove({"taskid":str(task["_id"])})
        
        #remove the scheduler if exists:
        # if scheduler.get_job(str(task["_id"])) is not None:
        #     scheduler.remove_job(str(task["_id"]))
        
    tasks.remove({"teamid":teamid})   
    
    return True


def check_exist_task(manager,name):
    task = tasks.find_one({
    '$and': [
        {'manager': manager},
        {'taskname': name} ]})      

    if task:
            return True
        
    else :
            return False
       

#trigger for deadlines : move to next editor
def next_editor(taskid):    
        obj = tasks.find_one({"_id":ObjectId(taskid)})        

        #get currenteditor of the task 
        currenteditor = obj.get("currenteditor") + 1
        
        #change currenteditor of task to assign to next
        tasks.update_one({'_id': ObjectId(taskid)}, {"$set": {"currenteditor":currenteditor}})  
                       
        #check if currenteditor = count of team member.. it means that the task finished
        #get the team of the task
        teamid = obj.get("teamid")
        if (getcountteam(teamid)==currenteditor):
                tasks.update_one({'_id': ObjectId(taskid)}, {"$set": {"status":1}})
                
                #remove the scheduler
                # scheduler.remove_job(str(taskid))  
   
        #get info from current task
        datepub = obj.get("datepub")
        eachperiod = obj.get("eachperiod")
        
        #change to date type
        date_object = datetime.strptime(datepub, '%Y-%m-%d').date()
        deadline = date_object + timedelta(days=int(eachperiod))
        
        #change deadline for the next member
        #get the next member and set new deadline for him  
        taskmembers.update_one({'$and': [
       {'userorder': currenteditor},
       {'taskid': taskid} ]}, {"$set": {"deadline":str(deadline)}})
               
        return True
    
   
#create task for a username
#status in tasks means if task finished yet or not.     
#status in taskmembers not used yet.            
def add_task(manager,name,desc,teamid ,datepub,eachperiod,currenteditor):
    
   #current user on user (0)    
    _id = tasks.insert({
            "manager": manager,
            "taskname": name,
            "desc"   : desc,
            "teamid": teamid,
            "datepub":datepub,
            "eachperiod" : eachperiod,
            "status": 0,
            "currenteditor":0
        })    
  
    #get members of a team
    memlist = getteammembers(teamid)  
   
    #save the deadline for the first member
    date_object = datetime.strptime(datepub, '%Y-%m-%d').date()
    deadline = date_object + timedelta(days=int(eachperiod))    
    
    #status 0 
    for member in memlist:
        taskmembers.insert({
            "username":member,
            "taskid" : str(_id),
            "teamid":teamid,
            "userorder":memlist.index(member),
            "deadline":str(deadline),
            "status":0,
            "seen":"seen"
            })   
        deadline = deadline + timedelta(days=int(eachperiod))
    
    #run schedule to pass task to next member when finish his peroid
    # interval = eachperiod
    # scheduler.add_job(lambda: next_editor(str(_id)), 'interval', days=interval, id=str(_id))        
    
    return True


#remove task
def remove_task(taskid) :
    #delete task
    tasks.remove({"_id":ObjectId(taskid)})
       
    #delete taskmember
    taskmembers.remove({"taskid":taskid})
    
    #delete ideas
    ideas.remove({"taskid":str(taskid)})
    
    #remove the scheduler:
    # if scheduler.get_job(taskid) is not None :
    #    scheduler.remove_job(taskid)    
   
    return True


#skip current member
def skip_member(taskid):
   
         #reset deadlines
        #get eachperiod
        
        # interval= obj2.get("eachperiod")    
        # if scheduler.get_job(taskid) is not None :
        #     scheduler.remove_job(taskid)        
        # scheduler.add_job(lambda: next_editor(taskid), 'interval', days=interval, id=taskid)        
   
        #move to the next editor
        next_editor(taskid)        
  
        return True  
    
    
#craete new idea
# status means if idea accepted yet or not
def addidea(memidea,writer,taskid):
        _id = ideas.insert({
            "idea": memidea,
            "writer": writer,
            "taskid"   : taskid,
            "status": 0
        })
     
        
    #     #change status of task of this member to 0 (finished for him)
    #     #not used yet
    #     taskmembers.update_one({
    # '$and': [
    #     {'username': writer},
    #     {'taskid': taskid} ]}, {"$set": {"status":0}})  
        
        #don't change currenteditor if manager added a comment
        obj2 = tasks.find_one({"_id":ObjectId(taskid)})
        
        if (obj2.get("manager") != writer):
            
            #reset deadlines
            
            #get eachperiod
            # interval= obj2.get("eachperiod")    
            # if scheduler.get_job(taskid) is not None :
            #     scheduler.remove_job(taskid)        
            # scheduler.add_job(lambda: next_editor(taskid), 'interval', days=interval, id=taskid)        
        
            #move to the next editor
            next_editor(taskid)       

        return True


#return tasks list for "shared with me" to a member (status not matter)
#member has the right to add an idea if current user = userorder
def get_tasks_shared_with_me(member):    
    teamsidlist = getmemteam(member)
    
    taskslist = []
    taskdic={}
    
    ideaslist=[]
    ideadic={}
    
    #returns list of dictionaries eachone contains details of a task     
    #for each team get all tasks id
    for teamid in teamsidlist :
        obj = tasks.find({"teamid":teamid})       
        
        #for each task get all data
        for task in obj:
              currentuser  = taskmembers.find_one({
                   '$and': [
                      {'username': member},
                      {'taskid': str(task["_id"])} ]})  
                
                #show task in order 
            #     #still show for user saw it (<=) and hide or others
            # if (currentuser.get("userorder") <= task["currenteditor"] ):                      
                    
              taskdic={}
              ideaslist=[]              
                                  
              taskdic["taskid"]=str(task["_id"])
              taskdic["taskname"]=task["taskname"]
              taskdic["manager"]=task["manager"]
              taskdic["fullname_manager"]=get_full_name(task["manager"])
              taskdic["desc"]=task["desc"]
              taskdic["datepub"]=task["datepub"]
              taskdic["eachperiod"]=task["eachperiod"]
              taskdic["status"]=task["status"]    
                            
              #get the teamname for teamid
              teamid = task["teamid"]
              obj2 = teams.find_one({"_id":ObjectId(teamid)})
              teamname = obj2.get("teamname")
              taskdic["teamname"]=teamname              
              
              #for each task get all ideas and put in list of dictionaries
              obj3 = ideas.find({"taskid":taskdic["taskid"]})
                         
              #for each idea get all data
              for idea in obj3:
                  
                  ideadic={}
                  ideadic["idea"]=idea["idea"]
                  ideadic["writer"]=idea["writer"]
                  ideadic["fullname_writer"]=get_full_name(idea["writer"])
                  ideadic["status"]=idea["status"]    
                  
                  #add the dic to ideas list
                  ideaslist.append(ideadic)                    
              
              #add ideas list to task dic
              taskdic["ideas"]= ideaslist           
                            
        #       #get the member status on this task(already added idea or not)
        #       obj4  = taskmembers.find_one({
        # '$and': [
        #    {'username': member},
        #    {'taskid': str(task["_id"])} ]})  
        #       taskdic["statusmem"]=obj4.get("status")
              
               #get the name of the current editor
              obj4 = taskmembers.find_one({
                 '$and': [
                    {'userorder': task["currenteditor"]},
                    {'taskid': str(task["_id"])} ]})  
              
              #no obj4 if task finished
              if obj4:
                  taskdic["currenteditor"]=obj4.get("username")
                  taskdic["fullname_currenteditor"]=get_full_name(obj4.get("username"))
                  taskdic["deadline"]=obj4.get("deadline")
              
              else :
                  taskdic["currenteditor"]=""
                  taskdic["deadline"]=""
             
              
              #add statusmem depending on the userorder
              taskdic["statusmem"]=0
              if (currentuser.get("userorder") == task["currenteditor"] ):
                  taskdic["statusmem"]=1
                  
              # add task dic to tasks list
              taskslist.append(taskdic)    
   
    return taskslist
    
# values returned from previous function 
    
# tasklist=[taskdic1,taskdic2,...]   
#      taskdic1={"taskid":"taskid",
#                 "name":"",
#                 "desc":"desc",
#                 "":"",
#                 ""teamname:"teamname"
#                 "ideas":[idea1,idea2]          
#     }   
     
#    idea1={ "idea":"idea",
#            "writer":"writer"
#            "status":"status"
#            }
#find tasks for teamid and not equals to unwantedstat
# obj = tasks.find(
#     {"$and": [
#         {"teamid": teamid},
#         {"status": {
#             "$ne": 2
#             }}
#         ]}
#     )    


#return tasks list for "created by me" to a owner (status not matter)
def get_tasks_created_by_me(manager):
    taskslist = []
    taskdic={}
    
    ideaslist=[]
    ideadic={}
    
    #returns list of dictionaries eachone contains details of a task 
    obj = tasks.find({"manager":manager})       
       
    #for each task get all data
    for task in obj:
            
            taskdic={}
            ideaslist=[]
            taskdic["taskid"]=str(task["_id"])
            taskdic["taskname"]=task["taskname"]
            taskdic["manager"]=task["manager"]
            taskdic["fullname_manager"]=get_full_name(task["manager"])
            taskdic["desc"]=task["desc"]
            taskdic["datepub"]=task["datepub"]
            taskdic["eachperiod"]=task["eachperiod"]
            taskdic["status"]=task["status"]          
            
            #get the teamname for teamid
            teamid = task["teamid"]
            obj2 = teams.find_one({"_id":ObjectId(teamid)})
            teamname = obj2.get("teamname")
            taskdic["teamname"]=teamname            
            
            #for each task get all ideas and put in list of dictionaries
            obj3 = ideas.find({"taskid":taskdic["taskid"]})
                       
            #for each idea get all data
            for idea in obj3:
                
                ideadic={}
                ideadic["idea"]=idea["idea"]
                ideadic["writer"]=idea["writer"]
                ideadic["fullname_writer"]=get_full_name(idea["writer"])
                ideadic["status"]=idea["status"]    
                
                #add the dic to ideas list
                ideaslist.append(ideadic)                    
            
             #get the name of the current editor
            obj4 = taskmembers.find_one({
               '$and': [
                  {'userorder': task["currenteditor"]},
                  {'taskid': str(task["_id"])} ]})  
            
            if obj4:
                taskdic["currenteditor"]=obj4.get("username")
                taskdic["fullname_currenteditor"]=get_full_name(obj4.get("username"))
                taskdic["deadline"]=obj4.get("deadline")

            
            else :
                taskdic["currenteditor"]=""
                taskdic["deadline"]=""            
            
            #add ideas list to task dic
            taskdic["ideas"]= ideaslist            
            
            #the manager has always the right to right comments
            taskdic["statusmem"]=1
            # add task dic to tasks list
            taskslist.append(taskdic)    
   
    return taskslist    


#return tasks list for "created by me" to a owner (status not matter)
def get_tasks_in_progress(username):
    taskslist = []
    
    #get all shared tasks with status 0 (not finished yet)
    #get only tasks with edition rights(for current user)
    sharedtaskslist = get_tasks_shared_with_me(username)
    for task in sharedtaskslist:
        if (task["status"]==0 and task["statusmem"]==1  ):
            taskslist.append(task)
    
    #get all created tasks with status 0 (not finished yet)
    createdtaskslist = get_tasks_created_by_me(username)
    for task in createdtaskslist:
        if task["status"]==0:
            taskslist.append(task)
   
    return taskslist    

#get setting
def get_setting(username):
    settinglist={}
    
    obj = users.find_one({"username":username})
    
    settinglist["fullname"]=obj.get("fullname")
    settinglist["email"]=obj.get("email")

    return settinglist

#save new setting
def save_setting(password,email,fullname):  
    username = session.get("username")    
    
    if password=="" :
         users.update_one({'username': username}, {"$set": {"fullname":fullname, "email":email} })  

    else:
         users.update_one({'username': username}, {"$set": {"fullname":fullname, "email":email, "password":password} })  


    return True