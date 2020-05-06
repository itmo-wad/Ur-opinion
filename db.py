from flask import Flask, render_template,request,send_from_directory,session,flash
import re
import os
import pymongo
from bson import ObjectId

#connect to datatbase


#client = pymongo.MongoClient("mongodb://<dbuser>:<password>@ds141952.mlab.com:41952/heroku_kmd3257w?retryWrites=false&w=majority")
#db = client["dbname"]
client = pymongo.MongoClient(os.environ.get('MongoDb', None))
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
def getteams():
    manager  = session.get('username')
    teamslist = []
    
    obj = teams.find({"manager":manager})
    for team in obj:
        teamslist.append(team)
        
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
    obj = teammembers.find({"teamid":teamid})
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
            "teamid": str(_id)
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
        
        
#create task for a username
#status in tasks means if task finished yet or not.     
#status in taskmembers means if member has added his idea or not.            

def add_task(manager,name,desc,teamid ,datepub,eachperiod,currenteditor):
    

    _id = tasks.insert({
            "manager": manager,
            "taskname": name,
            "desc"   : desc,
            "teamid": teamid,
            "datepub":datepub,
            "eachperiod" : eachperiod,
            "status": 0,
            "currenteditor":"currenteditor"
        })
    
    #get members of a team
    memlist = getteammembers(teamid)
    
    for member in memlist:
        taskmembers.insert({
            "username":member,
            "taskid" : str(_id),
            "teamid":teamid,
            "userorder":"userorder",
            "deadline":"dealine",
            "status":0,
            "seen":"seen"
            })    
    
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
        
        #change status of task of this member to 1 (finished for him)
        taskmembers.update_one({
    '$and': [
        {'username': writer},
        {'taskid': taskid} ]}, {"$set": {"status":1}})  
    
        return True

#return tasks list for "shared with me" to a member (status not matter)
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
            taskdic={}
            ideaslist=[]
            taskdic["taskid"]=str(task["_id"])
            taskdic["taskname"]=task["taskname"]
            taskdic["manager"]=task["manager"]
            taskdic["desc"]=task["desc"]
            taskdic["datepub"]=task["datepub"]
            taskdic["eachperiod"]=task["eachperiod"]
            taskdic["status"]=task["status"]     
            taskdic["currenteditor"]=task["currenteditor"]
            
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
                ideadic["status"]=idea["status"]    
                
                #add the dic to ideas list
                ideaslist.append(ideadic)                    
            
            #add ideas list to task dic
            taskdic["ideas"]= ideaslist            
            
            
            #get the member status on this task(already added idea or not)
            obj4  = taskmembers.find_one({
      '$and': [
         {'username': member},
         {'taskid': str(task["_id"])} ]})  
            taskdic["statusmem"]=obj4.get("status")
                
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
            taskdic["desc"]=task["desc"]
            taskdic["datepub"]=task["datepub"]
            taskdic["eachperiod"]=task["eachperiod"]
            taskdic["status"]=task["status"]     
            taskdic["currenteditor"]=task["currenteditor"]
            
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
                ideadic["status"]=idea["status"]    
                
                #add the dic to ideas list
                ideaslist.append(ideadic)                    
            
            #add ideas list to task dic
            taskdic["ideas"]= ideaslist            
            
            # add task dic to tasks list
            taskslist.append(taskdic)    
   
    return taskslist    

#return tasks list for "created by me" to a owner (status not matter)
def get_tasks_in_progress(username):
    taskslist = []
 
    #get all shared tasks with status 0 (not finished yet)
    sharedtaskslist = get_tasks_shared_with_me(username)
    for task in sharedtaskslist:
        if task["status"]==0:
            taskslist.append(task)
    
    #get all created tasks with status 0 (not finished yet)
    createdtaskslist = get_tasks_created_by_me(username)
    for task in createdtaskslist:
        if task["status"]==0:
            taskslist.append(task)
   
    return taskslist    
