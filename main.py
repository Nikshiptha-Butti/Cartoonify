from pydoc import render_doc
from flask import Flask, render_template,redirect, request,url_for,request,flash
from flask_mysqldb import MySQL
import mysql.connector
import notifypy
import cv2
notification=notifypy.Notify();
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
    global email
    email=request.form.get('email')
    password=request.form.get('password')
    con=mysql.connector.connect(host='localhost',user='root',password='')
    cur=con.cursor()
    cur.execute("use cartoonify;")
    res="select * from users where email='{}' and password='{}'".format(email,password)
    cur.execute(res)
    count=cur.fetchall()
    cur.close()
    if len(count)>0:
        notification.title="Cartoonify"
        notification.message="Login successful!"
        notification.icon="./static/images/logo.jpg"
        notification.send()
        return render_template("edit.html")
    else:
        notification.title="Cartoonify"
        notification.message="No such user found. Register Now!"
        notification.icon="./static/images/logo.jpg"
        notification.send()
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
    res="select * from users where email='{}' and password='{}'".format(email,password)
    cur.execute(res)
    count=cur.fetchall()
    if len(count)>0:
        notification.title="Cartoonify"
        notification.message="User already exists. Register again!"
        notification.icon="./static/images/logo.jpg"
        notification.send()
        cur.close()
        return render_template("register.html")
    else:
        res="insert into users(id,name,email,password,gender,phno,profpic) values(default,'{}','{}','{}','{}','{}','{}')".format(name,email,password,gender,phno,profpic)
        cur.execute(res)
        con.commit()
        cur.close()
        notification.title="Cartoonify"
        notification.message="Registration successful!"
        notification.icon="./static/images/logo.jpg"
        notification.send()
        return render_template("login.html")

@app.route('/edit',methods=['POST'])
def edit_photos():
    return render_template("edit.html")
    """count=0
    grey_scale=request.form.get('grey_scale')
    mean_blur=request.form.get('mean_blur')
    median_blur=request.form.get('median_blur')
    guassian_blur=request.form.get('guassian _blur')
    neural_style=request.form.get('neural_style')
    img=request.form.get('photo')
    con=mysql.connector.connect(host='localhost',user='root',password='')
    cur=con.cursor()
    cur.execute("use cartoonify;")
    id="select id from users where email='{}'".format(email)
    photos=[]
    print(grey_scale)
    if(grey_scale is not None):
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        photos[count]=gray
        count=count+1
        print(grey_scale)"""
    
if __name__=='__main__':
    app.run(debug=True)