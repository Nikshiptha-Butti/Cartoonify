from pydoc import render_doc
from flask import Flask, render_template,redirect, request,url_for,request,flash
from flask_mysqldb import MySQL
import mysql.connector
import yaml
app=Flask(__name__)
#Configure the database
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
@app.route('/loginvalidation',methods=['POST'])
def loginvalidation():
    email=request.form.get('email')
    password=request.form.get('password')
    con=mysql.connector.connect(host='localhost',user='root',password='')
    cur=con.cursor()
    cur.execute("use cartoonify;")
    res="select * from users where email=email and password=password;"
    cur.execute(res)
    count=cur.fetchall()
    cur.close()
    if len(count)>0:
        return render_template("edit.html")
    else:
        return render_template("register.html")
    


@app.route('/newuser',methods=['POST'])
def new_user():
    profpic=request.form.get('profpic')
    name=request.form.get('uname')
    print(name)
    email=request.form.get('email')
    password=request.form.get('pass')
    con_passsword=request.form.get('confirmpass')
    gender=request.form.get('gender')
    phno=request.form.get('phno')
    con=mysql.connector.connect(host='localhost',user='root',password='')
    cur=con.cursor()
    cur.execute("use cartoonify;")
    res="select * from users where email=email and password=password;"
    cur.execute(res)
    count=cur.fetchall()
    if len(count)>0:
        flash('User already exists.Register again!')
        cur.close()
        return render_template("register.html")
    else:
        res="insert into users(id,name,email,password,gender,phno,profpic) values(default,'{}','{}','{}','{}','{}','{}')".format(name,email,password,gender,phno,profpic)
        cur.execute(res)
        con.commit()
        cur.close()
        """flash('User added successfully')"""
        return render_template("login.html")
if __name__=='__main__':
    app.run(debug=True)