from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from application.models import *


from application.database import db
from application.config import *


app = Flask(__name__)

api = Api(app)

app = None
api = None

def create_app():
    
    app = Flask(__name__)
    if os.getenv("ENV","development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    
    
    api = Api(app)
    app.app_context().push()
    
    
    
    return app, api

USER = None

app, api = create_app()



from application.signup import *
from application.movie_controllers import *
from application.login_controllers import *
from application.controllers import *











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
    
    def put(self, user_id):
        return {
            "userid" : user_id
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