from __future__ import print_function # In python 2.7
import sys
from fileinput import filename
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = "static/uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key="test"
######################################################################################
#####################################################################################
def check_user(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('Select username,password FROM users WHERE username=? and password=?', (username, password))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False
#####################################################################################
def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
#####################################################################################
@app.route("/")
def index():
    return render_template('loginalaa.html')
#####################################################################################
@app.route('/home', methods=('GET', 'POST'))
def home_page():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('admin_home.html')
#####################################################################################
@app.route('/home_back',methods=('GET', 'POST'))
def home_nav():
    return render_template('home.html')
#####################################################################################
@app.route('/admin_home_back',methods=('GET', 'POST'))
def home_admin_back():
    return render_template('admin_home.html')
#####################################################################################
@app.route('/login',methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('home_page'))
        else:
            flash('incorrect information please try again')
     
    return redirect(url_for('index'))

#####################################################################################
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        Email = request.form['Email']
        username = request.form['username']
        password = request.form['password']
        ch = True
        if not Email :
            flash('please enter your email')
            ch = False
        elif not username:
            flash('please enter your name')
            ch = False
        elif not password:
            flash('please enter a password')
            ch = False
        elif ch :
            conn = get_db_conn()
            conn.execute('INSERT INTO users(Email,username,password) values (?,?,?)', (Email,username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('register.html')
#####################################################################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
#####################################################################################
@app.route("/hotel_admin",methods=('POST','GET'))
def hot_admin():
    connect = get_db_conn()
    r = connect.execute("select * from Hotels").fetchall()
    connect.close()
    return render_template("admin_hotel.html",rows=r)

#####################################################################################

@app.route("/hotel_user",methods=('POST','GET'))
def hot_user():
    connect = get_db_conn()
    r = connect.execute("select * from Hotels").fetchall()
    connect.close()
    return render_template("users_hotel.html",rows=r)

#####################################################################################

@app.route("/base_fun", methods= ['POST'])
def base():
     if request.method == 'POST':
         return redirect(url_for('hot_user'))
     
#####################################################################################
def get_Review(HotelID):
    conn = get_db_conn()
    Reviews = conn.execute('SELECT * FROM Reviews a INNER JOIN Hotels b ON a.HotelID=b.HotelID INNER JOIN Reviewer c ON a.ReviewerID=c.ReviewerID WHERE a.HotelID=?',(HotelID,)).fetchall()
    conn.close()
    if Reviews is None:
        abort(404)
    return Reviews

#####################################################################################
@app.route('/delete/<int:id>/',  methods=['GET', 'POST'])
def deletecomment(id):
    post = get_Review(id)
    conn = get_db_conn()
    HotelID = conn.execute('SELECT HotelID from Reviews WHERE ReviewID=?', (id,)).fetchone()[0]
    print(type(HotelID) , file=sys.stdout)
    conn.execute('DELETE FROM Reviews WHERE ReviewID=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('feedback_admin',id=HotelID))

#####################################################################################
@app.route('/deletehot/<int:id>', methods=['GET', 'POST'])
def deletehot(id):
    conn = get_db_conn()
    conn.execute('DELETE FROM Hotels WHERE HotelID=?',(id,))
    conn.commit()                    
    conn.close()
    return redirect(url_for('hot_admin'))
 
#####################################################################################

# For viewing feedback page with feedbacks of the chosen Hotels and opption of adding a new feedback
@app.route("/feedback/<int:id>" , methods=['GET', 'POST'])
def feedback(id): 
    posts = get_Review(id)
    if request.method == 'POST':
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Review = request.form['Review']

        if not FirstName:
            flash('Please enter your first name')
        elif not LastName:
            flash('Please enter your last name')
        else:
            conn = get_db_conn()
            conn.execute('INSERT INTO Reviewer (FirstName, LastName, HotelID) VALUES (?, ?, ?)',
                         (FirstName, LastName, id))
            conn.commit()
            ReviewerID = conn.execute('SELECT ReviewerID from Reviewer order by ReviewerID DESC limit 1').fetchone()[0]
            conn.execute(f"INSERT INTO Reviews (ReviewerID, HotelID, Review) VALUES('{ReviewerID}', '{id}' ,'{Review}');")
            conn.commit()
            conn.close()
            return redirect(url_for('feedback',id=id))

    return render_template('feedbacks.html', posts=posts)

########################################################################################
@app.route("/feedback_admin/<int:id>" , methods=['GET', 'POST'])
def feedback_admin(id): 
    posts = get_Review(id)
    return render_template('admin_feed.html', posts=posts)
########################################################################################
@app.route('/new_hotel', methods=('GET', 'POST'))
def new_hot():
    if request.method == 'POST':
        hotName = request.form['hotName']
        pic = request.files['mypict']
        hotDes = request.form['hotDes']
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db_conn()
        conn.execute(f"INSERT INTO Hotels (hotName, hotDes, picture) VALUES('{hotName}', '{hotDes}' ,'{filename}');")
        conn.commit()
        conn.close()
        return redirect(url_for('hot_admin'))

    return render_template('Add_hotel.html')
########################################################################################
@app.route('/home_contact',methods=['POST'])
def message():
     messName = request.form['messName']
     messEmail = request.form['messEmail']
     messPhone = request.form['messPhone']
     message = request.form['message']
     conn = get_db_conn()
     conn.execute(f"INSERT INTO messages (messName, messEmail, messPhone,message_des) VALUES('{messName}', '{messEmail}' ,'{messPhone}','{message}');")
     conn.commit()
     mass = conn.execute('select * from messages').fetchall()
     print(mass)
     conn.close()
     return redirect(url_for('home_page'))
################################################################################################
@app.route('/messages',methods=['GET'])
def get_mess():
    conn = get_db_conn()
    res = conn.execute('select * from messages').fetchall()
    conn.close()
    return render_template('retrive_mess.html',row=res)
################################################################################################
@app.route('/users',methods=['GET'])
def get_user():
    conn = get_db_conn()
    res = conn.execute('select * from users').fetchall()
    conn.close()
    return render_template('users.html',row=res)
################################################################################################
@app.route('/delete_message/<int:id>',methods=['POST','GET'])
def delete_mess(id):
    conn = get_db_conn()
    conn.execute('DELETE from messages where mess_id=?',(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_mess'))
################################################################################################
@app.route('/delete_user/<int:id>',methods=['POST','GET'])
def delete_user(id):
    conn = get_db_conn()
    conn.execute('DELETE from users where log_id=?',(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_user'))
################################################################################################

@app.route('/admin_login',methods=['POST','GET'])
def admin():
        return render_template('login.html')
################################################################################################
@app.route('/admin_back',methods=['POST','GET'])
def admin_back():
        return render_template('admin.html')
################################################################################################
@app.route('/contact_us',methods=['POST','GET'])
def contact_us():
        return render_template('contact.html')
################################################################################################
@app.route('/admin_page',methods=['POST'])
def validition():
    if  request.method == 'POST':
        username = request.form['username']
        a_pass = request.form['password']
        if username == 'admin' and int(a_pass) == 1001505 :
            return redirect(url_for('admin_back'))
        else:
         flash('incorrect information please try again')
    return redirect(url_for('admin'))
################################################################################################
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit_comment(id):
    post = get_Review(id)
    conn = get_db_conn()
    if request.method == 'POST':
        #FirstName = request.form['FirstName']
        #LastName = request.form['LastName']
        Review = request.form['Review']
        HotelID = conn.execute('SELECT HotelID from Reviews WHERE ReviewID=?', (id,)).fetchone()[0]
        conn.execute('UPDATE Reviews SET Review = ?'
                         ' WHERE ReviewID = ?',
                         (Review, id))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback_admin', id=HotelID))
    return render_template('update_feedback.html',post=post)

########################################################################################
@app.route('/update_hotel/<int:id>', methods=('GET', 'POST'))
def update_hot(id):
    conn = get_db_conn()
    if request.method == 'POST':
        hotName= request.form['hotName']
        hotDes= request.form['hotDes']
        picture=request.files['mypict']
        if picture:
             filename = secure_filename(picture.filename)
             picture.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
             conn.execute(f"update Hotels set  hotName='{ hotName}',hotDes='{hotDes}',picture ='{filename}' where HotelID={id}")
        elif not picture:
             conn.execute(f"update Hotels set  hotName='{ hotName}',hotDes='{hotDes}' where HotelID={id}")
        conn.commit()
        conn.close()
    elif request.method == 'GET':
       conn= conn.cursor().execute(f"select * from Hotels where HotelID={id}")
       new=conn.fetchone()
       conn.close()
       return render_template('update_hotel.html',new=new)
    return redirect(url_for('hot_admin'))
#####################################################################################

@app.route('/search', methods=('GET', 'POST'))
def search_hot():
    if 'name' in request.form:
        name=request.form['name']
    conn=get_db_conn().cursor()
    conn.execute(f"select * from Hotels where hotName like '{name}%';")
    data=conn.fetchall()
    conn.close()
    return render_template("users_hotel.html",rows=data)

###############################################################################################
@app.route('/search_user', methods=('GET', 'POST'))
def search_user():
    if 'user' in request.form:
        name=request.form['user']
    conn=get_db_conn().cursor()
    conn.execute(f"select * from users where username like '{name}%';")
    data=conn.fetchall()
    conn.close()
    return render_template("users.html",row=data)

###############################################################################################