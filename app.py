'''
Addison Huang
SoftDev1 pd6
K
'''
import urllib.request
import json

from flask import Flask, render_template

app=Flask(__name__)


@app.route("/")

@app.route('/categories')
def startGame():
    url = urllib.request.urlopen("http://jservice.io/api/random")
    data = json.loads(url.read())
    print(data)
    return render_template('categories.html', question = data[0]['question'], 
                            answer = data[0]['answer'], 
                            difficulty = data[0]['value'],
                            category = data[0]['category']['title'])
                        

if __name__ == "__main__":
    app.debug = True
    app.run()
