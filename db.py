from flask import Flask, render_template,request,send_from_directory,session,flash
import re
import pymongo

#connect to datatbase
client = pymongo.MongoClient("mongodb+srv://admin:P%40ssword%23%2A@cluster0-rkjc0.mongodb.net/test?retryWrites=true&w=majority")
db = client["moon"]

#get users' collection
users = db["users"]
users.create_index("username")


def add_user_to_db(username, password,email,fullname):
      users.insert({
            "username": username,
            "password": password,
            "email"   : email,
            "fullname": fullname
        })
    
def check_user_in_db(username):
    # user = users.find({"username":username})
    user = users.find_one({"username":username})
    if user : 
        return True


def check_pass_in_db(username,password):
        user=users.find_one({"username":username})
        if user["password"] == password:
            return True
        

