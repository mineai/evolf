import os
import sys

sys.path.append(os.getcwd())

from domains.mnist.get_mnist_data import GetMnistData
from domains.mnist.mnist_network_constructor import MnistNetworkConstructor
from evolution.session_server import SessionServer
from servicecommon.persistor.local.json.json_persistor import JsonPersistor

config_path = os.path.join(os.getcwd(), "temp/config")
json_persistor = JsonPersistor(base_file_name="config", folder=config_path)
config = json_persistor.restore()

session_server = SessionServer(MnistNetworkConstructor, GetMnistData, config)
session_server.run()
