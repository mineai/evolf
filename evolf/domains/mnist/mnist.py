
from evolf.domains.mnist.get_mnist_data import GetMnistData
from evolf.domains.mnist.mnist_network_constructor import MnistNetworkConstructor
from evolf.evolution.session_server import SessionServer

if __name__ == "__main__":
    session_server = SessionServer(MnistNetworkConstructor, GetMnistData)
    session_server.run()


