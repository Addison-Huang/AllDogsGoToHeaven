import sqlite3 #imports sqlite

'''
highScores()
Retrieves the top 10 highest scores
Returns the top 10 in descending order
'''

def highScores():
    DB_FILE="data/AllDogsGoToHeaven.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT score, username from users"
    c.execute(command)
    scores = c.fetchall() #retrieves the scores in descending order
    scores.sort(reverse=True)
    return scores[0:5]
'''
password(username)
returns the password that matches the username if one exists
else return none
'''
def password(username):
    DB_FILE="data/AllDogsGoToHeaven.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    get_password = 'SELECT password FROM users WHERE users.username = (?)'
    c.execute(get_password,(username,))
    password = c.fetchone()
    return password

'''
username(username)
returns an empty list if username doesn't exist in the database
returns [username] if username exists
'''
def username(username):
    DB_FILE="data/AllDogsGoToHeaven.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    user_exists = 'SELECT username FROM users WHERE users.username = (?);'
    c.execute(user_exists,(username,))
    userList = c.fetchall()
    return userList

'''
score(username)
retrieves score of user
'''
def score(username):
    DB_FILE="data/AllDogsGoToHeaven.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    user_exists = 'SELECT score FROM users WHERE users.username = (?);'
    c.execute(user_exists,(username,))
    score = c.fetchone()
    return score

'''
question(username,question)
returns question if user already answered that question
None if user didn't answer
'''

def question(username,question):
    DB_FILE="data/AllDogsGoToHeaven.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    command = 'SELECT question FROM questions WHERE questions.username = (?) AND questions.question = (?);'
    c.execute(command, (username, question))
    match = c.fetchone()
    return match
    
    
    
        
        
        
        
        
