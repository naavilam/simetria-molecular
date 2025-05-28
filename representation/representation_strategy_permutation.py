class PermutationRepresentationStrategy(RepresentationStrategy):
    """Estratégia de construção de representação como permutações (1D)."""

    def construir(self, group: 'Group', molecule: 'Molecule') -> Representation:
        representation = Representation(group.nome)
        for operacao in group.operacoes:
            nome = operacao.nome
            matriz = operacao.matriz()
            mol_transformada = matriz @ molecule  # operador @ implementado na classe Molecule
            permutacao = Permutation.from_coords(molecule, mol_transformada, tol=group.tolerancia)
            representation.adicionar(nome, permutacao.indices)
        return representation
