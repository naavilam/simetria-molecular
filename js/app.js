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
    alert("here")
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
    alert("here")
    const moleculaSelecionada = moleculaSelect.value;
    if (moleculaSelecionada === 'outro') {
        moleculaOutput.readOnly = false;
        moleculaOutput.value = "";
    } else {
        alert("here")
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
  const container = document.getElementById("renderOpcoes");

  if (tipo === "texto") {
    container.innerHTML = `

      <h3>Análises Desejadas:</h3>
      <label><input type="checkbox" name="analises" value="grupo" checked>Identificação do Grupo de Simetria</label><br>
      <label><input type="checkbox" name="analises" value="permutacoes" checked> Permutações</label><br>
      <label><input type="checkbox" name="analises" value="tabela_multiplicacao"> Tabela de multiplicação</label><br>
      <label><input type="checkbox" name="analises" value="classes_conjugacao"> Classes de conjugação</label><br>
      <label><input type="checkbox" name="analises" value="representacao_caracteres" disabled> Representação por caracteres (Em breve)</label><br>
      <label><input type="checkbox" name="analises" value="autovalores" disabled> Autovalores das operações (Em breve)</label><br>
      <label><input type="checkbox" name="analises" value="subgrupos" disabled> Subgrupos (Em breve)</label><br>
      <label><input type="checkbox" name="analises" value="ciclico" disabled> Cíclico (Em breve)</label><br>
      <label><input type="checkbox" name="analises" value="abeliano" disabled> Abeliano (Em breve)</label><br>

      <h3>Formato de Saída:</h3>
      <label><input type="radio" name="formatoTexto" value="latex" checked> LaTeX</label><br>
      <label><input type="radio" name="formatoTexto" value="txt"> Texto Puro</label><br>

        `;
    } else {
        container.innerHTML = `

    <div class="container">
        <label for="grupo">Escolha o Grupo de Simetria</label>
        <select id="grupoSelect">
            <option value="">Selecione um grupo ...</option>
            <optgroup label="Cristalográficos (Hexagonal)">
                <option value="cristalograficos/Hexagonal/C3h">C3h</option>
                <option value="cristalograficos/Hexagonal/C6">C6</option>
                <option value="cristalograficos/Hexagonal/C6h">C6h</option>
                <option value="cristalograficos/Hexagonal/C6v">C6v</option>
                <option value="cristalograficos/Hexagonal/D3h">D3h</option>
                <option value="cristalograficos/Hexagonal/D6">D6</option>
                <option value="cristalograficos/Hexagonal/D6h">D6h</option>
            </optgroup>
            <optgroup label="Cristalográficos (Monoclinico)">
                <option value="cristalograficos/Monoclinico/C2">C2</option>
                <option value="cristalograficos/Monoclinico/C2h">C2h</option>
                <option value="cristalograficos/Monoclinico/Cs">Cs</option>
            </optgroup>
            <optgroup label="Cristalográficos (Ortorrombico)">
                <option value="cristalograficos/Ortorrombico/C2v">C2v</option>
                <option value="cristalograficos/Ortorrombico/D2">D2</option>
                <option value="cristalograficos/Ortorrombico/D2h">D2h</option>
            </optgroup>
            <optgroup label="Cristalográficos (Tetragonal)">
                <option value="cristalograficos/Tetragonal/C4">C4</option>
                <option value="cristalograficos/Tetragonal/C4h">C4h</option>
                <option value="cristalograficos/Tetragonal/C4v">C4v</option>
                <option value="cristalograficos/Tetragonal/D2d">D2d</option>
                <option value="cristalograficos/Tetragonal/D4">D4</option>
                <option value="cristalograficos/Tetragonal/D4h">D4h</option>
                <option value="cristalograficos/Tetragonal/S4">S4</option>
            </optgroup>
            <optgroup label="Cristalográficos (Triclinico)">
                <option value="cristalograficos/Triclinico/C1">C1</option>
                <option value="cristalograficos/Triclinico/Ci">Ci</option>
            </optgroup>
            <optgroup label="Cristalográficos (Trigonal)">
                <option value="cristalograficos/Trigonal/C3">C3</option>
                <option value="cristalograficos/Trigonal/C3v">C3v</option>
                <option value="cristalograficos/Trigonal/D3">D3</option>
                <option value="cristalograficos/Trigonal/D3d">D3d</option>
                <option value="cristalograficos/Trigonal/S6">S6</option>
            </optgroup>
            <optgroup label="Moleculares">
                <option value="moleculares/C3v">C3v</option>
                <option value="moleculares/C4h">C4h</option>
                <option value="moleculares/C5">C5</option>
                <option value="moleculares/C5h">C5h</option>
                <option value="moleculares/C5v">C5v</option>
                <option value="moleculares/Cinfv">C∞v</option>
                <option value="moleculares/Dinfh">D∞h</option>
                <option value="moleculares/D3d">D3d</option>
                <option value="moleculares/D5">D5</option>
                <option value="moleculares/D5h">D5h</option>
                <option value="moleculares/I">I</option>
                <option value="moleculares/Ih">Ih</option>
                <option value="moleculares/S8">S8</option>
                <option value="outro">Outro (especifique)</option>
            </optgroup>
        </select>
        <textarea id="grupoOutput" placeholder="Json do grupo ..."></textarea>
        </div>

         <div id="select-operacoes-container">
            <h3>Operação a ser Renderizada:</h3>
            <select id="select-operacao-unica">
              <option>Carregando operações...</option>
            </select>
          </div>

          <h3>Paleta de Cores:</h3>
          <label><input type="radio" name="paletaCores" value="PASTEL" checked> 🎨 Pastel</label><br>
          <label><input type="radio" name="paletaCores" value="VIBRANTE"> 🌈 Vibrante</label><br>
          <label><input type="radio" name="paletaCores" value="MONOCROMATICA"> 🩶 Monocromática</label>

          <h3>Formato Gráfico:</h3>
          <label><input type="radio" name="formatoGrafico" value="gif" checked> GIF</label><br>
          <label><input type="radio" name="formatoGrafico" value="3d"> 3D Interativo</label><br>

        `
        ;

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