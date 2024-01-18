from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


USER = None

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user" 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    idAdmin = db.Column(db.Boolean, default = False)

with app.app_context():
    db.create_all()



@app.route("/login", methods = ["GET", "POST"])
def login():
    global USER
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            USER = user
            return redirect(url_for('index'))
        else:
            return redirect(url_for("error"))
        

    
    return render_template("login.html")

@app.route("/logout")
def logout():
    global USER
    USER = None
    return redirect(url_for('login'))

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        if password == cpassword:

            user = User(
                username = username,
                password = password,
                email = email,
            )

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('error'))
    return render_template("signup.html")

@app.route("/", methods = ["GET", "POST"])
def index():

    try:
        return render_template("index.html", name = USER.username)
    except:
        return redirect(url_for('error'))

@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/myPage")
def myPage():
    return render_template("myPage.html")

if __name__ == "__main__":
    app.run(
        debug = True
    )








# [user1, 56], [user2, 45], [user1, 78]
    #[
    # [user1, 56],  0
    # [user1, 78]   1
    # ]