from pydoc import render_doc
from cv2 import VideoCapture
from flask import Flask, render_template,redirect, request,url_for,flash,session
from flask_mysqldb import MySQL
import mysql.connector
import notifypy
import cv2
from PIL import Image,ImageFilter
import numpy as np
notification=notifypy.Notify()
import yaml
import os
from werkzeug.utils import secure_filename
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
app=Flask(__name__)
app.secret_key="NHN"
UPLOAD_FOLDER='static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#Configure the database
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
email=""
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
        return render_template('select.html')
    else:
        notification.title="Cartoonify"
        notification.message="No such user found. Register Now!"
        notification.icon="./static/images/logo.jpg"
        notification.send()
        return render_template("register.html")

@app.route('/uploadpic',methods=['POST'])
def uploadpic():
    return render_template("edit.html")

@app.route('/capturepic',methods=['POST'])
def capturepic():
    print('me')
    return render_template("video.html")

@app.route('/newuser',methods=['POST'])
def new_user():
    profpic=request.form.get('profpic')
    name=request.form.get('uname')
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

@app.route('/apply',methods=['POST'])
def apply():
    cam_port=0
    print('me')
    cam=VideoCapture(cam_port)
    result, image = cam.read()
    if result:
        print('me')
        vimg=Image.fromarray(image)
        vimg.save('static/uploads/newvimg.jpeg')
    else:
        print("No image detected. Please! try again")
    return render_template("video.html")
    


@app.route('/video',methods=['POST'])
def video():
    count=0
    global email
    flname=""
    grey_scale=request.form.get('grey_scale')
    mean_blur=request.form.get('mean_blur')
    median_blur=request.form.get('median_blur')
    guassian_blur=request.form.get('guassian_blur')
    bilateral_filter=request.form.get('b_filter')
    color_palatte=request.form.get('color_palatte')
    neural_style=request.form.get('neural_style')    
    flname=UPLOAD_FOLDER+'newvimg.jpeg'
    print(flname)
    send=[]
    con=mysql.connector.connect(host='localhost',user='root',password='')
    cur=con.cursor()
    cur.execute("use cartoonify;")
    if(grey_scale is not None):
        imgread=cv2.imread(flname)
        gray=cv2.cvtColor(imgread,cv2.COLOR_BGR2GRAY)
        graynew=Image.fromarray(gray)
        graynew.save('static/uploads/newgray.jpeg')
        send[count]="static/uploads/newgray.jpeg"
        count=count+1
    if(mean_blur is not None):
        imgread=Image.open(flname)
        blurimg=imgread.filter(ImageFilter.BLUR)
        blurimg.save('static/uploads/blurnew.jpeg')
        send[count]="static/uploads/blurnew.jpeg"
        count=count+1
    if(guassian_blur is not None):
        imgread=Image.open(flname)
        guassianimg=imgread.filter(ImageFilter.GaussianBlur(5))
        guassianimg.save('static/uploads/guassian.jpeg')
        send[count]="static/uploads/guassian.jpeg"
        count=count+1
    if(median_blur is not None):
        read=cv2.imread(flname)
        medianblur=cv2.medianBlur(read,5)
        medianblur=Image.fromarray(medianblur)
        medianblur.save('static/uploads/medianblur.jpeg')
        send[count]="static/uploads/medianblur.jpeg"
        count=count+1
    if(bilateral_filter is not None):
        read=cv2.imread(flname)
        b_filter=cv2.bilateralFilter(read,d=7,sigmaColor=200,sigmaSpace=200)
        b_filter=Image.fromarray(b_filter)
        b_filter.save('static/uploads/bfilter.jpeg')
        send[count]="static/uploads/bfilter.jpeg"
        count=count+1
    if(color_palatte is not None):
        read=cv2.imread(flname)
        # Defining input data for clustering
        data = np.float32(read).reshape((-1, 3))
        # Defining criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        # Applying cv2.kmeans function
        ret, label, center = cv2.kmeans(data,3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(read.shape)
        img=Image.fromarray(result)
        img.save('static/uploads/colorpalatte.jpeg')
        send[count]="static/uploads/colorpalatte.jpeg"
        count=count+1
    return render_template("video.html",send=send,count=count)


@app.route('/edit',methods=['POST'])
def edit():
    count=0
    global email
    flname=""
    name=""
    grey_scale=request.form.get('grey_scale')
    mean_blur=request.form.get('mean_blur')
    median_blur=request.form.get('median_blur')
    guassian_blur=request.form.get('guassian_blur')
    bilateral_filter=request.form.get('b_filter')
    color_palatte=request.form.get('color_palatte')
    neural_style=request.form.get('neural_style')
    img=request.files.getlist('pic')
    print(img)
    print('me')
    if not img:
        flname=UPLOAD_FOLDER+'newvimg.jpeg'
        print(flname)
    else:
        for f in img:
            flname=secure_filename(f.filename)
            fos=os.path.join(app.config['UPLOAD_FOLDER'],flname)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],flname))
            flname=UPLOAD_FOLDER+flname
        print(flname)
    sendp=[]
    con=mysql.connector.connect(host='localhost',user='root',password='')
    cur=con.cursor()
    cur.execute("use cartoonify;")
    if(grey_scale is not None):
        imgread=cv2.imread(flname)
        gray=cv2.cvtColor(imgread,cv2.COLOR_BGR2GRAY)
        graynew=Image.fromarray(gray)
        graynew.save('static/uploads/newgray.jpeg')
        sendp[count]="static/uploads/guassian.jpeg"
        count=count+1
    if(mean_blur is not None):
        imgread=Image.open(flname)
        blurimg=imgread.filter(ImageFilter.BLUR)
        blurimg.save('static/uploads/blurnew.jpeg')
        count=count+1
    if(guassian_blur is not None):
        imgread=Image.open(flname)
        guassianimg=imgread.filter(ImageFilter.GaussianBlur(5))
        guassianimg.save('static/uploads/guassian.jpeg')
        count=count+1
    if(median_blur is not None):
        read=cv2.imread(flname)
        medianblur=cv2.medianBlur(read,5)
        medianblur=Image.fromarray(medianblur)
        medianblur.save('static/uploads/medianblur.jpeg')
        count=count+1
    if(bilateral_filter is not None):
        read=cv2.imread(flname)
        b_filter=cv2.bilateralFilter(read,d=7,sigmaColor=200,sigmaSpace=200)
        b_filter=Image.fromarray(b_filter)
        b_filter.save('static/uploads/bfilter.jpeg')
        count=count+1
    if(color_palatte is not None):
        read=cv2.imread(flname)
        # Defining input data for clustering
        data = np.float32(read).reshape((-1, 3))
        # Defining criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        # Applying cv2.kmeans function
        ret, label, center = cv2.kmeans(data,3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(read.shape)
        img=Image.fromarray(result)
        img.save('static/uploads/colorpalatte.jpeg')
        count=count+1
    return render_template("edit.html")
    
if __name__=='__main__':
    app.run(debug=True)
