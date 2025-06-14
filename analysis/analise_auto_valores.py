from representation.representation_interface import Representation
from analysis.analise import Analise

class AutoValores(Analise):

    def __init__(self, representation: Representation):
        self.rep = representation
        self.tabela = {}