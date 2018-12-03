from util import db_updater as update
from flask import Flask,render_template,request,session,url_for,redirect,flash
from os import urandom
import urllib
import json
import random
import ssl

import sqlite3 #imports sqlite
'''
DB_FILE="data/AllDogsGoToHeaven.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations
'''

app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/")
def home():
    if 'username' in session: #if user is logged in
        username = session['username']
        return render_template('home.html', Name = username)
    else:
        return render_template('auth.html')

@app.route("/logout")
def logout():
    session.pop('username')
    return redirect(url_for('home'))

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

@app.route('/points', methods = ['GET','POST'])
def startPage():
    return render_template('points.html')

@app.route('/question')
def startGame():
    value = list(dict(request.args).keys())[0]
    url = "http://jservice.io/api/clues?value=" + value
    readUrl = urllib.request.urlopen(url)
    data = json.loads(readUrl.read())
    randI =  random.randint(0,len(data) - 1)
    question = data[randI]['question'].split(' ')
    for each in question:
        if each == '&':
            question[question.index('&')] = 'and'
    question = ' '.join(question)
    answer = "_".join(data[randI]['answer'].strip('<i>').strip('</i>').split(" "))
    category = data[randI]['category']['title']
    uCategory = '_'.join(category.split(' '))
    return render_template('question.html', question = question, category = category, answer = answer,
                            link = '/check?question=' + '_'.join(question.split(' ')),
                            uCategory = uCategory)

timesWrong = 0
@app.route('/check', methods = ['GET','POST'])
def checkAnswer():
    global timesWrong
    username = session['username']
    question = ' '.join(request.args['question'].split('_'))
    useranswer = request.form['useranswer']
    answer = request.form['answer']
    category = ' '.join(request.form['uCategory'].split('_'))
    context = ssl._create_unverified_context()
    urlData="https://www.googleapis.com/customsearch/v1?key="
    key="AIzaSyDLFqAoBs-xQCm9XPVAlTsTa0jG8ewM57k"
    query = answer
    temp = "&cx=009364855531151632334:atzshazndou&q=" + query
    urlData2=temp
    webURL=urllib.request.urlopen(urlData+key+urlData2,context=context)
    data=webURL.read()
    data=json.loads(data)
    print(data)
    title= data['items'][0]['title']
    link = data['items'][0]['link']
    print(useranswer.strip(' ').lower())
    print(answer.strip(' ').lower())
    if useranswer.strip(' ').lower() == ' '.join(answer.strip(' ').lower().split('_')):
        timesWrong = 0
        update.addScore(username,100) #placeholder for now
        return render_template('correct.html', link = link, title = title)
    else:
        timesWrong += 1
        if timesWrong == 3:
            timesWrong = 0
            update.subScore(username,100) #placeholder for now
            return render_template('results.html', answer = ' '.join(answer.split('_')),
                                    useranswer = useranswer, title = title, link = link)
        else:
            return render_template('question.html', question = question,
                                    answer = answer, category = category,
                                    link = '/check?question=' + request.args['question'],
                                    wrong = 'Incorrect, Tries Left:' + str(3 - timesWrong),
                                    uCategory = request.form['uCategory'])

@app.route('/search')
def search_results():
    return


if __name__ == '__main__':
    app.debug = True
    app.run()
