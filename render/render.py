from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render(self):
        pass