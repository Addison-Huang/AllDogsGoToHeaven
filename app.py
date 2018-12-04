from flask import Flask,render_template,request,session,url_for,redirect,flash
from os import urandom
from util import db_updater as update
from util import db_search as search
from passlib.hash import sha256_crypt
import ssl
import urllib
import json
import random
import difflib

import sqlite3 #imports sqlite
app = Flask(__name__)
app.secret_key = urandom(32)


#----------------------------------------------------------home--------------------------------------------------------
@app.route("/")
def home():
    '''
    Home route; if user is signed into session, they will see game home screen. If not, they will be redirected to login screen
    '''
    if 'username' in session: #if user is logged in
        username = session['username']
        score = search.score(username)[0]
        return render_template('home.html', Name = username,Points = score )
    else:
        return render_template('auth.html')

#----------------------------------------------------------login/register/logout--------------------------------------------------------
@app.route("/logout")
def logout():
    '''
    Logs user out of session by popping them from the session. Returns user to log-in screen
    '''
    session.pop('username')
    return redirect(url_for('home'))

@app.route("/auth",methods=['GET','POST'])
def authPage():
    '''
    Authenticates user signing in. Checks to see if password is correct or not;
    if correct, logs user in. If not, flashes "incorrect credentials"
    '''
    username=request.form['username'] #username
    password = search.password(username) #password that matches the username
    if password == None: #if credentials are incorrect
        flash('incorrect credentials')
        return redirect(url_for('home')) #redirects
    elif sha256_crypt.verify(request.form['password'], password[0]): #if password is correct, login
        session['username'] = username
        score = search.score(username)[0]
        return render_template('home.html', Name = username, Points = score)
    else: #else credentials are wrong
        flash('incorrect credentials')
        return redirect(url_for('home'))


@app.route("/reg",methods=['GET','POST'])
def reg():
    '''
    Loads the template that takes information and allows user to register,
    creating a new account that they can sign into session with
    '''
    return render_template('reg.html')

#----------------------------------------------------------database--------------------------------------------------------
@app.route("/added",methods=['GET','POST'])
def added():
    '''
    Checks to see if username is unique,
    flashes "username taken" if it is,
    adds user and password to database if not and sends to home
    '''
    newUsername = request.form['username']
    newPassword = sha256_crypt.encrypt(request.form['password']) #encrypts password
    userList = search.username(newUsername)
    if userList == [] : #if username isn't taken
        update.adduser(newUsername,newPassword) #add to database
        return redirect(url_for('home'))
    else: #if username is taken
        flash('Username Taken')
        return redirect(url_for('reg'))


#----------------------------------------------------------playing the game--------------------------------------------------------
@app.route('/points', methods = ['GET','POST'])
def startPage():

    '''Lets the user choose how many points the user want their question to be worth'''
    username = session['username']
    score = search.score(username)[0]
    return render_template('points.html',Points = score)
    '''Game time! Lets the user choose how many points the user want their question to be worth'''
    return render_template('points.html')


@app.route('/question')
def startGame():
    '''Gives the user a question based on how many points the user choose

    The question is retrieved from the jservice API
    The category of the question is also given
    The user is given a text box to write their answer in
    '''
    #gets a question from the jservice API
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
    #gets the correct answer from the jservice api and strips is of italics
    answer = "_".join(data[randI]['answer'].strip('<i>').strip('</i>').split(" "))
    #gets the category of the question
    category = data[randI]['category']['title']
    uCategory = '_'.join(category.split(' '))
    return render_template('question.html', question = question, category = category, answer = answer,
                            link = '/check?question=' + '_'.join(question.split(' ')),
                            uCategory = uCategory, points = value)

timesWrong = 0
@app.route('/check', methods = ['GET','POST'])
def checkAnswer():
    '''Checks if the user's answer is correct and shows the corresponding page

    If the user's answer is correct, the user are redirected to a page saying the user're correct
    If the user's answer is incorrect, the user are given another try, up to 3 tries total
    On the 3rd try, if the user gets the question wrong, the user are redirected to a page
    saying that the user are incorrect and shows them the correct answer.
    For both pages, the user is given a google result that would give them more information;
    this is done using a google search API.
    If the user gets the question correct, the user are given the question's point value, but
    if the user gets the question incorrect 3 times, their score is decreased by the question's
    point value
    '''
    global timesWrong
    username = session['username']
    #gets information from hidden input in the question html and also the user's answer
    points = int(float(request.form['points']))
    question = ' '.join(request.args['question'].split('_'))
    useranswer = request.form['useranswer']
    answer = request.form['answer']
    category = ' '.join(request.form['uCategory'].split('_'))
    #gets a search result from the google search API
    context = ssl._create_unverified_context()
    urlData="https://www.googleapis.com/customsearch/v1?key="
    key="AIzaSyDLFqAoBs-xQCm9XPVAlTsTa0jG8ewM57k"
    query = answer
    temp = "&cx=009364855531151632334:atzshazndou&q=" + query
    urlData2=temp
    webURL=urllib.request.urlopen(urlData+key+urlData2,context=context)
    data=webURL.read()
    data=json.loads(data)
    title= data['items'][0]['title']
    link = data['items'][0]['link']
    #checks if the answer is correct or similar enough to the correct answer
    cWords = ['an','a','the','and']
    answer = answer.strip(' ').lower().split('_')
    useranswer = useranswer.strip(' ').lower().split(' ')
    print(answer)
    print(useranswer)
    for word in cWords:
        for ans in answer:
            if word == ans:
                answer.remove(word)
        for uAns in useranswer:
            if word == uAns:
                useranswer.remove(word)
    useranswer = ' '.join(useranswer)
    answer = ' '.join(answer)
    seq = difflib.SequenceMatcher(None,a = answer, b= useranswer)
    dif = seq.ratio() * 100
    useranswer = useranswer.split(' ')
    answer = answer.split(' ')
    correct = True
    #checks it by seeing if all the noncommon words in the user's answer are in the correct answer and if the match between the strings is lower than 85%
    for word in useranswer:
        if word not in cWords:
            if (word not in answer and dif < 95.0) or dif < 85.0:
                correct = False
    if correct:
        #if so increase the user's score and say that the user is correct
        timesWrong = 0
        update.addScore(username,points)
        return render_template('correct.html', link = link, title = title)
    else:
        #otherwise check how many times the user got the question wrong and act accordingly
        timesWrong += 1
        if timesWrong == 3:
            #if the user got it wrong 3 times, say that the user is incorrect and decrease the user's score
            timesWrong = 0
            update.subScore(username,points)
            return render_template('results.html', answer = ' '.join(answer),
                                    useranswer = ' '.join(useranswer), title = title, link = link)
        else:
            #otherwise let them try again
            return render_template('question.html', question = question,
                                    answer = '_'.join(answer), category = category,
                                    link = '/check?question=' + request.args['question'],
                                    wrong = 'Incorrect, Tries Left:' + str(3 - timesWrong),
                                    uCategory = request.form['uCategory'], points = str(points))


if __name__ == '__main__':
    app.debug = True
    app.run()
