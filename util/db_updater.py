''' this file stores the updating database code'''

import sqlite3
from flask import request,session
DB_FILE = "./data/AllDogsGoToHeaven.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations


def adduser(username, password):
    command = "INSERT INTO users VALUES(" + '"' + username + '", "' + password + '"' +'0)'
    c.execute(command)

#def subScore(username,score):
#    command = "SELECT score FROM users WHERE" + 

    
    
    
    
    

    
    
    



