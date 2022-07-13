"""
"""
from email.policy import default
import os
import hashlib
import datetime
from sqlalchemy import text
from flask import Flask, jsonify, session, request, redirect, url_for, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

app.secret_key = "super secret key"
path1=os.getcwd()
file_path="static/media"
path=os.path.join(path1,file_path)
engine = create_engine('mysql://root:root@localhost:3306/test101')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conn = engine.connect()
db = SQLAlchemy(app)

class analytics(Base):
    """
    Database Connection SQlAlchemy with Mysql
    """
    __tablename__ = "analytics"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    request = db.Column(db.String(300), nullable=False)
    referral = db.Column(db.String(300), nullable=False)
    client = db.Column(db.String(300), nullable=False)
    response = db.Column(db.String(10), nullable=False)
    databased_ti = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    country = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    latitude = db.Column(db.String(10), nullable=False)
    longitude = db.Column(db.String(10), nullable=False)
    postal = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"


class donation_methods(Base):
    """
    donations names
    """
    __tablename__ = "donation_methods"

    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    active = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"{self.id}-{self.service}"

class Posts(Base):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(750), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    type = db.Column(db.String(300), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    length = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(300), nullable=False)
    subission_t = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    publish_time = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


    req_uest = db.Column(db.Integer, nullable=False)
    title_slug = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"
class relays(Base):
    __tablename__ = "relays"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    type = db.Column(db.String(300), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    length = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(300), nullable=False)

    request = db.Column(db.Integer, nullable=False)
    title_slug = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"

class settings(Base):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    podcast_cate = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    explicit = db.Column(db.String(300), nullable=False)
    donations_ac = db.Column(db.String(300), nullable=False)

    donate_descr = db.Column(db.Integer, nullable=False)
    shortened_na = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"

class social(Base):
    __tablename__ = "social"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"

class users(Base):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    picture = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False, unique=True)
    phone = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)

    date_register = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    last_login = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_type = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(300), nullable=False)
    def is_active(self):
        """True, as all users are active."""
        return True

    def __repr__(self) -> str:
        return f"{self.id}"


class Guest(Base):
    __tablename__ = "guest_user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    message = db.Column(db.String(300), nullable=False)


class File_post(Base):
    __tablename__ = "File_post"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(300), nullable=False)
    file_name = db.Column(db.String(300), nullable=False)

Base.metadata.create_all(engine)

@app.route("/")
def home():
    sql = text("SELECT * FROM settings")
    settings_data = engine.execute(sql).fetchone()
    print(settings_data)
    sql = text("SELECT * FROM posts WHERE status = 'published' ")
    posts_data = engine.execute(sql)
    sql = text("SELECT * FROM donation_methods WHERE active = 1")
    donation_methods_data = engine.execute(sql)
    return(render_template('index.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))


@app.route("/posts/")
def posts():

    sql = text("SELECT * FROM settings")
    settings_data = engine.execute(sql).fetchone()
    sql = text("SELECT * FROM posts WHERE status = 'published' ")
    posts_data = engine.execute(sql).fetchall()
    sql = text("SELECT * FROM donation_methods WHERE active = 1")
    donation_methods_data = engine.execute(sql)
    return(render_template('posts-listing.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))


@app.route("/post/<post_slug>")
def single_post_page(post_slug):
    sql = text("SELECT * FROM posts WHERE status = 'published' and title_slug = '{}' ORDER BY id DESC;".format(str(post_slug)))
    post_data = engine.execute(sql).fetchone()
    sql = text("SELECT * FROM settings")
    settings_data = engine.execute(sql).fetchone()
    sql = text("SELECT * FROM posts WHERE status = 'published'")
    posts_data = engine.execute(sql).fetchall()
    sql = text("SELECT * FROM donation_methods WHERE active = 1")
    donation_methods_data = engine.execute(sql)
    return(render_template("post-page.html", settings_data=settings_data, posts_data=posts_data, post_data=post_data, donation_methods_data=donation_methods_data))


@app.route("/donate")
def donate():
    sql = text("SELECT * FROM settings LIMIT 1")
    show_data = engine.execute(sql).fetchone()
    if show_data:
        sql = text("SELECT * FROM settings")
        settings_data = engine.execute(sql).fetchone()
        sql = text("SELECT * FROM posts WHERE status = 'published' ")
        posts_data = engine.execute(sql).fetchall()
        sql = text("SELECT * FROM donation_methods WHERE active = 1")
        donation_methods_data = engine.execute(sql).fetchall()
        return render_template('donate.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data)
    else:
        return(redirect(url_for('home')))


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    """
    Get settings data
    """
    sql = text("SELECT * FROM settings")
    settings_data = engine.execute(sql).fetchone()

    """
    Get posts data
    """
    sql = text("SELECT * FROM posts WHERE status = 'published' ")
    posts_data = engine.execute(sql).fetchall()

    """
    Get donations data
    """
    sql = text("SELECT * FROM donation_methods WHERE active = 1")

    donation_methods_data = engine.execute(sql).fetchall()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(name, email, message)
        data = ({
            "name": name,
            "email": email,
            "message": message,
        },)
        statement = text("""INSERT INTO guest_user (name, email,
                        message) VALUES(:name, :email,
                            :message)""")
        for line in data:
            engine.execute(statement, **line)

        return redirect(url_for('home'))

    return(render_template('contact.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    """
    Get settings data
    """
    sql = text("SELECT * FROM settings")
    settings_data = engine.execute(sql).fetchone()

    if 'username' in session:
        sql = text("SELECT * FROM posts ORDER BY id DESC")
        posts_data = engine.execute(sql).fetchall()

        """
        Automatically create length and title_slug for db
        """
        return(render_template('admin.html', settings_data=settings_data, post_data=posts_data))
    return redirect(url_for('loginn'))


@app.route("/admin/edit-upload", methods=['GET', 'POST'])
def admin_edit_upload():
    sql = text("SELECT * FROM users ")
    settings_data = engine.execute(sql).fetchone()

    if 'username' in session:
        if request.method == 'POST':
            name = session['username']
            email = session['email']
            title = request.form.get('title')
            description = request.form.get('desc')
            types = request.form.get('type')
            files = str(request.files.get("file"))
            file_ending = files.split("'")[1][-4:]
            if types == '1' and file_ending == ".mp3":
                media=request.files.get('file')
                if os.path.isdir(path + '/' + 'audio'): 
                    pass
                else:
                    os.mkdir(path + '/' + 'audio')    
                media.save(os.path.join(f'{path}/audio/', media.filename))                  
                data = ({
                    "name": name,
                    "title": title,
                    "email": email,
                    "description": description,
                    "file_type": "Mp3",
                    "file_name": media.filename,
                },)
                statement = text("""INSERT INTO File_post (name, title,email, description,
                    file_type , file_name) VALUES(:name,:title, :email, :description,
                        :file_type, :file_name)""")
                for line in data:
                    engine.execute(statement, **line)
            elif types == '2' and file_ending == '.mp4':
                media=request.files.get('file')
                if os.path.isdir(path + '/' + 'video'): 
                    pass
                else:
                    os.mkdir(path + '/' + 'video')    

                media.save(os.path.join(f'{path}/video/', media.filename))   

                print("Mp4 saved is Video folder")

                data = ({
                    "name": name,
                    "title": title,
                    "email": email,
                    "description": description,
                    "file_type": "Mp4",
                    "file_name": media.filename,

                },)
                statement = text("""INSERT INTO File_post (name, title,email, description,
                    file_type , file_name) VALUES(:name,:title,:email, :description,
                        :file_type, :file_name)""")

                for line in data:
                    engine.execute(statement, **line)


            elif types == "3":
                media=request.files.get('file')
                if os.path.isdir(path + '/' + 'other'): 
                    pass
                else:
                    os.mkdir(path + '/' + 'other')    
                media.save(os.path.join(f'{path}/other/', media.filename)) 
                data = ({
                    "name": name,
                    "title": title,
                    "email": email,
                    "description": description,
                    "file_type": "Blog",
                    "file_name": media.filename,

                },)
                statement = text("""INSERT INTO File_post (name, title,email, description,
                    file_type , file_name) VALUES(:name,:title,:email, :description,
                        :file_type, :file_name)""")

                for line in data:
                    engine.execute(statement, **line)

                print("File inserted in the database")

            else:
                return "please select valid formate"

        return(render_template('admin-edit-upload.html', settings_data=settings_data))
    return("Please <a href='/admin'>Log In</a> For Access")


@app.route("/admin/analytics")
def admin_analytics():
    """
    Get settings data
    """
    sql = text("SELECT * FROM settings ")
    settings_data = engine.execute(sql).fetchone()

    if 'username' in session:
        """
        Get analytics data
        """
        sql = "SELECT * FROM analytics ORDER BY id DESC LIMIT 1000;"
        analytics_data = engine.execute(sql).fetchall()
        return(render_template('admin-analytics.html', settings_data=settings_data, analytics_data=analytics_data))
    return("Please <a href='/login'>Log In</a> For Access")


@app.route("/admin/analytics/ip/<ip_id>")
def admin_analytics_ip(ip_id):
    ip_address = ip_id.replace('-', '.')
    return(ip_address)


@app.route("/admin/users")
def admin_users():
    """
    Get settings data
    """
    sql = text("SELECT * FROM settings ")
    settings_data = engine.execute(sql).fetchone()

    if 'username' in session:
        """
        Get user data
        """
        sql = "SELECT * FROM users ORDER BY id DESC;"
        user_data = engine.execute(sql).fetchall()

        return(render_template('admin-users.html', settings_data=settings_data, user_data=user_data))
    return("Please <a href='/login'>Log In</a> For Access")


@app.route("/admin/settings")
def admin_settings():
    """
    Get settings data
    """
    sql = text("SELECT * FROM settings")
    settings_data = engine.execute(sql).fetchone()

    if 'username' in session:
        """
        Automatically create length and title_slug for db
        """
        return(render_template('admin-settings.html', settings_data=settings_data))
    return("Please <a href='/signup'>Log In</a> For Access")


@app.route('/loginn', methods=['GET', 'POST'])
def loginn():
    return render_template('login_new.html')

@app.route('/signupp', methods=['GET', 'POST'])
def signupp():
    return render_template('signupp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        """
        Get potential user data
        """
        email = request.form['email']
        password1 = request.form['password']
        password2 = hashlib.md5(password1.encode())
        password = password2.hexdigest()
        sql = text(
            "SELECT * FROM users WHERE email = '{}' AND password = '{}';".format(email, password))
        user_data = engine.execute(sql).fetchone()

        if user_data == None:
            return(redirect(url_for('loginn')))
        else:
            session['username'] = user_data[1]
            session['email'] = user_data[3]
            return redirect(url_for('home'))
    return "wrong credentials "


@app.route('/admin/get_data')
def getdata():
    sql = text("SELECT * FROM settings ")
    settings_data = engine.execute(sql).fetchone()

    if 'username' in session:
        email = session['email']
        """
        Get user data
        """
        sql = text(
            "SELECT * FROM File_post WHERE email = '{}';".format(email))
        user_data = engine.execute(sql).fetchall()
        return(render_template('getdata.html', settings_data=settings_data, user_data=user_data))
    return("Please <a href='/login'>Log In</a> For Access")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Get seetings data
    """
    sql = text("SELECT * FROM settings;")
    engine.execute(sql).fetchone() 
    sql = text("SELECT * FROM users;")
    
    if request.method == 'POST':
        """
        Get potential user data
        """
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

            return redirect(url_for('loginn'))
        else:
            print("Please try with other email")
    return(render_template('signup.html'))

@app.route('/logout')
def logout():
    """
    Logout
    """
    if 'username' in session:
        session.pop('username', None)

    return redirect(url_for('loginn'))


@app.route('/data', methods=["GET", "POST"])
def data():
    print("inside data")
    print(request.get_data("file"))

    if request.method == "POST":
        files = str(request.form.get("file"))
        print(files,'/********************')
        file_ending = files.split("'")[0][-4:]
        if file_ending == ".mp3":
            print("your type is correct ", '.mp3')
            try:
                path1=f'{path}/audio'+"/"+files
                return send_file(path1,as_attachment=True)
            except:
                return   "file not found"
        if file_ending == ".mp4":
            print("your type is correct ", '.mp4')
            try:
                path1=f'{path}/video'+"/"+files
                return send_file(path1,as_attachment=True)
            except:
                return   "file not found"

        else:
            try:
                path1=f'{path}/other'+"/"+files
                return send_file(path1,as_attachment=True)
            except:
                return   "file not found"

    return "file not found"


@app.route('/delete/<id>')
def delete(id):
    sql = text(
            "SELECT * FROM File_post WHERE id = '{}';".format(id))
    user_data = engine.execute(sql).fetchall()

    if user_data[0]==id:
        hii= session.delete('id',None)
    return  redirect('/')

@app.route('/api/posts' , methods=['GET', 'POST'])
def post():
    if request.method=="GET":
        sql = text("SELECT * FROM posts;")
        user_data = engine.execute(sql).fetchall()
        print(user_data,'*****************')
        req=jsonify({'user_data': [dict(row) for row in user_data]})

        return req
    elif request.method=="POST":
        print('post wworking **************************************************')
        data = request.get_json()
        print(data,'***********************************************************')
        print(data['title'])
        current_datetime =datetime.datetime.now()
        title=data['title'],
        description=data['description'],
        type=data['type'],
        content=data['content'],
        image=data['image'],
        length=data['length'],
        status=data['status'],
        subission_t=[str(current_datetime)],
        publish_time=[str(current_datetime)],

        req_uest=data['req_uest'],
        title_slug=data['title_slug']

        data = ( { "title": title,
            "description": description,
            "type": type,
            "content": content,
                "image": image,
                "length": length,
                "status": status,
                "subission_t":subission_t,
                "publish_time": publish_time,
                "req_uest":req_uest,
                "title_slug": title_slug
                
                },
            )
        statement = text("""
            INSERT INTO posts ( title, description, type,
            content,image,length,status,subission_t,publish_time,req_uest,title_slug) VALUES(:title,:description, :type,
            :content,:image,:length,:status,:subission_t,:publish_time,:req_uest,:title_slug)
            """)
        
        print(statement,'******************')

        for line in data:
            engine.execute(statement, **line)
        return jsonify({'message' : 'New record created at post table!'})

@app.route('/api/donations' , methods=['GET', 'POST'])
def donation():
    if request.method=="GET":
        sql = text("SELECT * FROM donation_methods;")
        user_data = engine.execute(sql).fetchall()
        req=jsonify({'user_data': [dict(row) for row in user_data]})

        return req
    elif request.method=="POST":
        data = request.get_json()
        service=data['service']
        image=data['image']
        address=data['address']
        active=data['active']
        print(service,'***************************ef*er')
        data = ( { "service": service,
            "image": image,
                "address": address,
                "active": active
                
                },
            )

        statement = text("""
            INSERT INTO donation_methods ( service, image,
            address,active) VALUES(:service, :image,
            :address,:active)
            """)
        for line in data:
            engine.execute(statement, **line)
        return jsonify({'message' : 'New record created at donation table!'})

@app.route('/api/settings' , methods=['GET', 'POST'])
def setting():
    """
    settings
    """
    if request.method=="GET":
        sql = text("SELECT * FROM settings;")
        user_data = engine.execute(sql).fetchall()
        req=jsonify({'user_data': [dict(row) for row in user_data]})
        return req
      

    elif request.method=="POST":
        data = request.get_json()
        title=data['title'],
        description=data['description'],
        image=data['image'],
        podcast_cate=data['podcast_cate'],
        email=data['email'],
        explicit=data['explicit'],
        donations_ac=data['donations_ac'],
        donate_descr=data['donate_descr'],
        shortened_na=data['shortened_na']

        data = ( { "title": title,
            "description": description,
            "image": image,
            "podcast_cate": podcast_cate,
                "email": email,
                "explicit": explicit,
                "donations_ac": donations_ac,
                "donate_descr":donate_descr,
                "shortened_na": shortened_na
                
                },
            )

        statement = text("""
            INSERT INTO settings ( title, description, image,
            podcast_cate,email,explicit,donations_ac,donate_descr,shortened_na) VALUES(:title,:description, :image,
            :podcast_cate,:email,:explicit,:donations_ac,:donate_descr,:shortened_na)
            """)
        
        for line in data:
            engine.execute(statement, **line)

        return jsonify({'message' : 'New record created at settings table!'})
    return  redirect('/')

session_email=''
@app.route('/test' )
def test():  
    if 'username' in session:
        global session_email
        session_email = session['email']       
    return session_email

@app.route('/api/users' , methods=['GET', 'POST'])
def user():
    sql = text( "SELECT * FROM users WHERE email = '{}';".format(session_email))
    getting_user_data = engine.execute(sql).fetchone()
    user_data=getting_user_data[8].lower()
    if request.method=="POST":
        data = request.get_json()
        print(data,'getting data from postman')
        getting_user_type=data['user_type']
        user_type=getting_user_type.lower()
        if user_data==user_type=="admin":
            return jsonify({'message' : "Authenticated user"})
        else:
            return jsonify({'message' : "Your are not authorised to have access"})

if __name__ == "__main__":
    app.debug = True
    app.run()
