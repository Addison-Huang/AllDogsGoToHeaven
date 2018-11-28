'''
Team Quack-a-moo
SoftDev1 pd6
P #00: Da Art of Storytellin'
2018-10-17
'''

''' this file stores the updating database code'''

import sqlite3
from flask import request,session
DB_FILE = "./data/quackamoo.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations


'''
create()
This function is called when a new story is created
It adds an entry in the logs and stories database
'''
def create(title, body, username, ):
    if request.form["submit"] == "create": 
        command = "INSERT INTO stories VALUES(?,?)" #adds the story to the stories db
        c.execute(command,(title,body)) #executes the insert story command
        c.execute("SELECT entryId FROM logs") #selects all of the entryids
        entryIds = c.fetchall() #stores the list of entryids as a list
        if len(entryIds) > 0:
            entryId = len(entryIds)#the next entryId in the logs
        else:
            entryId = 0
        command2 = "INSERT INTO logs VALUES(?,?,?,?)" #updates logs
        c.execute(command2, (entryId,username,title,body)) #executes the insert log entry command

'''
add()
This function is called when someone adds to a story
it adds an entry in the logs and updates the stories database
'''
def add():
    if request.form["submit"] == "add":
        title = request.form["title"] #variables for code readability
        body = request.form["body"]
        username = session["username"]
        c.execute("SELECT entryId FROM logs") #selects all of the entryids
        entryIds = c.fetchall() #stores the list of entryids as a list
        entryId = len(entryIds)#the next entryId in the logs
        command = "INSERT INTO logs VALUES(?,?,?,?)" #updates logs
        c.execute(command, (entryId,username,title,body)) #executes the insert log entry command
        c.execute("SELECT body FROM stories WHERE stories.title ='" +title + "';")
        oldBody = c.fetchall() #stores the old body
        body = oldBody + body #updates the body
        command = "UPDATE stories SET body = '" + body + "'WHERE stories.title ='" + title + "';"
        c.execute(command) #executes the update stories command
    
def adduser(username, password):
    command = "INSERT INTO users VALUES(" + '"' + username + '", "' + password + '")'
    c.execute(command)
    
    
    

    
    
    
    
    

    
    
    



