from flask import Flask, render_template,request
import re

def index_r():
    return "Welcome to Ur-opinion!"

#login page
def log_r():
    return render_template('login.html')

#register page
def reg_r():
    return render_template('register.html')  
