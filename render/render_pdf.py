import subprocess
import os

class PdfReportGenerator(object):
	"""docstring for TextReportGenerator"""
	def __init__(self, arg):
		super(PdfReportGenerator, self).__init__()
		self.arg = arg


		def compilar_latex_para_pdf(self, tex_path: str, output_dir: str) -> str:
			if output_dir is None:
				output_dir = os.path.dirname(tex_path)

			comando = [
			"pdflatex",
			"-interaction=nonstopmode",
			"-output-directory", output_dir,
			tex_path
			]

			result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			if result.returncode != 0:
				raise RuntimeError(f"Erro na compilação do LaTeX:\n{result.stderr.decode()}")

			base = os.path.splitext(os.path.basename(tex_path))[0]
			return os.path.join(output_dir, f"{base}.pdf")