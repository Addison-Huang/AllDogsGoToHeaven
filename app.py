from flask import Flask,render_template,request,session,url_for,redirect,flash
from os import urandom
from util import db_updater as update
from util import db_search as search
from util import db_builder as builder
from passlib.hash import sha256_crypt
import ssl
import urllib
import json
import random
import difflib

import sqlite3 #imports sqlite
app = Flask(__name__)
app.secret_key = urandom(32)

#----------------------------------------------------------getKey--------------------------------------------------------
def getKey():
    try:
        with open('keys.json') as f:
            data = json.load(f)
        return data['googleapi']
        print('---------------')
        print(data['googleapi'])
        print('---------------')
    except:
        pass
#----------------------------------------------------------home--------------------------------------------------------
@app.route("/",methods=['GET','POST'])
def home():
    builder.main()
    if 'username' in session: #if user is logged in
        return redirect(url_for('authPage'))
    else:
        return render_template('auth.html')

#----------------------------------------------------------login/register/logout--------------------------------------------------------
@app.route("/logout")
def logout():
    '''
    Logs user out of session by popping them from the session. Returns user to log-in screen
    '''
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('authPage'))
    else:
        return redirect(url_for('home'))

@app.route("/auth",methods=['GET','POST'])
def authPage():
    '''
    Authenticates user signing in. Checks to see if password is correct or not;
    if correct, logs user in. If not, flashes "incorrect credentials"
    '''
    if 'username' in session:
        username = session['username']
        score = search.score(username)[0]
        scores = search.highScores()
        counter = 0
        highScores = []
        userNames = []
        while counter < len(scores):
            highScores.append(scores[counter][0])
            userNames.append(scores[counter][1])
            counter += 1
        return render_template('home.html', Name = username,Points = score, scores= highScores, names = userNames)
    else:
        try:
            username=request.form['username'] #username
            password = search.password(username) #password that matches the username
            if password == None: #if credentials are incorrect
                flash('Wrong Username or Password!')
                return redirect(url_for('home')) #redirects
            elif sha256_crypt.verify(request.form['password'], password[0]): #if password is correct, login
                session['username'] = username
                return redirect(url_for('authPage'))
            else: #else credentials are wrong
                flash('Wrong Username or Password!')
                return redirect(url_for('home'))
        except:
            return redirect(url_for('home'))

@app.route("/reg",methods=['GET','POST'])
def reg():
    '''
    Loads the template that takes information and allows user to register,
    creating a new account that they can sign into session with
    '''
    if 'username' in session:
        return redirect(url_for('authPage'))
    return render_template('reg.html')

#----------------------------------------------------------database--------------------------------------------------------
@app.route("/added",methods=['GET','POST'])
def added():
    '''
    Checks to see if username is unique,
    flashes "username taken" if it is,
    adds user and password to database if not and sends to home
    '''
    try:
        newUsername = request.form['username']
        newPassword = sha256_crypt.encrypt(request.form['password']) #encrypts password
        userList = search.username(newUsername)
        if userList == [] : #if username isn't taken
            update.adduser(newUsername,newPassword) #add to database
            return redirect(url_for('home'))
        else: #if username is taken
            flash('Username Taken')
            return redirect(url_for('reg'))
    except:
        return redirect(url_for('home'))


#----------------------------------------------------------playing the game--------------------------------------------------------
@app.route('/points', methods = ['GET','POST'])
def startPage():

    '''Lets the user choose how many points the user want their question to be worth'''
    if 'username' in session:
        username = session['username']
        score = search.score(username)[0]
        return render_template('points.html',Points = score)
    return redirect(url_for('home'))
'''Game time! Lets the user choose how many points the user want their question to be worth'''

@app.route('/question', methods = {"GET", "POST"})
def startGame():
    '''Gives the user a question based on how many points the user choose

    The question is retrieved from the jservice API
    The category of the question is also given
    The user is given a text box to write their answer in
    '''
    if 'username' in session:
        username = session['username']
        value = list(dict(request.args).keys())[0]
        url = "http://jservice.io/api/clues?value=" + value
        readUrl = urllib.request.urlopen(url)
        data = json.loads(readUrl.read())
        randI =  random.randint(0,len(data) - 1)
        quest = data[randI]['question']
        if search.question(username, quest) == None:
            #gets a question from the jservice API
            question = data[randI]['question'].split(' ')
            update.ansQuestion(username, quest)
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
                           uCategory = uCategory, points = value,Points = search.score(username)[0], wrong = 'Tries Left: 3')
        else:
            return startGame()
    else:
        return redirect(url_for('home'))


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
    if 'username' in session:
        username = session['username']
        #gets information from hidden input in the question html and also the user's answer
        points = int(float(request.form['points']))
        question = ' '.join(request.args['question'].split('_'))
        useranswer = request.form['useranswer']
        answer = request.form['answer']
        category = ' '.join(request.form['uCategory'].split('_'))
        #gets a search result from the google search API
        try:
            context = ssl._create_unverified_context()
            urlData="https://www.googleapis.com/customsearch/v1?key="
            key= getKey()
            query = answer
            temp = "&cx=009364855531151632334:atzshazndou&q=" + query
            urlData2=temp
            webURL=urllib.request.urlopen(urlData+key+urlData2,context=context)
            data=webURL.read()
            data=json.loads(data)
            title= data['items'][0]['title']
            link = data['items'][0]['link']
        except:
            title = "No content found or no API key given"
            link = "https://playmeadowlands.com/generic.aspx?id=16034"
        cWords = ['an','a','the','and','be','or','in']
        answer = answer.strip(' ').lower().split('_')
        useranswer = useranswer.strip(' ').lower().split(' ')
        #replaces numbers with their word equivalent
        nums = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five',
                '6':'six','7':'seven','8':'eight','9':'nine','10':'ten'}
        #removes special characters from the useranswer and answer
        index = 0
        for each in useranswer:
            new = ''.join(e for e in each if e.isalnum())
            if new in nums:
                new = nums[new]
            useranswer[index] = new
            index += 1
        index = 0
        for each in answer:
            new = ''.join(e for e in each if e.isalnum())
            if new in nums:
                new = nums[new]
            answer[index] = new
            index += 1
        #removes common words from the answer and useranswer
        for word in cWords:
            for ans in answer:
                if word == ans:
                    answer.remove(word)
            for uAns in useranswer:
                if word == uAns:
                    useranswer.remove(word)
        #finds similarity between the answer and useranswer
        useranswer = ' '.join(useranswer)
        answer = ' '.join(answer)
        seq = difflib.SequenceMatcher(None,a = answer, b= useranswer)
        dif = seq.ratio() * 100
        useranswer = useranswer.split(' ')
        answer = answer.split(' ')
        correct = True
        username = session['username']
        score = search.score(username)[0]
        #checks it by seeing if all the noncommon words in the user's answer are in the correct answer and if the match between the strings is lower than 85%
        for word in useranswer:
            if word not in cWords:
                if (word not in answer and dif < 70.0) or dif < 80.0:
                    correct = False
        if correct:
        #if so increase the user's score and say that the user is correct
            timesWrong = 0
            update.addScore(username,points)
            return render_template('correct.html', link = link, title = title, Points = str(int(score)+ int(points)),
            cScore = '+' + str(points) + ', ' + str(int(score)+ int(points)))
        else:
            #otherwise check how many times the user got the question wrong and act accordingly
            timesWrong += 1
            if timesWrong == 3:
                #if the user got it wrong 3 times, say that the user is incorrect and decrease the user's score
                timesWrong = 0
                update.subScore(username,points)
                return render_template('results.html', answer = ' '.join(answer),
                                   useranswer = ' '.join(useranswer), title = title, link = link, Points = str(int(score)- int(points)),
                                   cScore = '-' + str(points) + ', ' + str(int(score) - int(points)))
            else:
                #otherwise let them try again
                return render_template('question.html', question = question,
                                   answer = '_'.join(answer), category = category,
                                   link = '/check?question=' + request.args['question'],
                                   wrong = 'Incorrect, Tries Left:' + str(3 - timesWrong),
                                   uCategory = request.form['uCategory'], points = str(points),
                                   Points = score)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    app.run()
