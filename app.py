__author__ = "neehad"

from entities.user import User
from flask import Flask,render_template, request, session

app  = Flask(__name__) #create a flask object
app.secret_key="neehad"


#create endpoint
@app.route('/') #www.mysiste.com/api/
def hello_method():
    return render_template('login.html')

#initialize database
@app.before_first_request
def initialize_database():
    Database.initialize()

#make a new endpoint
@app.route('/login' methods=['POST']) #only do post request
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
    

    return render_template("profile.html", email = session['email'] )

if __name__ == '__main__':
    app.run(port = 5000) #so if we initialize the app, run it
