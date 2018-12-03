''' this file stores the updating database code'''

import sqlite3
from flask import request,session
DB_FILE = "./data/AllDogsGoToHeaven.db"

db = sqlite3.connect(DB_FILE,check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations

'''
adduser(username,password)
params:username, password
username is the username of the user
password is the password of the user
function adds the username and password to the users database
'''
def adduser(username, password):
    command = "INSERT INTO users VALUES(" + '"' + username + '", "' + password + '"' +'0)'
    c.execute(command)

'''
addScore(username,score):
params:username, score
username is the username of the user in session
score is the point value of the question added
function adds the point value of the question to the users score
'''
def addScore(username,score):
    command = "SELECT score FROM users WHERE users.username ='" + username + "';" #selects score of the user
    c.execute(command)
    oldScore = c.fetchone()
    newScore = oldScore[0] + score
    command = "UPDATE users SET score = '" + str(newScore) + "'WHERE users.username = '" + username + "';" #updates score
    c.execute(command)
    db.commit()
    db.close()

'''
subScore(username,score):
params:username, score
username is the username of the user in session
score is the point value of the question added
function subtracts the point value of the question from the users score
'''
def subScore(username, score):
    addScore(username, score * -1)

'''
ansQuestion(username, question, answer)
params:username, question, answer
username is the username of the user in session
question is the question the user answered
answer is api provided answer for the question
'''

def ansQuestion(username, question, answer):
    insert = "INSERT INTO questions VALUES(?,?,?)"
    params = (username, question,username)
    c.execute(insert, params)
    
    
    
    




    
    
    
    
    

    
    
    



