from flask import Flask, render_template,request,send_from_directory,session,flash
import re
from db import *


        

def index_r():
    return render_template('index.html') 

#login page
def log_r(username,password,email,fullname):

        add_user_to_db(username, password,email,fullname)
        session['logged_in'] = True
        return index_r()
    
  #  return render_template('login.html')

#register page
def reg_r():
    return render_template('register.html')  

