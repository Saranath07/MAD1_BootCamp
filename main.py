from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user" 
    id = db.Column(db.Integer, primary_key = True, auto_increment = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    idAdmin = db.Column(db.Boolean, default = False)

with app.app_context():
    db.create_all()


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get('username')
        return render_template("index.html", name = name)
    
    return render_template("index.html")

@app.route("/myPage")
def myPage():
    return render_template("myPage.html")

if __name__ == "__main__":
    app.run(
        debug = True
    )
