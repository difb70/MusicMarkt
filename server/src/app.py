from flask import Flask
from flask import render_template, redirect, url_for, request, session
import sys
from functools import wraps
from random import randint
import database_api as db

app = Flask(__name__)
# secret key for sessions to work
app.secret_key = "secret_key"

#################################################################################
#
#                               Wrappers
#
#################################################################################
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check if there was a session created for this user
        if "cid" not in session and not session["code"]:
            return redirect(url_for('login'))
        else:
            return func(*args, **kwargs)
    return wrapper

def create_session(cid, username):
    session["cid"] = cid
    session["username"] = username
    session["code"] = False

@login_required
def get_session_cid():
    return session["cid"]

#################################################################################
#
#                               Initial Page
#
#################################################################################
@app.route('/')
def initialPage():
    try:
        return render_template("initialPage.html")
    except Exception as e:
        return render_template("error.html", error_message = e)  # Renders a page with the error.


#################################################################################
#
#                               Register Page
#
#################################################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':

        #(TODO) verify if that email or that username is already registered in the database'
        #(TODO) else, redirect him to 'menu'
        username = request.form['username']
        password = request.form['password']
        try:
            db.create_user(username, password)
            return redirect(url_for('products'))
        except:
            error = "User already exists"

    return render_template('register.html', error=error)


#################################################################################
#
#                               Login Page
#
#################################################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        #(TODO) if user is not registered in database, return 'Invalid Credentials. Please try again.'
        #(TODO) else, redirect him to 'menu'
        username = request.form['username']
        password = request.form['password']

        # check if the credentials where correct
        if (db.check_password(username, password)):
            # TODO : created session here but, the session must only
            # be set after the 2fa code verified
            cid = db.get_cid(username)
            create_session(cid, username)

            db.generate_code(username)
            return redirect(url_for('code'))
            #return redirect(url_for('products'))
        else :
            error = "Incorrect credentials"

    return render_template('login.html', error=error)

@app.route('/code', methods=['GET', 'POST'])
def code():
    error = None
    if request.method == 'POST':
        code = request.form['code']
        print(code)

        #TODO in here we should pass the name of the client associated to the session
        #name = 'difb70' # for debug
        
        status = db.check_code(session["username"], code)
        print("status: " + str(status))

        if (status == 1): # Code checks
            session["code"] = True
            return redirect(url_for('products'))
        elif (status == 0): # Code doesn't check but has more attempts
            error = "Wrong code"
        elif (status == -1): # Is banned
            error = "You are banned for 5 min"

    return render_template('code.html', error=error)
    


#################################################################################
#
#                               Menu Page
#
#################################################################################
@app.route('/products/')
@login_required
def products():
    message = None
    try:
        pid = request.args.get("pid")
        # a product was bought
        if pid:
            cid = get_session_cid()
            db.buy_item(cid, pid)
            message = "Product bought with success!"

        products = db.get_products()
        return render_template("products.html", products=products, message=message)
    except Exception as e:
        return render_template("error.html", error_message = e)  # Renders a page with the error

@app.route('/artists')
@login_required
def artists():
    try:
        artists = db.get_artists()
        return render_template("artists.html", artists=artists)
    except Exception as e:
        return render_template("error.html", error_message = e)  # Renders a page with the error.

@app.route('/artists/scoreboard/')
@login_required
def menu():
    try:
        aid = request.args.get("aid")
        artist = db.get_artist_name(aid)
        scoreboard = db.get_scoreboard(aid)

        return render_template("scoreboard.html", scoreboard=scoreboard, artist=artist)
    except Exception as e:
        return render_template("error.html", error_message = e)  # Renders a page with the error.


if __name__ == '__main__':
    # create database connection
    db.connect()
    # TODO for the Diogo pc to run, the code below should be replaced by app.run(ssl_context=('adhoc'))
    app.run(ssl_context=('../keys/api_keys/api_server.cert.pem', '../keys/api_keys/api_server.key.pem'), host='0.0.0.0')
    db.close()
