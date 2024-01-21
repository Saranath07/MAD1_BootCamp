from flask import current_app as app
from flask import render_template, request, redirect, url_for
from .database import db
from .models import User



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