import os
import sys

sys.path.append(os.getcwd())

from domains.mnist.get_mnist_data import GetMnistData
from domains.mnist.mnist_network_constructor import MnistNetworkConstructor
from evolution.session_server import SessionServer

session_server = SessionServer(MnistNetworkConstructor, GetMnistData)
session_server.run()
