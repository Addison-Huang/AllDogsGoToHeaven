import sqlite3 #imports sqlite

DB_FILE="../data/AllDogsGoToHeaven.db" 
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations

def users(): #creates the users db
    command = "CREATE TABLE users(username TEXT, password TEXT, score INTEGER)"
    c.execute(command)

def questions(): #creates the questions db
    command = "CREATE TABLE questions(username TEXT, question TEXT, answer TEXT)"
    c.execute(command)

def main(): #calls all of the functions to build the databases
    try:
        users()
        questions()
    except:
        pass
    

main()
