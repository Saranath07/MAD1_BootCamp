from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with, reqparse

app = Flask(__name__)

api = Api(app)


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

class Movies(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    movieName = db.Column(db.String, nullable = False)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = 'CASCADE'), nullable = False)

class Theatres(db.Model):
    __tablename__ = "theatres"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    theatreName = db.Column(db.String, nullable = False)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = 'CASCADE'), nullable = False)

class Shows(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    movieId = db.Column(db.Integer, db.ForeignKey("movies.id", ondelete = 'CASCADE'), nullable = False)
    theatreId = db.Column(db.Integer, db.ForeignKey("theatres.id", ondelete = 'CASCADE'), nullable = False)

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

@app.route("/addMovie", methods = ["GET", "POST"])
def addMovie():
    if request.method == "POST":

        # Collect all info

        # Check if user is admin

        if USER.idAdmin:
             
             # Logic for adding movie
            movie = Movies(
                movieName = request.form.get('movieName'),
                admin_id = USER.id
            )

            db.session.add(movie)
            db.session.commit()
            
            return redirect(url_for("index"))
        else:

            # Return Error
            return "Error"
    return render_template("addMovie.html", name = USER.username, isAdmin = USER.idAdmin)

@app.route("/addTheatre", methods = ["GET", "POST"])
def addTheatre():
    if request.method == "POST":

        # Collect all info

        # Check if user is admin

        if USER.idAdmin:
             
             # Logic for adding movie
            theatre = Theatres(
                theatreName = request.form.get('name'),
                admin_id = USER.id
            )

            db.session.add(theatre)
            db.session.commit()
            
            return redirect(url_for("index"))
        else:

            # Return Error
            return "Error"
    return render_template("addTheatre.html", name = USER.username, isAdmin = USER.idAdmin)

@app.route("/", methods = ["GET", "POST"])
def index():

    try:
        movies = []
        theatres = []
        if USER.idAdmin:
            movies = Movies.query.filter_by(admin_id = USER.id).all()
            theatres = Theatres.query.filter_by(admin_id = USER.id).all()
        
        else:
            movies = Movies.query.all()
            theatres = Theatres.query.all()
        return render_template("index.html", name = USER.username, isAdmin = USER.idAdmin, movies = movies,
                               theatres = theatres)
    except:
        return redirect(url_for('login'))

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/editMovie/<id>", methods = ["POST", "GET"])
def edit(id):
    
    movie = Movies.query.filter_by(id = id).first()
    if request.method == "POST":
        movie.movieName = request.form.get("movieName")
        db.session.commit()

        return redirect("/")
    return render_template("editMovie.html", name = USER.username, isAdmin = USER.idAdmin)

@app.route("/editTheatre/<id>", methods = ["POST", "GET"])
def editTheatre(id):
    
    theatre = Theatres.query.filter_by(id = id).first()
    if request.method == "POST":
        theatreName = request.form.get("theatreName")
        movieID = request.form.get("movieID")
        theatre = Theatres.query.filter_by(id = id).first()
        if theatreName:
            theatre.theatreName = theatreName
        movie = Movies.query.filter_by(id = movieID).first()
        show = Shows(
            movieId = movieID,
            theatreId = theatre.id
        )
        db.session.add(show)
        db.session.commit()

        return redirect("/")
    return render_template("editTheatre.html", name = USER.username, isAdmin = USER.idAdmin, theatre = theatre)

@app.route("/deleteMovie/<id>")
def delete(id):
    movie = Movies.query.filter_by(id = id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect("/")

@app.route("/shows/<id>")
def show(id):

    shows = Shows.query.filter_by(movie_id = id).all()
    theatres = []
    for show in shows:
        theatre = Theatres.query.filter_by(id = show.theatr_id).first()
        theatres.append(theatre)


@app.route("/profile")
def myPage():
    return render_template("myPage.html", name = USER.username)


class UserAPI(Resource):

    def get(self, user_id):

        try:
            user = User.query.filter_by(id = user_id).first()

            if user:

                return {
                    "id" : user.id,
                    "mail" : user.email,
                    "username" : user.username,
                    "isAdmin" : user.idAdmin
                }, 200
            else:
                return {
                    "error" : "User does not exist"
                }, 403
            
        except:
            return {
                "error" : "Something went wrong"
            }, 404

    def post(self):

        data = request.get_json()

        user = User(
            email = data['email'],
            username = data['username'],
            password = data['password'],
            idAdmin = 0
        )

        db.session.add(user)
        db.session.commit()

        return {
            "message" : "User Registered Successfully"
        }, 200



api.add_resource(UserAPI, "/api/user/<user_id>", "/api/user")


if __name__ == "__main__":
    app.run(
        debug = True
    )



# 200 - 299 : Sucess
# 400 - 499 : Error
# 500 +     : HTTP Error / No internet




# [user1, 56], [user2, 45], [user1, 78]
    #[
    # [user1, 56],  0
    # [user1, 78]   1
    # ]