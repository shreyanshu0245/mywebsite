from flask import Flask, render_template, request,url_for,redirect,flash
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = 'some_secret'

engine = create_engine("postgresql://postgres:sona@localhost:1234/users")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/hello", methods=["GET","POST"])
def hello():
    if request.method=="GET":
        return redirect(url_for('index'))

    else:
        fname = request.form.get("fname")
        fname = fname.capitalize()
        lname = request.form.get("lname")
        lname = lname.capitalize()
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        age = request.form.get("age")
        location = request.form.get("location")

        if fname == '' and age == '':
            flash('Invalid Credentials !!')
            return render_template("register.html",message='True')
        else:
            db.execute("INSERT INTO users(fname, lname, username, password, email, mobile, age, location) VALUES (:fname, :lname, :username, :password, :email, :mobile, :age, :location)",
                    {"fname": fname, "lname": lname,"username": username, "password": password, "email": email, "mobile": mobile, "age": age, "location": location})
            db.commit()

            users = db.execute("SELECT * FROM users").fetchall()

            return render_template("hello.html", fname=fname,lname=lname,username=username,password=password,email=email,mobile=mobile,age=age,location=location,users=users)

if __name__ == '__main__':
    app.debug = True
    app.run()
