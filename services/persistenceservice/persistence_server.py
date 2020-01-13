from flask import Flask, request
import boto3
from botocore.client import Config

import pickle
import json
import os

# get the values of the following environment variables to provide credentials
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

# Port 9000 inside the MinIO container
ENDPOINT_URL = 'http://172.18.0.2:9000'

def get_boto3_object():
    '''
    retrieves the boto3 object by sending it the proper credentials

    - the endpoint that corresponds to the MinIO container
    - Access and Secret key that were set in using environment variables
    in the MinIO container.
    - the config and region_name arguments are set to a default

    '''


    s3_obj = boto3.resource('s3',
                        endpoint_url=ENDPOINT_URL,
                        aws_access_key_id=MINIO_ACCESS_KEY,
                        aws_secret_access_key=MINIO_SECRET_KEY,
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')
    
    return s3_obj

persistence_server = Flask(__name__)

@persistence_server.route('/')
def index():
    return '''<h1>MineAI Persistence Service</h1>'''

if __name__ == '__main__':
    # runs the flask app.

    # turns on debug mode and sets the host IP address of the 
    # app to 0.0.0.0
    persistence_server.run(debug=True, host='0.0.0.0')