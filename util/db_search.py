import sqlite3 #imports sqlite

DB_FILE="../data/AllDogsGoToHeaven.db" 

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations

'''
highScores()
Retrieves the top 10 highest scores
Returns the top 10 in descending order
'''

def highScores():
    command = "SELECT scores from users"
    c.execute(command)
    scores = c.fetchall().sort(reverse=True) #retrieves the scores in descending order
    return scores[0:10]
        
        
        
        
        
