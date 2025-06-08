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
        alert("here")
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

const grupoOutput = document.getElementById("grupoOutput");
grupoOutput.readOnly = false;
grupoOutput.value = JSON.stringify(exemplo, null, 2);
grupoOutput.readOnly = true;

alert("Grupo D3h injetado com sucesso!");
}
document.addEventListener("DOMContentLoaded", trocarRender);