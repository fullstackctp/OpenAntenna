from email.policy import default
from lib2to3.pgen2.token import TILDE
from flask import Flask, session, request, redirect, url_for, render_template
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import result

from sqlalchemy import text, Column, create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import datetime
import os
import hashlib

Base=declarative_base()

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Database Connection
 

# app.config['UPLOAD_FOLDER_1']="/home/ctp/Desktop/webfactory/OpenAntenna/static/media/audio"
# app.config['UPLOAD_FOLDER_2']="/home/ctp/Desktop/webfactory/OpenAntenna/static/media/video"
# app.config['UPLOAD_FOLDER_3']="/home/ctp/Desktop/webfactory/OpenAntenna/static/media/others"

path="/home/ctp/Desktop/webfactory/OpenAntenna/static/media"


engine = create_engine(
    "mysql://deependra:1234@localhost:3306/myfactory")     # substitue the 'user:1234@localhost:3306/openantenna' with <username>:<password>@<host>:<port>/<DB_name>

# initialize the Metadata Object
meta = MetaData(bind=engine)
MetaData.reflect(meta)


db = SQLAlchemy(app)

 



### creating Databases Tables

class analytics(Base):
    __tablename__="analytics"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    ip = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    method = db.Column(db.String(10),nullable=False)
    request = db.Column(db.String(300),nullable=False)
    referral = db.Column(db.String(300),nullable=False)
    client = db.Column(db.String(300),nullable=False)
    response = db.Column(db.String(10),nullable=False)
    databased_time = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    country = db.Column(db.String(30),nullable=False)
    city = db.Column(db.String(30),nullable=False)
    state = db.Column(db.String(30),nullable=False)
    latitude = db.Column(db.String(10),nullable=False)
    longitude = db.Column(db.String(10),nullable=False)
    postal = db.Column(db.String(100),nullable=True)

    def __str__(self):
        return f'<analytics {self.id}>'


class donation_methods(Base):
    __tablename__="donation_methods"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    service = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(300),nullable=False)
    active = db.Column(db.Integer,autoincrement=False)
     

    def __str__(self):
        return f'<donation_methods {self.id}>'


class posts(Base):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(750), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20),nullable=False)
    content = db.Column(db.Text,nullable=False)
    image = db.Column(db.String(300),nullable=False)
    length = db.Column(db.String(20),nullable=False)
    status = db.Column(db.String(20),nullable=False)
    submission_time = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),nullable=False)
    publish_time = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),nullable=False)
    requests = db.Column(db.Integer, nullable=False)
    title_slug = db.Column(db.String(750),nullable=False)

    def __str__(self):
        return f'<posts {self.id}>'
 


class relays(Base):
    __tablename__="relays"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(500),nullable=False)
    type = db.Column(db.String(100),nullable=False)

    def __str__(self):
        return f'<relays {self.id}>'


class settings(Base):
    __tablename__="settings"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(750), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    image = db.Column(db.String(300),nullable=False)
    podcast_category = db.Column(db.String(300),nullable=False)
    email = db.Column(db.String(300),nullable=False)
    explicit = db.Column(db.String(20),nullable=False)
    donations_active = db.Column(db.Integer, nullable=False)
    donate_description = db.Column(db.String(1000),nullable=False)
    shortened_name = db.Column(db.String(100),nullable=False)
     

    def __str__(self):
        return f'<settings {self.id}>'


class social(Base):
    __tablename__="social"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(300),nullable=False)
    image = db.Column(db.String(300),nullable=False)
    
    def __str__(self):
        return f'<social {self.id}>'

class GuestUser(Base):
    __tablename__="guest_user"
    id = Column(db.Integer, primary_key=True,autoincrement=True)
    name = Column(db.String(100), nullable=False)
    email = Column(db.String(50),nullable=False)
    message = Column(db.String(1000), nullable=False)


 


class users(Base):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(1000), nullable=True)
    email = db.Column(db.String(1000),nullable=False)
    phone = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    date_registered =  db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.now(),nullable=False)
    last_login = db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.now(),nullable=False)
    user_type = db.Column(db.String(10),nullable=False)
    status = db.Column(db.String(10),nullable=False)
     

    def __str__(self):
        return f'<users {self.id}>'



class blog_post_data(Base):
    __tablename__="blog_post_data"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_name = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    type = db.Column(db.String(300), nullable=False)
    file = db.Column(db.String(300),nullable=False)
    
    def __str__(self):
        return f'<blog_post_data {self.id}>'




Base.metadata.create_all(engine)



@app.route("/")
def home():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")
    posts_data=engine.execute(sql).fetchall()
        
    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")
    donation_methods_data=engine.execute(sql).fetchall()
    return(render_template('index.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))


@app.route("/posts/")
def posts():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")
    posts_data=engine.execute(sql).fetchall()   
    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")    
    donation_methods_data=engine.execute(sql).fetchall()          
    return(render_template('posts-listing.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/post/<post_slug>")
def single_post_page(post_slug):
    # Get individual post data
    sql = text("SELECT * FROM posts WHERE status = 'published' and title_slug = '{}' ORDER BY id DESC;".format(str(post_slug)))
    post_data=engine.execute(sql).fetchone()        

    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")   
    posts_data=engine.execute(sql).fetchall() 
    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")
    donation_methods_data=engine.execute(sql).fetchall()  
    return(render_template("post-page.html", settings_data=settings_data, posts_data=posts_data, post_data=post_data, donation_methods_data=donation_methods_data))

@app.route("/donate")
def donate():
    # Get donate status and description
     
    sql = text("SELECT * FROM settings LIMIT 1;")
    show_data=engine.execute(sql).fetchone()
    if show_data[7] == 1:
        # Get settings data
        sql = text("SELECT * FROM settings;")
        settings_data=engine.execute(sql).fetchone()
        # Get posts data
        sql = text("SELECT * FROM posts WHERE status = 'published';")
        posts_data=engine.execute(sql).fetchall()    
        # Get donations data
        sql = text("SELECT * FROM donation_methods WHERE active = 1;")
        donation_methods_data=engine.execute(sql).fetchall()        
        return render_template('donate.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data)
    else:
        return(redirect(url_for('home')))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")
    posts_data=engine.execute(sql).fetchall()    

    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")
    donation_methods_data=engine.execute(sql).fetchall() 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # print(name, email, message) 

        data = ( { "name": name,
          "email": email,
          "message": message},
          )
        statement = text("""INSERT INTO guest_user (name, email,
        message) VALUES(:name, :email,
        :message)""")

        for line in data:
            engine.execute(statement, **line)

        return redirect(url_for('home'))
    return(render_template('contact.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    if 'username' in session:
        # Get post data
        sql = text("SELECT * FROM posts ORDER BY id DESC;")
        post_data=engine.execute(sql).fetchall()   
        # Automatically create length and title_slug for db
        return(render_template('admin.html', settings_data=settings_data,post_data=post_data))
    return("Please <a href='/login'>Log In</a> For Access")


@app.route("/admin/edit-upload",methods=['GET','POST'])
def admin_edit_upload():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()  
    if 'username' in session: 
        # Automatically create length and title_slug for db
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            types = request.form.get('type')
            files = request.form.get('file')
            username = session['username']

            file_name= str(request.files.get('file'))

            file_ending= file_name.split("'")[1][-4:]
            
            if types == 'Podcast Episode'  and file_ending == '.mp3':

                media=request.files.get('file')

                if os.path.isdir(path + '/' + 'audio'): 
                    
                    print(' exists.')
                else:
                    os.mkdir(path + '/' + 'audio')    
                    print( ' created.')
                media.save(os.path.join(f'{path}/audio/', media.filename))

                data = ( { 'user_name':username,
                "title": title,
                "description": description,
                'type':'audio',
                    "file":media.filename},
                )
                statement = text("""
                INSERT INTO blog_post_data (user_name,title, description,
                type,file) VALUES(:user_name, :title, :description,
                :type,:file)
                """)

                for line in data:
                    engine.execute(statement, **line)

                print("Image saved in .mp3 formate")


            elif types == "Video Post"  and file_ending == '.mp4':
                
                media=request.files['file']
                if os.path.isdir(path + '/' + 'video'): 
                    
                    print(' exists.')
                else:
                    os.mkdir(path + '/' + 'video')    
                    print( ' created.')
                media.save(os.path.join(f'{path}/video/', media.filename))

                data = ( { 'user_name':username,
                "title": title,
                "description": description,
                'type':'video',
                    "file":media.filename},
                )
                statement = text("""
                INSERT INTO blog_post_data (user_name,title, description,
                type,file) VALUES(:user_name, :title, :description,
                :type,:file)
                """)

                for line in data:
                    engine.execute(statement, **line)
                print("Image saved in .mp4 formate")
                 

            elif types == "Blog Post" and file_ending != '.mp3' and file_ending != '.mp4' :
                media=request.files['file']

                if os.path.isdir(path + '/' + 'others'): 
                    
                    print(' exists.')
                else:
                    os.mkdir(path + '/' + 'others')    
                    print( ' created.')

                media.save(os.path.join(f'{path}/others/', media.filename))
                
                data = ( { 'user_name':username,
                "title": title,
                "description": description,
                'type':'others',
                    "file":media.filename},
                )
                statement = text("""
                INSERT INTO blog_post_data (user_name,title, description,
                type,file) VALUES(:user_name, :title, :description,
                :type,:file)
                """)

                for line in data:
                    engine.execute(statement, **line)

                print("Image saved in other formate")


            else:
                print("please select valid formate")


        return(render_template('admin-edit-upload.html', settings_data=settings_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/analytics")
def admin_analytics():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()     
    if 'username' in session:
        # Get analytics data
        sql = text("SELECT * FROM analytics ORDER BY id DESC LIMIT 1000;") 
        analytics_data=engine.execute(sql).fetchall()  
        # Automatically create length and title_slug for db
        return(render_template('admin-analytics.html',settings_data=settings_data, analytics_data=analytics_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/analytics/ip/<ip_id>")
def admin_analytics_ip(ip_id):
    ip_address = ip_id.replace('-','.')
    return(ip_address)

    
@app.route("/admin/users")
def admin_users():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone() 
    if 'username' in session: 
        # Get user data
        sql = text("SELECT * FROM users ORDER BY id DESC;")  
        user_data=engine.execute(sql).fetchall() 
        return(render_template('admin-users.html',settings_data=settings_data,user_data=user_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/settings")
def admin_settings():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone() 
    if 'username' in session: 
        # Automatically create length and title_slug for db
        return(render_template('admin-settings.html',settings_data=settings_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    engine.execute(sql).fetchone() 
    if request.method == 'POST':
        # # Get potential user data
        email = request.form['email']
        password1 = request.form['password']
        password2 = hashlib.md5(password1.encode())
        password = password2.hexdigest()

        sql = text("SELECT * FROM users WHERE email = '{}' AND password = '{}';".format(email,password))
        user_data=engine.execute(sql).fetchone() 
        if user_data == None:
            return(redirect(url_for('login')))
        else:
            session['username'] = user_data[1]
            session['email'] = user_data[3]
            return(redirect(url_for('admin')))

    return(render_template('login.html'))


@app.route('/logout')
def logout():
    hii= session.pop('username',None)
    return redirect('/')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    engine.execute(sql).fetchone() 
    sql = text("SELECT * FROM users;")
    
    if request.method == 'POST':
        # # Get potential user data
        firstName = request.form['firstName']
        status = request.form['status']
        phoneNo = request.form['phoneNo']
        email = request.form['email']
        user_type = request.form['user_type']
        password1 = request.form['password']
        password2 = hashlib.md5(password1.encode())
        password = password2.hexdigest()

        mails = engine.execute(sql).fetchall() 
        store=[]
        for i in mails:
            store.append(i[3])


        if email not in store:

            data = ( { "firstName": firstName,
            "status": status,
            "phoneNo": phoneNo,
                "email": email,
                "password": password,
                "user_type": user_type,
                "picture":"New_Image.jpg"},
            )
            statement = text("""
            INSERT INTO users (name, picture, email,
            status,phone,password,user_type) VALUES(:firstName, :picture, :email,
            :status,:phoneNo,:password,:user_type)
            """)

            for line in data:
                engine.execute(statement, **line)

            return redirect(url_for('home'))
        else:
            print("Please try with other email")
    return(render_template('signup.html'))

if __name__ == "__main__":
    
    app.secret_key = os.urandom(24)
    app.run(debug = True)


