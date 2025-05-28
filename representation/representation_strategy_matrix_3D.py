class Matrix3DRepresentationStrategy(RepresentationStrategy):
    """
    Implementa a estratégia de representação matricial 3D (rotacional) para cada operação do grupo.
    """
    def construir(self, group: 'GroupSymmetry', molecule: 'Molecule') -> Representation:
        representation = Representation(group.nome)
        for operacao in group.operacoes:
            nome = operacao.nome
            matriz = operacao.matriz()
            representation.adicionar(nome, matriz)
        return representation