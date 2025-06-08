/******************************/
/* ENDPOINTS BACKEND          */
/******************************/

// const baseUrlAnalise = 'https://naraavila-simetria-molecular.hf.space/api/analise'
// const baseUrlGrupos = 'https://naraavila-simetria-molecular.hf.space/api/grupo/';
// const baseUrlMoleculas = 'https://naraavila-simetria-molecular.hf.space/api/molecula/';

const baseUrlAnalise = 'http://localhost:8000/api/analise'
const baseUrlGrupos = 'http://localhost:8000/api/grupo/';
const baseUrlMoleculas = 'http://localhost:8000/api/molecula/';

/******************************/
/* AÇÃO SELECT GROUP          */
/******************************/
grupoSelect.addEventListener('change', () => {
    const grupoSelecionado = grupoSelect.value;
    if (grupoSelecionado === 'outro') {
        grupoOutput.readOnly = false;
        grupoOutput.value = "";
    } else {
        if (grupoSelecionado) {
            fetch(baseUrlGrupos + grupoSelecionado)
            .then(response => response.ok ? response.json() : Promise.reject('Erro ao carregar o JSON'))
            .then(data => grupoOutput.value = JSON.stringify(data, null, 2))
            .catch(err => grupoOutput.value = err);
            grupoOutput.readOnly = true;   
        } else {
            grupoOutput.value = '';
        }
    }
});


/******************************/
/* AÇÃO SELECT MOLECULE*/
/******************************/
moleculaSelect.addEventListener('change', () => {
    const moleculaSelecionada = moleculaSelect.value;
    if (moleculaSelecionada === 'outro') {
        moleculaOutput.readOnly = false;
        moleculaOutput.value = "";
    } else {
        if (moleculaSelecionada) {
            fetch(baseUrlMoleculas + moleculaSelecionada)
            .then(response => response.ok ? response.text() : Promise.reject('Erro ao carregar o XYZ'))
            .then(data => moleculaOutput.value = data)
            .catch(err => moleculaOutput.value = err);
            moleculaOutput.readOnly = true;
        } else {
            moleculaOutput.value = '';
        }
    }
});

/******************************/
/* AÇÃO BOTÃO ANÁLISE SIMETRIA*/
/******************************/
const analiseBtn = document.getElementById("botaoAnalise");

analiseBtn.addEventListener("click", async () => {
  const formData = new FormData();

      // Pegando os blobs dos campos de texto do grupo e da molécula
  const moleculaBlob = new Blob([document.getElementById("moleculaOutput").value], { type: "text/plain" });
  const grupoBlob = new Blob([document.getElementById("grupoOutput").value], { type: "application/json" });

  formData.append("molecula", moleculaBlob, "molecula.xyz");
  formData.append("grupo", grupoBlob, "grupo.json");

  try {
    const response = await fetch(baseUrlAnalise, {
      method: "POST",
      body: formData,
  });

    if (!response.ok) throw new Error("Erro ao processar a análise");

    const blob = await response.blob();

        // Cria um link temporário para baixar o ZIP
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "resultado.zip";
    a.click();
    window.URL.revokeObjectURL(url);
} catch (err) {
    alert("Erro na análise: " + err.message);
}
});

const renderGrafico = document.querySelector('input[name="renderizacaoGrafica"]:checked').value;
formData.append("render_grafico", renderGrafico);

function trocarRender() {
  const tipo = document.querySelector('input[name="renderTipo"]:checked').value;
  const divTexto = document.getElementById("render-texto");
  const divGrafico = document.getElementById("render-grafico");

  if (tipo === "texto") {
    divTexto.style.display = "block";
    divGrafico.style.display = "none";
  } else {
    divTexto.style.display = "none";
    divGrafico.style.display = "block";

    try {
      const grupoJson = document.getElementById("grupoOutput").value;
      const grupo = JSON.parse(grupoJson);

      const select = document.createElement("select");
      select.id = "select-operacao-unica";
      grupo.operacoes.forEach(op => {
        const option = document.createElement("option");
        option.value = op.id;
        option.textContent = op.comentario || op.nome || `Op ${op.id}`;
        select.appendChild(option);
      });

      const containerSelect = document.getElementById("select-operacoes-container");
      containerSelect.innerHTML = "<h3>Operação a ser Renderizada:</h3>";
      containerSelect.appendChild(select);
    } catch (err) {
      console.warn("Erro ao carregar operações:", err);
      document.getElementById("select-operacoes-container").innerHTML =
        "<p style='color: red'>Erro ao carregar operações. Verifique o JSON do grupo.</p>";
    }
  }
}


// Executa na inicialização da página
document.addEventListener("DOMContentLoaded", trocarRender);

// Excluir depois
function injetarExemplo() {
  const exemplo = {
    "nome": "D3h",
    "ordem": 12,
    "descricao": "Grupo de simetria do etano eclipsado",
    "operacoes": [
      {
        "id": 1,
        "tipo": "identidade",
        "comentario": "Identidade (E)",
        "nome": "\\mathrm{E}"
    },
    {
        "id": 2,
        "tipo": "rotacao",
        "eixo": [0,0,1],
        "angulo": 120,
        "comentario": "Rotação C3 em torno do eixo z (120°)",
        "nome": "\\mathrm{C}_{3}"
    },
    {
        "id": 3,
        "tipo": "rotacao",
        "eixo": [0,0,1],
        "angulo": 240,
        "comentario": "Rotação C3 em torno do eixo z (240°)",
        "nome": "\\mathrm{C}_{3}^{2}"
    },
    {
        "id": 4,
        "tipo": "rotacao",
        "eixo": [1,0,0],
        "angulo": 180,
        "comentario": "Rotação C2(a) em torno do eixo x (180°)",
        "nome": "\\mathrm{C}_{2}^{(a)}"
    },
    {
        "id": 5,
        "tipo": "rotacao",
        "eixo": [-0.5,0.86602540378,0],
        "angulo": 180,
        "comentario": "Rotação C2(b) em torno de eixo no plano xy (180°)",
        "nome": "\\mathrm{C}_{2}^{(b)}"
    },
    {
        "id": 6,
        "tipo": "rotacao",
        "eixo": [-0.5,-0.86602540378,0],
        "angulo": 180,
        "comentario": "Rotação C2(c) em torno de eixo no plano xy (180°)",
        "nome": "\\mathrm{C}_{2}^{(c)}"
    },
    {
        "id": 7,
        "tipo": "reflexao",
        "plano_normal": [0.0,1.0,0.0],
        "comentario": "σv(a) – plano que contém o eixo C–C e H3–H5",
        "nome": "\\sigma_{v1}"
    },
    {
        "id": 8,
        "tipo": "reflexao",
        "plano_normal": [-0.866,-0.5,0.0],
        "comentario": "σv(b) – plano que contém o eixo C–C e H4–H6",
        "nome": "\\sigma_{v2}"
    },
    {
        "id": 9,
        "tipo": "reflexao",
        "plano_normal": [0.866,-0.5,0.0],
        "comentario": "σv(c) – plano que contém o eixo C–C e H5–H7",
        "nome": "\\sigma_{v3}"
    },
    {
        "id": 10,
        "tipo": "reflexao",
        "plano_normal": [0,0,1],
        "comentario": "Reflexão σh no plano xy",
        "nome": "\\sigma_{h}"
    },
    {
        "id": 11,
        "tipo": "impropria",
        "eixo": [0,0,1],
        "angulo": 120,
        "comentario": "Rotação imprópria S3 de 120° (C3 + σh)",
        "nome": "\\mathrm{S}_{3}",
        "plano_normal": [0,0,1]
    },
    {
        "id": 12,
        "tipo": "impropria",
        "eixo": [0,0,1],
        "angulo": 240,
        "comentario": "Rotação imprópria S3 de 240° (C3^2 + σh)",
        "nome": "\\mathrm{S}_{3}^{5}",
        "plano_normal": [0,0,1]
    }
],
"tolerancia": 0.01
};

const grupoOutput = document.getElementById("grupoOutput");
grupoOutput.readOnly = false;
grupoOutput.value = JSON.stringify(exemplo, null, 2);
grupoOutput.readOnly = true;

alert("Grupo D3h injetado com sucesso!");
}
document.addEventListener("DOMContentLoaded", trocarRender);