from pydoc import render_doc
from flask import Flask, render_template,redirect, request,url_for,request
from flask_mysqldb import MySQL
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        userDetails=request.form
        email=userDetails['name']
        password=userDetails['password']
    return render_template("login.html")
@app.route('/register')
def new_user():
    return render_template("register.html")
if __name__=='__main__':
    app.run(debug=True)