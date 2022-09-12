from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)

class User_indexAPI(MethodView):
    def get(self):
        users = User.query.all()
        result = []
        for user in users:
            jsonUser = {
                'id': user.id,
                'admin': user.admin,
                'email': user.email,
                'registered_on': user.registered_on
            }
            # print(jsonify(jsonUser))
            result.append(jsonUser)
        return make_response(str(result))



class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json(); print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token

                print("user.id: ")
                print(user.id)
                print("\n")
                auth_token = user.encode_auth_token(user.id)
                print("auth_token: ")
                print(auth_token)
                print("\n")
                print("decode: ")
                print(user.decode_auth_token(auth_token))
                print("\n")

                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': user.decode_auth_token(auth_token)
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)

index_view = User_indexAPI.as_view('index_api')

auth_blueprint.add_url_rule(
    '/users/index',
    view_func=index_view,
    methods=['GET']
)