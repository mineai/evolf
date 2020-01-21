import requests
import pickle
import json
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

class PersistenceTester:
    def __init__(self):
        self.url = ""
        self.endpoint_url = ''
        self.minio_access_key = ''
        self.minio_secret_key = ''
        self.boto3_obj = None
        self.bucket_name = ""

    def instantiate_boto3_obj(self):
        '''
            This function creates the boto3 object using various credentials
            to establish a connection to either s3 or MinIO
        '''

        self.boto3_obj = boto3.resource('s3',
                        endpoint_url=self.endpoint_url,
                        aws_access_key_id=self.minio_access_key,
                        aws_secret_access_key=self.minio_secret_key,
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')

    def set_credentials(self):
        '''
            This function takes the credentials held in a file called
            'credentials.json' that you will have to put in this folder.

            credentials.json format: 
            {
                "endpoint_url": "http://localhost:8080",
                "minio_access_key": "YOUR_ACCESS_KEY",
                "minio_secret_key": "YOUR_SECRET_KEY"
            }
        '''
        with open('credentials.json') as json_file:
            credentials = json.load(json_file)
        
        self.endpoint_url = credentials['endpoint_url']
        self.minio_access_key = credentials['minio_access_key']
        self.minio_secret_key = credentials['minio_secret_key']

    def create_test_bucket_test(self):
        print("Create Test Bucket Test:\n")

        default_data = {"directory_name": "default"}
        custom_data = {"directory_name": "test-bucket-1-13-20"}

        self.url = "http://127.0.0.1:9001/create-test-bucket"

        # retrieve the credentials from the json file
        self.set_credentials()

        # instantiate the boto3 object
        self.instantiate_boto3_obj()

        print(f"Default Directory Name: {default_data}\n")

        # pickled_data = pickle.dumps(default_data)

        persistence_app_response = requests.post(self.url, json=default_data)

        status_code = persistence_app_response.status_code

        response_text = persistence_app_response.text

        # set the default bucket name that was created for the user to the class variable bucket_name
        self.bucket_name = response_text

        if status_code == 200:
            print("Passed!\n")
            print(f"Response: {response_text}\n\n")
        else:
            print(f"Failed with a {status_code} status code.\n")
            print(f"Response: {response_text}\n\n")

        print(f"Custom Directory Name: {custom_data}\n")

        # pickled_data = pickle.dumps(custom_data)

        persistence_app_response = requests.post(self.url, json=custom_data)

        status_code = persistence_app_response.status_code

        response_text = persistence_app_response.text

        if status_code == 200:
            print("Passed!\n")
            print(f"Response: {response_text}\n\n")
        else:
            print(f"Failed with a {status_code} status code.\n")
            print(f"Response: {response_text}\n\n")

    def file_upload_test(self):
        print("Upload File Test:\n")

        post_request_data = {
            "file_info": {
                "bucket_name": self.bucket_name,
                "generation_number": "0",
                "tree_number": "25"
            },
            "persistence_config": {
                "tree_stats": True,
                "tree_visualize": False,
                "tree_graph": True,
                "avg_fitness_graph": False,
                "best_fitness_graph": True
            }
        }

        self.url = "http://localhost:9001/test-file-upload"

        # retrieve the credentials from the json file
        self.set_credentials()

        # instantiate the boto3 object
        self.instantiate_boto3_obj()

        print(f"File Upload Job Config: {post_request_data}\n")

        # pickled_data = pickle.dumps(post_request_data)

        persistence_app_response = requests.post(self.url, json=post_request_data)

        status_code = persistence_app_response.status_code

        response_text = persistence_app_response.text

        if status_code == 200:
            print("Passed!\n")
            print(f"Response: {response_text}\n\n")
        else:
            print(f"Failed with a {status_code} status code.\n")
            print(f"Response: {response_text}\n\n")
    
    def persist_population_test(self):
        self.url = "http://localhost:9001/persist/population"

        print("Persist Population Test:\n")

        test = {"name": "Alex Jirovsky"}

        persistence_app_response = requests.post(self.url, json=test)

        status_code = persistence_app_response.status_code

        response_text = persistence_app_response.text

        if status_code == 200:
            print("Passed!\n")
            print(f"Response: {response_text}\n\n")
        else:
            print(f"Failed with a {status_code} status code.\n")
            print(f"Response: {response_text}\n\n")


test_obj = PersistenceTester()
test_obj.create_test_bucket_test()
test_obj.file_upload_test()
test_obj.persist_population_test()
