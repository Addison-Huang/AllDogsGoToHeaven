# AllDogsGoToHeaven - Addison Huang, Claire Liu, Damian Wasilewicz, Dennis Chen


### What is Trivia?
A web based trivia game with questions straight from the JService API, an API with jeopardy questions. Users' scores are calculated by the point value of the questions they answer correctly and incorrectly. If a user answers a question incorrectly, they will be given the opportunity to learn more about the question they answered incorrectly.

----
### How to run?
#### 1. create and open a your virtual environment
```bash
$ python3 -m venv woof
$ . woof/bin/activate
```
#### 2. clone the repository
(https)
```bash
$ git clone https://github.com/Addison-Huang/AllDogsGoToHeaven.git
```
(ssh)
```bash
$ git clone git@github.com:Addison-Huang/AllDogsGoToHeaven.git
```
#### 3. install needed pip install
``` bash
$ pip install -r AllDogsGoToHeaven/requirements.txt
```
#### 4. run the flask app
```bash
$ cd AllDogsGoToHeaven/
$ python app.py
```
#### 5. open up the flask app in a preferred browser
<http://127.0.0.1:5000/>

----
#### Why Passlib

Link to the Passlib Documentation<https://passlib.readthedocs.io/en/stable/>
Passlib encrypts a password by hashing it and can also decrypt it for later verification. We decided to use this module as we thought any website that requires authentication, should not make passwords easily available to everyone who clones the repository. Passlib is used to encrypt passwords submitted on our website. The passwords are decrypted for verification when a user logs in.

----

#### Procuring API Keys

Jservice API: no api key <br>
link to the documentation: <http://jservice.io/>

Google Custom Search API: sign up for an api key @ <https://developers.google.com/custom-search/v1/overview#api_key>
link to the documentation: <https://developers.google.com/custom-search/v1/overview>

----

#### Using API Keys
As of right now, Team AllDogsGoHeaven has their api keys stored in keys.json. The user can input their api key into keys.json so that the flask app works.
