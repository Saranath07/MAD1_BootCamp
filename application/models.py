from .database import db

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