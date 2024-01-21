from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
from .database import db
from .models import User



@app.route("/login", methods = ["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['user'] = user.id
            return redirect(url_for('index'))
        else:
            return redirect(url_for("error"))
        

    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('login'))
