from flask import Flask , request
from flask_restful import Resource, Api , reqparse
from flask_jwt import JWT, jwt_required, current_identity
from user import UserResource
from auto import Auto , AutoCollection
from auth_conf import authenticate, identity
import table 


app = Flask(__name__)
app.secret_key = "MySuperDuperSecretKey"
api = Api(app)
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)


api.add_resource(Auto, "/auto/<string:name>")
api.add_resource(AutoCollection, "/stock") 
api.add_resource(UserResource, "/register")


if __name__ == "__main__":
    app.run(port=8080, debug=True)