<<<<<<< HEAD
import argparse
from evolf.domains.mnist.generate_mnist_data import GenerateMnistData
from evolf.domains.mnist.network_constructor import NetworkConstructor
=======

from evolf.domains.mnist.get_mnist_data import GetMnistData
from evolf.domains.mnist.mnist_network_constructor import MnistNetworkConstructor
>>>>>>> 2b4ac31f582bd602a247916d08053d4e924117e0
from evolf.evolution.session_server import SessionServer

if __name__ == "__main__":
    session_server = SessionServer(MnistNetworkConstructor, GetMnistData)
    session_server.run()


