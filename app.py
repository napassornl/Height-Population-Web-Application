from flask import Flask, render_template, request,send_file
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
# can use psycopg2 library to operate for PostgreSQL too, but
# to operate PostgreSQL in flask, it is better to use SQLAlchemy library
# More higher level than psycopg2, don't have to est a connection, commit change, etc
from send_email import send_email
from werkzeug import secure_filename # use for securing files uploads - library installed in flask

app=Flask(__name__)
# specifying URI of database in computer to connect with flask app
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1490511358@localhost/height_collector' # pointing to local database
# To create a web seiver live, need to create a database in heroku and connect to this app in heroku and get URI of database
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://cdskzwiqwabput:9b56a2272c01073c1f478adf5687e4fb1f2fccd75f2033a5bea00c9368d5733a@ec2-54-83-48-188.compute-1.amazonaws.com:5432/d5ro1nf4rnttmt?sslmode=require'
# connecting database with heroku app, then need to create a table with columns in the database - db.create_all()
db=SQLAlchemy(app) # creates a SQLALCHEMY object and pass name of flask object

class Data(db.Model): # a subclass of the SQLAlchemy class - inheritance
    __tablename__="data" # create a table when class called
    # create the columns
    id=db.Column(db.Integer, primary_key=True) # pass datatype and set as the primary key
    email=db.Column(db.String(120), unique=True) # pass length of string dataype and make sure email is unique
    height=db.Column(db.Integer)

    def __init__(self,email,height):
        self.email=email
        self.height=height


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=['POST']) # the two arguments are in post method=passed later
def success():
    global file # so variable can be access throughout the script
    # catches the two above arguments
    # first is get request from homepage
    # 127.0.0.1 - - [25/Aug/2017 19:20:51] "GET / HTTP/1.1" 200 - napassorn@gmail.com
    # second is post request from success page
    # 127.0.0.1 - - [25/Aug/2017 19:21:00] "POST /success HTTP/1.1" 200 -
    if request.method=='POST':
        # email=request.form["email_name"] # grabs the form elements (in html file) that stored in this variable
        file=request.files["file"] # for users to upload a file into the website, stores a file object
        file.save(secure_filename("uploaded_"+file.filename)) # saves the uploaded file in your current directory, passing the filename
        # secure_filename protects hackers - they might pass path of directory
        with open("uploaded_"+file.filename, "a") as f:
            f.write("This was added later")
        # height=request.form["height_name"]
        # send the form elements in the PostgreSQL database
        # if db.session.query(Data).filter(Data.email==email).count()==0: #pass blueprint of class field
            # data =Data(email,height) # creates the Data object and pass to the database
            # db.session.add(data)
            # db.session.commit()
            # then calculate the average
            # average_height=db.session.query(func.avg(Data.height)).scalar() # to get average value
            # average_height=round(average_height,1)
            # count=db.session.query(Data.height).count() #how many rows in database
            # print(average_height)
            # send_email(email,height, average_height,count) # functions that sends an email, function is in another py
            # need to check if the input in the form is already in the database
            # get 0 for when unique email and 1 otherwise
        print(file)
        print(type(file))
        return render_template("index.html", btn="download.html") # once file upload, want to render a download button in index page, instead of a success page
    # return render_template("index.html",
    # text="Seems like we've got something from that email address already!")
    # if same email address will stay on same page with a warning
    # will pass the text through the index.html via a placeholder {{text | safe}}

@app.route('/download')
def download():
    return send_file("uploaded_"+file.filename, attachment_filename="yourfile.csv", as_attachment=True) # a method that sends a file to the user, passes the file to send and new name

if __name__ =='__main__':
    app.debug=True
    app.run()
