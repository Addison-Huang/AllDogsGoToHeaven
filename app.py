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
    url = urllib.request.urlopen("http://jservice.io/api/clues?value=100")
    data = json.loads(url.read())
    print(data)
    return render_template('categories.html')
                        

if __name__ == "__main__":
    app.debug = True
    app.run()
