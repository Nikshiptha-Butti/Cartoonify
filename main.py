from pydoc import render_doc
from flask import Flask, render_template,redirect, request,url_for,flash,session
from flask_mysqldb import MySQL
import mysql.connector
import notifypy
import cv2
import torch
from torch import optim
from torchvision import models
from torchvision import transforms as T
import IPython.display as display
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import PIL.Image
import time
import functools
import scipy.io
import scipy.misc
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from PIL import Image
from PIL import Image,ImageFilter
import numpy as np
from sklearn import neural_network
import tensorflow as tf
notification=notifypy.Notify()
import yaml
import os
mpl.rcParams['figure.figsize'] = (12,12)
mpl.rcParams['axes.grid'] = False
import PIL.Image
from werkzeug.utils import secure_filename
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.utils import save_image
id=0
app=Flask(__name__)
app.secret_key="NHN"
UPLOAD_FOLDER='static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#Configure the database
@app.route('/login')
def login(methods=['POST']):   
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/select')
def select():
    return render_template("select.html")

@app.route('/')
def home():
    return render_template('home.html')

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

@app.route('/uploadpic',methods=['POST'])
def uploadpic():
    return render_template("edit.html")

@app.route('/capturepic',methods=['POST'])
def capturepic():
    return render_template("video.html")
@app.route('/apply',methods=['POST'])
def apply():
    cam_port=0
    print('me')
    cam=cv2.VideoCapture(cam_port)
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
    res="select id from users where email='{}'".format(email)
    cur.execute(res)
    idc=cur.fetchall()
    for i in idc:
        for j in i:
            print(j)
            print(flname)
            res="insert into imagestore(imgid,img,userid) values(default,'{}','{}')".format(flname,j)
            cur.execute(res)
            con.commit()
    cur.close()
    if(grey_scale is not None):
        imgread=cv2.imread(flname)
        gray=cv2.cvtColor(imgread,cv2.COLOR_BGR2GRAY)
        graynew=Image.fromarray(gray)
        graynew.save('static/uploads/newgrayv.jpeg')
        """send[count]="static/uploads/newgrayv.jpeg" """
        count=count+1
    if(mean_blur is not None):
        imgread=Image.open(flname)
        blurimg=imgread.filter(ImageFilter.BLUR)
        blurimg.save('static/uploads/blurnewv.jpeg')
        """send[count]="static/uploads/blurnewv.jpeg" """
        count=count+1
    if(guassian_blur is not None):
        imgread=Image.open(flname)
        guassianimg=imgread.filter(ImageFilter.GaussianBlur(5))
        guassianimg.save('static/uploads/guassianv.jpeg')
        """send[count]="static/uploads/guassianv.jpeg" """
        count=count+1
    if(median_blur is not None):
        read=cv2.imread(flname)
        medianblur=cv2.medianBlur(read,5)
        medianblur=Image.fromarray(medianblur)
        medianblur.save('static/uploads/medianblurv.jpeg')
        """send[count]="static/uploads/medianblurv.jpeg" """
        count=count+1
    if(bilateral_filter is not None):
        read=cv2.imread(flname)
        b_filter=cv2.bilateralFilter(read,d=7,sigmaColor=200,sigmaSpace=200)
        b_filter=Image.fromarray(b_filter)
        b_filter.save('static/uploads/bfilterv.jpeg')
        """send[count]="static/uploads/bfilterv.jpeg" """
        count=count+1
    if(color_palatte is not None):
        read=cv2.imread(flname)
        # Defining input data for clustering
        data = np.float32(read).reshape((-1, 3))
        # Defining criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        # Applying cv2.kmeans function
        ret, label, center = cv2.kmeans(data,10, None, criteria,10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(read.shape)
        img=Image.fromarray(result)
        img.save('static/uploads/colorpalattev.jpeg')
        """send[count]="static/uploads/colorpalattev.jpeg" """
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
    neural_style=request.form.get('Neural_style')
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
    print(email)
    res="select id from users where email='{}'".format(email)
    cur.execute(res)
    idc=cur.fetchall()
    for i in idc:
        for j in i:
            print(j)
            print(flname)
            res="insert into imagestore(imgid,img,userid) values(default,'{}','{}')".format(flname,j)
            cur.execute(res)
            con.commit()
    cur.close()
    if(grey_scale is not None):
        imgread=cv2.imread(flname)
        gray=cv2.cvtColor(imgread,cv2.COLOR_BGR2GRAY)
        graynew=Image.fromarray(gray)
        graynew.save('static/uploads/newgray.jpeg')
        """sendp[count]="static/uploads/guassian.jpeg" """
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
        ret, label, center = cv2.kmeans(data,15, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(read.shape)
        img=Image.fromarray(result)
        img.save('static/uploads/colorpalatte.jpeg')
        count=count+1
    return render_template("edit.html")

@app.route('/neural',methods=['POST'])
def neural():
    return render_template("neural.html")
    
@app.route('/newneural',methods=['POST'])
def newneural():
    global email
    flname=UPLOAD_FOLDER+'newvimg.jpeg'
    
    model=models.vgg19(pretrained=True).features
    print(model)
    class VGG(nn.Module):
        def __init__(self):
            super(VGG,self).__init__()
            self.chosen_features=['0','5','10','19','28']
            self.model=models.vgg19(pretrained=True).features[:29]
        def forward(self,x):
            features=[]
            for layer_num,layer in enumerate(self.model):
                x=layer(x)
                if str(layer_num) in self.chosen_features:
                    features.append(x)
            return features
    device=torch.device("cpu")
    def load_image(image_name):
        image=Image.open(image_name)
        image=loader(image).unsqueeze(0)
        return image.to(device)
    
    image_size=356
    loader=transforms.Compose(
        [
            transforms.Resize((image_size,image_size)),
            transforms.ToTensor(),
            #transforms.Normalize(mean=[],std=[])
        ]
    )
    original_img=load_image(flname)
    style_img=load_image("static/style/img1.jpg")
    print(style_img)
    con=mysql.connector.connect(host='localhost',user='root',password='')
    cur=con.cursor()
    cur.execute("use cartoonify;")
    res="select id from users where email='{}'".format(email)
    cur.execute(res)
    idc=cur.fetchall()
    for i in idc:
        for j in i:
            print(j)
            print(flname)
            res="insert into neuralstore(imgid,img1,img2,userid) values(default,'{}','{}')".format(original_img,style_img,j)
            cur.execute(res)
            con.commit()
    cur.close()
    #generated=torch.randn(original_img.shape,device=device,requires_grad=True)
    model=VGG().to(device).eval()
    generated=original_img.clone().requires_grad_(True)
    #Hyperparameteres
    total_steps=6000
    learning_rate=0.001
    alpha=1
    beta=0.01
    optimizer=optim.Adam([generated],lr=learning_rate)
    for step in range(total_steps):
        generated_features=model(generated)
        original_img_features=model(original_img)
        style_features=model(style_img)
        style_loss = original_loss=0
        for gen_feature,orig_feature,style_feature in zip(
            generated_features,original_img_features,style_features
        ):
            batch_size,channel,height,width=gen_feature.shape
            original_loss+=torch.mean((gen_feature - orig_feature)**2)

            #compute Gram Matrix
            G=  gen_feature.view(channel,height*width).mm(
                gen_feature.view(channel,height*width).t()
            )
            A=  style_feature.view(channel,height*width).mm(
                style_feature.view(channel,height*width).t()
            )
            style_loss+= torch.mean((G-A)**2)
        total_loss = alpha*original_loss +beta*style_loss
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        print("you")
        if step % 10 == 0:
            print(total_loss)
            print("me")
            save_image(generated,"static/images/generated.jpeg")
            #img=Image.fromarray(generated)
            #img.save('static/style/results.jpeg')
    return render_template("newneural.html")



       
  
if __name__=='__main__':
    app.run(debug=True)