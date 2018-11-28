from util import db_updater as update
from flask import Flask,render_template,request,session,url_for,redirect,flash
from os import urandom

import sqlite3 #imports sqlite
DB_FILE="data/quackamoo.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('auth.html')

@app.route("/auth",methods=['GET','POST'])
def authPage():
    DB_FILE="data/AllDogsGoToHeaven.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    username=request.form['username']
    command = 'SELECT password FROM users WHERE users.username = "{0}"'.format(username)
    c.execute(command)
    password = c.fetchone()
    print(password[0])
    if password == []:
        flash('incorrect credentials')
        return redirect(url_for('home'))
    elif request.form['password'] == password[0]:
        session['username'] = username
        return render_template('home.html', Name = username)
    else:
        flash('incorrect credentials')
        return redirect(url_for('home'))

@app.route("/reg",methods=['GET','POST'])
def reg():
     return render_template('reg.html')

@app.route("/added",methods=['GET','POST'])
def added():
    DB_FILE="data/AllDogsGoToHeaven.db"
    newUsername = request.form['username']
    newPassword = request.form['password']
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    command = 'SELECT username FROM users;'
    c.execute(command)
    userList = c.fetchall()
    print(userList)
    if newUsername not in userList:
        insert = "INSERT INTO users VALUES(?,?,?)"
        params=(newUsername,newPassword,0)
        c.execute(insert,params)
        db.commit()
        db.close()
        #session['username'] = newUsername
        return redirect(url_for('home'))
    else:
        flash('Username Taken')
        return redirect(url_for('home'))

@app.route('/categories')
def startGame():
    url = "http://jservice.io/api/clues?value="
    url100 = urllib.request.urlopen(url + "100")
    url200 = urllib.request.urlopen(url + "200")
    url300 = urllib.request.urlopen(url + "300")
    url400 = urllib.request.urlopen(url + "400")
    url500 = urllib.request.urlopen(url + "500")
    url600 = urllib.request.urlopen(url + "600")
    url700 = urllib.request.urlopen(url + "700")
    url800 = urllib.request.urlopen(url + "800")
    url900 = urllib.request.urlopen(url + "900")
    url1000 = urllib.request.urlopen(url + "1000")
    data = json.loads(url100.read())
    data = json.loads(url100.read())
    data = json.loads(url100.read())
    data = json.loads(url100.read())
    data = json.loads(url100.read())
    data = json.loads(url100.read())
    data = json.loads(url100.read())
    data = json.loads(url100.read())
    print(data)
    return render_template('categories.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
