from pydoc import render_doc
from flask import Flask, render_template,redirect,url_for
app=Flask(__name__)
@app.route('/')
def index():
    return render_template("login.html")
@app.route('/register')
def new_user():
    return render_template("register.html")
if __name__=='__main__':
    app.run(debug=True)