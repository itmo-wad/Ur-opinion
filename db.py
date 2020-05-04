from flask import Flask, render_template,request,send_from_directory,session,flash
import re
import os
import pymongo

#connect to datatbase


#client = pymongo.MongoClient("mongodb://<dbuser>:<password>@ds141952.mlab.com:41952/heroku_kmd3257w?retryWrites=false&w=majority")
#db = client["dbname"]
# client = pymongo.MongoClient(os.environ.get('MongoDb', None))
# db = client.get_default_database()
client = pymongo.MongoClient("mongodb://admin:P29069921@ds141952.mlab.com:41952/heroku_kmd3257w?retryWrites=false&w=majority")
db = client.get_default_database()

#get users' collection
users = db["users"]
users.create_index("username")

#get teams collection
teams = db["teams"]

#get members collection
members = db["members"]

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

#check if the passowrd is correct
def check_pass_in_db(username,password):
        user=users.find_one({"username":username})
        if user["password"] == password:
            return True
#get the teams list for a username        
def getteams():
    manager  = session.get('username')
    teamslist = []
    
    obj = teams.find({"manager":manager})
    for team in obj:
        teamslist.append(team["teamname"])
   
    return teamslist
 
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
    for member in memlist:
        members.insert({
            "username": member,
            "teamid": _id,
            "userorder" : "",
            "deadline": "",
            "status": "",
            "seen":""
        })
        
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
def add_task(manager,name,desc,team,datepub,eachperiod,status,currenteditor):
    
    teamid = getteamid(manager, team)
    
    _id = tasks.insert({
            "manager": manager,
            "taskname": name,
            "desc"   : desc,
            "teamid": teamid,
            "datepub":datepub,
            "eachperiod" : eachperiod,
            "status": "status",
            "currenteditor":"currenteditor"
        })
    return True


#craete new idea
def addidea(memidea,writer,taskid,status):
        _id = ideas.insert({
            "idea": memidea,
            "writer": writer,
            "taskid"   : taskid,
            "status": status
        })
    
        return True
    