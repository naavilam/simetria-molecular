from .render import Renderer
import subprocess
import os

class PdfReportGenerator(Renderer):

    def __init__(self, metadata, resultado):
        self.metadata = metadata
        self.resultado = resultado

    def render(self) -> str:
        return "0"