from representation.representation_interface import Representation

class Abeliano(object):

    def __init__(self, representation: Representation):
        self.rep = representation
        self.tabela = {}