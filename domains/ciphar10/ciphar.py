
from domains.ciphar10.ciphar_network_constructor import CipharNetworkConstructor
from domains.ciphar10.get_ciphar_data import GetCipharDataDict
from evolution.session_server import SessionServer

if __name__ == "__main__":
    session_server = SessionServer(CipharNetworkConstructor, GetCipharDataDict)
    session_server.run()
