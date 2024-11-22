from datetime import timedelta
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from .env file
load_dotenv()

jwt = JWTManager()

# limiter = Limiter(
#     get_remote_address,  # Function to get the user's IP address
#     default_limits=["2000 per day", "200 per hour"],  # Default limits for all routes
#     # storage_uri="redis://localhost:6379"  # Configure with your Redis URI
# )

db = SQLAlchemy()
socketio = SocketIO()
cors = CORS()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_DAYS', 15) or 15 ))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 30)))
    # GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    # GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    # GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    # FILE_SERVER_URL = os.getenv('FILE_SERVER_URL')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
    LIMITER_ENABLED = False

authorizations = {
    "Bearer Auth": {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Add a JWT token to the header with ** Bearer &lt;JWT&gt; token to authorize **'
    }
    # 'google_oauth2': {
    #     'type': 'oauth2',
    #     'flow': 'implicit',
    #     'authorizationUrl': 'https://accounts.google.com/o/oauth2/auth',
    #     'tokenUrl': 'https://accounts.google.com/o/oauth2/token',
    #     'scopes': {
    #         'email': 'Access to email',
    #         'profile': 'Access to profile'
    #     }
    # }
}

# oauth = OAuth()
# google = oauth.remote_app(
#     'google',
#     consumer_key=os.getenv('GOOGLE_CLIENT_ID'),
#     consumer_secret=os.getenv('GOOGLE_CLIENT_SECRET', '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'),
#     request_token_params={
#         'scope': 'email profile',
#     },
#     base_url='https://www.googleapis.com/oauth2/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://oauth2.googleapis.com/token',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
# )

SOCKET_SECRET_KEY = os.getenv('SOCKET_SECRET_KEY', 'default_socket_secret_key')
