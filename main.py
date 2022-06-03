from pydoc import render_doc
from flask import Flask, render_template,redirect, request,url_for,request,flash
from flask_mysqldb import MySQL
import mysql.connector
import yaml
app=Flask(__name__)
#Configure the database
con=mysql.connector.connect(host='localhost',user='root',password='',database='cartoonify')
cur=con.cursor()
"""
app.config['MYSQL_HOST']=''
app.config['MYSQL_USER']=''
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']=''
mysql=MySQL(app)*/
"""
@app.route('/')
def login(methods=['POST']):   
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")
"""
@app.route('/')
def home():
    return render_template('home.html')
"""


@app.route('/loginvalidation',methods=['POST','GET'])
def loginvalidation():
    email=request.form.get('email')
    password=request.form.get('password')
    cur.execute("""SELECT * from 'user' where 'email' like '()' and 'password' like '()'""",format(email,password))
    count=cur.fetchall()
    if len(count)>0:
        return render_template("edit.html")
    else:
        return render_template("register.html")



@app.route('/newuser',methods=['POST'])
def new_user():
    profpic=request.form.get('profpic')
    name=request.form.get('uname')
    email=request.form.get('email')
    password=request.form.get('pass')
    con_passsword=request.form.get('confirmpass')
    gender=request.form.get('gender')
    phno=request.form.get('phno')
    cur.execute("""SELECT * from 'user' where 'email' like '()' and 'password' like '()'""",format(email,password))
    count=cur.fetchall()
    if len(count)>0:
        flash('User already exists.Regsiter again!')
        return render_template("register.html")
    else:
        cur.execute("INSERT INTO users values(DEFAULT,name,email,password,gender,phno,profpic)")
        con.commit()
        cur.close()
        flash('User added successfully')
        return render_template("login.html")
if __name__=='__main__':
    app.run(debug=True)