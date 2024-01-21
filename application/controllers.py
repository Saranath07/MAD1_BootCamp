from flask import current_app as app
from main import USER
from flask import render_template, request, redirect, url_for, session
from .database import db
from .models import *



@app.route("/addTheatre", methods = ["GET", "POST"])
def addTheatre():
    user_id = session.get('user')
        # Collect all info
    USER = User.query.filter_by(id = user_id).first()
    if request.method == "POST":

        
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
    user_id = session.get('user')
        # Collect all info
    USER = User.query.filter_by(id = user_id).first()
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



@app.route("/editTheatre/<id>", methods = ["POST", "GET"])
def editTheatre(id):
    user_id = session.get('user')
        # Collect all info
    USER = User.query.filter_by(id = user_id).first()
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



@app.route("/shows/<id>")
def show(id):
    user_id = session.get('user')
        # Collect all info
    USER = User.query.filter_by(id = user_id).first()
    shows = Shows.query.filter_by(movie_id = id).all()
    theatres = []
    for show in shows:
        theatre = Theatres.query.filter_by(id = show.theatr_id).first()
        theatres.append(theatre)


@app.route("/profile")
def myPage():
    return render_template("myPage.html", name = USER.username)


@app.route("/search")
def search():
    user_id = session.get('user')
        # Collect all info
    USER = User.query.filter_by(id = user_id).first()
    query = request.args.get("query")
    movies = Movies.query.filter(Movies.movieName.like(f"%{query}%")).all()

    return render_template("search.html", movies = movies, name = USER.username, isAdmin = USER.idAdmin)