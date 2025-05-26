# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM continuumio/miniconda3

# Ainda como root
WORKDIR /app
COPY ./requirements.txt requirements.txt

# Instale tudo antes de trocar para o usuário comum
RUN conda install -y -c conda-forge vtk pyvista fastapi uvicorn numpy scipy

# Agora sim, crie o usuário
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copie o código com permissões corretas
COPY --chown=user . /app

# Rode o servidor
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]