from flask import current_app as app
from main import USER
from flask import render_template, request, redirect, url_for, session
from .database import db
from .models import User, Movies


@app.route("/addMovie", methods = ["GET", "POST"])
def addMovie():
    user_id = session.get('user')
        
    USER = User.query.filter_by(id = user_id).first()
    if request.method == "POST":

       
        

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

@app.route("/editMovie/<id>", methods = ["POST", "GET"])
def edit(id):
    user_id = session.get('user')
        
    USER = User.query.filter_by(id = user_id).first()

    movie = Movies.query.filter_by(id = id).first()
    if request.method == "POST":
        movie.movieName = request.form.get("movieName")
        db.session.commit()

        return redirect("/")
    return render_template("editMovie.html", name = USER.username, isAdmin = USER.idAdmin)


@app.route("/deleteMovie/<id>")
def delete(id):
    
    movie = Movies.query.filter_by(id = id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect("/")

