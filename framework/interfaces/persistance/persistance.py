from framework.interfaces.persistance.persistor import Persistor
from framework.interfaces.persistance.restorer import Restorer


class Persistance(Persistor, Restorer):
    def __init__(self):
        pass

    def persist(self):
        pass

    def restore(self):
        pass
