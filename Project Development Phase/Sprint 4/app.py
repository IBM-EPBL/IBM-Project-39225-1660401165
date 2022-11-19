from collections import UserDict
from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re


app =Flask(__name__)
app.secret_key='jobrecommender'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30120;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=mnt68303;PWD=bwznNCTwcvzfsh98",'','')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home_logout')
def home_logout():
    return render_template('home_logout.html')

@app.route('/login',methods =['GET','POST'])
def login():
    global userid    
    msg=''

    if request.method=='POST':
        username =request.form['username']
        password=request.form['password']
        sql="SELECT * FROM users WHERE username =? AND password=?"
        stmt =ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin']=account['USERNAME']
            session['id']=account['USERNAME']
            userid=account['USERNAME']
            session['username']=account['USERNAME']
            msg= 'logged in succesfully !!!'

            return render_template('dashboard.html',msg=msg)

        else:
            msg='incorrect'

    return render_template('login.html',msg=msg)
@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method =='POST':
          username =request.form['username']
          email=request.form['email']
          password=request.form['password']
          sql="SELECT * FROM users WHERE username =?"
          stmt=ibm_db.prepare(conn,sql)
          ibm_db.bind_param(stmt,1,username)
          ibm_db.execute(stmt)
          account=ibm_db.fetch_assoc(stmt)
          print(account)
          if account:  
            msg='Account already exist'
          elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='invalid email address !'
          elif not re.match(r'[A-Za-z0-9]+',username):
            msg='Name must contain char and number'
          else:
            insert_sql="INSERT INTO users VALUES (?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql) 
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password) 
            ibm_db.execute(prep_stmt)
            msg='you have successfully registered '
    elif request.method =='POST':
        msg="Please fill out the form"
    return render_template('register.html',msg=msg)

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/apply',methods=['GET','POST'])
def apply():
    msg=''
    if request.method =='POST':
        username =request.form['username']
        email=request.form['email']  
        qualification=request.form['qualification']
        skills =request.form['skills']
        jobs="AI"  
        sql='SELECT * FROM users WHERE username =?'
        insert_sql="INSERT INTO job VALUES (?,?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql) 
        ibm_db.bind_param(prep_stmt,1,username)
        ibm_db.bind_param(prep_stmt,2,email)
        ibm_db.bind_param(prep_stmt,3,qualification) 
        ibm_db.bind_param(prep_stmt,4,skills)
        ibm_db.bind_param(prep_stmt,5,jobs)
        ibm_db.execute(prep_stmt)
        msg='you have successfully applied for job ' 
        session['loggedin']=True
    elif request.method =='POST':
        msg="Please fill out the form"
    return render_template('apply.html',msg=msg)  

@app.route('/display')
def display():
    print(session["username"],session["id"],"hello")
    sql="SELECT * FROM job WHERE username =?"
    stmt =ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,"muthu")
    ibm_db.execute(stmt)
    account=ibm_db.fetch_assoc(stmt)
    print("accountdisplay",account)

    return render_template('display.html',account=account)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)

    return render_template('home.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port = "5000")    
    


