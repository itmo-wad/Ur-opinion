from flask import Flask, render_template,request,send_from_directory,session,flash
import re
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import get_db


#for testing
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#error page    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
