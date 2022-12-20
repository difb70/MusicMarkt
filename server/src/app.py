from flask import Flask
from flask import render_template, redirect, url_for, request
import database_api as db

app = Flask(__name__)
PRODUCT_PATH = "product/"

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
            return redirect(url_for('menu'))
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
            return redirect(url_for('menu'))
        else :
            error = "Incorrect credentials"

    return render_template('login.html', error=error)


#################################################################################
#
#                               Menu Page
#
#################################################################################
@app.route('/menu')
def menu():
    try:
        products = db.get_products()
        return render_template("menu.html", products=products, product_path=PRODUCT_PATH)
    except Exception as e:
        return render_template("error.html", error_message = e)  # Renders a page with the error.

if __name__ == '__main__':
    # create database connection
    db.connect()
    app.run(ssl_context=('keys/cert.pem', 'keys/key.pem'))
    db.close()
