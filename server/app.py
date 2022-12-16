from flask import Flask
from flask import render_template, redirect, url_for, request
import databaseAPI

app = Flask(__name__)

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

        if request.form['email'] != 'admin@gmail.com' or request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        
        else:
            print("email: ", request.form['email'])
            print("username: ", request.form['username'])
            print("password: ", request.form['password'])
            
            return redirect(url_for('menu'))\

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

        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        
        else:
            
            print("username: ", request.form['username'])
            print("password: ", request.form['password'])
            
            return redirect(url_for('menu'))\

    return render_template('login.html', error=error)


#################################################################################
#
#                               Menu Page
#
#################################################################################
@app.route('/menu')
def menu():
    try:
        return render_template("menu.html")
    except Exception as e:
        return render_template("error.html", error_message = e)  # Renders a page with the error.

if __name__ == '__main__':
	app.run(ssl_context=('keys/cert.pem', 'keys/key.pem'))
