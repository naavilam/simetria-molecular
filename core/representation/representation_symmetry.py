from representation.representation import Representation
from typing import List
from core.core_symmetry_operation import SymmetryOperation

class SymmetryRepresentation(Representation):
    """
    Representação no domínio das próprias operações de simetria.

    Permite realizar composição, inverso e conjugação diretamente entre as operações
    definidas no conjunto, usando os índices como referência (base-1).
    """

    def __init__(self, operacoes: List[SymmetryOperation]):
        super().__init__()
        self.operacoes = operacoes

    def compor(self, a: int, b: int) -> int:
        op_a = self.operacoes[a - 1]
        op_b = self.operacoes[b - 1]
        resultado = op_b.compose(op_a)  # b ∘ a

        return self._buscar_indice(resultado)

    def inverso(self, a: int) -> int:
        op_a = self.operacoes[a - 1]
        resultado = op_a.inverse()
        return self._buscar_indice(resultado)

    def conjugar(self, a: int, b: int) -> int:
        inv_b = self.inverso(b)
        return self.compor(self.compor(b, a), inv_b)

    def _buscar_indice(self, op_resultado: SymmetryOperation) -> int:
        """Summary

        Raises:
            ValueError: Description
        """
        for idx, op in enumerate(self.operacoes):
            if op.equals(op_resultado):
                return idx + 1
        raise ValueError("[SymmetryOperationSet] Operação resultante não encontrada no conjunto.")


        class SymmetryOperation:
    """
    Representa uma operação de simetria individual.

    Pode ser identidade, rotação, reflexão, inversão ou rotação imprópria.
    """

    def __init__(self, tipo: str, matriz: np.ndarray, nome: str = "", id: int = None):
        """
        Args:
            tipo (str): Tipo da operação (ex: 'identidade', 'rotacao', 'reflexao', etc)
            matriz (np.ndarray): Matriz 3x3 representando a operação espacial.
            nome (str, opcional): Nome simbólico (ex: '\\mathrm{C}_3').
            id (int, opcional): ID da operação no grupo.
        """
        self.tipo = tipo
        self.matriz = matriz
        self.nome = nome
        self.id = id

    def compose(self, other: 'SymmetryOperation') -> 'SymmetryOperation':
        """
        Retorna o resultado da composição: this ∘ other (ou seja: this após other).

        Args:
            other (SymmetryOperation): A operação a ser aplicada antes.

        Returns:
            SymmetryOperation: Nova operação resultante.
        """
        nova_matriz = np.dot(self.matriz, other.matriz)
        return SymmetryOperation(tipo="composta", matriz=nova_matriz, nome=f"({self.nome})∘({other.nome})")

    def inverse(self) -> 'SymmetryOperation':
        """
        Retorna a operação inversa desta.

        Returns:
            SymmetryOperation: Operação inversa.
        """
        inv_matriz = np.linalg.inv(self.matriz)
        return SymmetryOperation(tipo=f"inverso_{self.tipo}", matriz=inv_matriz, nome=f"{self.nome}⁻¹")

    def equals(self, other: 'SymmetryOperation', tol: float = 1e-6) -> bool:
        """
        Testa se duas operações são iguais (matriz por matriz).

        Args:
            other (SymmetryOperation): Outra operação a comparar.
            tol (float): Tolerância numérica.

        Returns:
            bool: True se forem estruturalmente iguais.
        """
        return np.allclose(self.matriz, other.matriz, atol=tol)

    def __repr__(self):
        """Summary
        """
        return f"SymmetryOperation(tipo='{self.tipo}', nome='{self.nome}', id={self.id})"