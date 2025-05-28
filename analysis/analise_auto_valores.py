from representation.representation_interface import Representation

class AutoValores(object):

    def __init__(self, representation: Representation):
        self.rep = representation
        self.tabela = {}