from pydoc import render_doc
from flask import Flask, render_template,redirect, request,url_for,request
from flask_mysqldb import MySQL
import mysql.connector
import yaml
app=Flask(__name__)
#Configure the database
con=mysql.connector.connect(host='localhost',user='root',password='',database='cartoonify')
cursor=con.cursor()
"""
app.config['MYSQL_HOST']=''
app.config['MYSQL_USER']=''
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']=''
mysql=MySQL(app)*/
"""
@app.route('/',methods=['GET','POST'])
def Home():   
    return render_template("login.html")
@app.route('/register')
def new_user():
    if request.method == 'POST':
        userDetails=request.form
        profpic=userDetails['profpic']
        name=userDetails['uname']
        email=userDetails['email']
        password=userDetails['pass']
        con_passsword=userDetails['confirmpass']
        gender=userDetails['gender']
        phno=userDetails['phno']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO users values(DEFAULT,name,email,password,gender,phno,profpic)")
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("register.html")
if __name__=='__main__':
    app.run(debug=True)