from abc import ABC, abstractmethod
from typing import Dict
from engine_analyser.symmetry_analyzer import SymmetryAnalyzer

class ExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, analyzer: SymmetryAnalyzer) -> dict:
        """Summary
        """
        pass

class LowScoreStrategy(ExecutionStrategy):
    def execute(self, analyzer: SymmetryAnalyzer) -> dict:
        """Summary
        """
        return (
            analyzer
            .qual_grupo()
            .permutacoes()
            .results()
        )

class MediumScoreStrategy(ExecutionStrategy):
    def execute(self, analyzer: SymmetryAnalyzer) -> dict:
        return (
            analyzer
            .qual_grupo()
            .permutacoes()
            .tabela_multiplicacao()
            .results()
        )

class HighScoreStrategy(ExecutionStrategy):
    def execute(self, analyzer: SymmetryAnalyzer) -> dict:
        return (
            analyzer
            .qual_grupo()
            .permutacoes()
            .tabela_multiplicacao()
            .classes_conjugacao()
            .tabela_caracteres()
            .results()
        )

def select_strategy(score: int) -> ExecutionStrategy:
    """Summary
    """
    if score <= 10:
        return LowScoreStrategy()
    elif score <= 1000:
        return MediumScoreStrategy()
    else:
        return HighScoreStrategy()

def calculate_score(flags: dict) -> int:
    """
    Calcula o score total com base nas análises escolhidas pelo usuário.
    """
    score_map = {
        "grupo": 1,
        "permutacao": 10,
        "tabela_multiplicacao": 100,
        "tabela_conjugacao": 1000,
        "tabela_caracteres": 10000,
    }

    total_score = sum(
        score_map.get(key, 0) for key, value in flags.items() if value
    )

    return total_score