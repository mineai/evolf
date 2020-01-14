from flask import Flask, request
import boto3
from botocore.client import Config

import pickle
import json
import os
import calendar
import time

# get the values of the following environment variables to provide credentials
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

# Port 9000 inside the MinIO container
ENDPOINT_URL = 'http://172.19.0.2:9000'

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

@persistence_server.route('/create-test-bucket', methods=['POST'])
def create_test_bucket():
    '''

    This creates the bucket that will contain all the directories
    and files of the experiment.

    expected incoming data format:
    {'directory_name': 'default'} or
    {'directory_name': 'test-run-1-13-2020'}

    returns: 
    The name of the bucket that's been created.

    ex: 'test-run-1-13-2020'

    or 

    Returns 'Failed', to indicate that no bucket has been created.

    '''
    
    pickled_request_data = request.data

    # deserialize the request data
    main_directory_config = pickle.loads(pickled_request_data)

    # get the users specified directory name
    directory_name = main_directory_config['directory_name']

    if directory_name == 'default':
        experiment_id = calendar.timegm(time.gmtime())
        directory_name = f'evolf-test-{experiment_id}'

    s3 = get_boto3_object()
    
    try:
        # make sure that the directory name is acceptable
        s3.create_bucket(Bucket=directory_name)
    except:
        try:
            # if it already exists, add a 1 at the end
            directory_name += '1'
            s3.create_bucket(Bucket=directory_name)
        except:
            return "Failed"
    
    return directory_name




if __name__ == '__main__':
    # runs the flask app.

    # turns on debug mode and sets the host IP address of the 
    # app to 0.0.0.0
    persistence_server.run(debug=True, host='0.0.0.0')