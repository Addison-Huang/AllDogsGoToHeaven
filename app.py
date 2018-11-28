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
                        

if __name__ == "__main__":
    app.debug = True
    app.run()
