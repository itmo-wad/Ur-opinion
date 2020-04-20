from flask import Flask, render_template,request
import re
from routes import *

app = Flask(__name__)


#for testing
@app.route('/')
@app.route('/index')
def index():
    return index_routes()
    
    

#error page    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
      

   
if __name__ == '__main__':

    app.run( port='5000',threaded=True)

