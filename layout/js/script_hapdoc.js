// Função para limpar o status
document.querySelectorAll("#data-table th").forEach((header, index) => {
    header.addEventListener("click", () => {
        const table = document.querySelector("#data-table tbody");
        const rows = Array.from(table.rows);

        // Alterna entre ascendente e descendente
        const isAscending = header.classList.toggle("asc");
        header.classList.toggle("desc", !isAscending);

        // Remove classes de outros cabeçalhos
        document.querySelectorAll("#data-table th").forEach(th => {
            if (th !== header) th.classList.remove("asc", "desc");
        });

        // Ordena as linhas
        rows.sort((a, b) => {
            const aText = a.cells[index].textContent.trim();
            const bText = b.cells[index].textContent.trim();

            return isAscending
                ? aText.localeCompare(bText, undefined, { numeric: true })
                : bText.localeCompare(aText, undefined, { numeric: true });
        });

        // Reinsere as linhas ordenadas
        rows.forEach(row => table.appendChild(row));
    });
});

// função para auxiliar o python
document.getElementById("select-file").addEventListener("click", function () {
    // Simula o clique no input de arquivo
    document.getElementById("file-input").click();
});

document.getElementById("file-input").addEventListener("change", function (event) {
    const file = event.target.files[0]; // Obtém o arquivo selecionado
    if (file) {
        const filePath = file.path; // Caminho completo do arquivo
        console.log("Arquivo selecionado:", filePath);

        // Envia o caminho do arquivo para o Python via PyWebView
        window.pywebview.api.processFile(filePath).then(data => {
            console.log("Dados processados recebidos:", data);
            updateTable(data); // Atualiza a tabela com os dados processados
        }).catch(error => {
            console.error("Erro ao processar o arquivo:", error);
        });
    }
});

// Função para atualizar a tabela com os dados processados
function updateTable(data) {
    const tableBody = document.querySelector("#data-table tbody");
    tableBody.innerHTML = ""; // Limpa a tabela antes de inserir os novos dados

    data.forEach(row => {
        const tr = document.createElement("tr");
        row.forEach(cell => {
            const td = document.createElement("td");
            td.textContent = cell;
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

// Inicializa o QWebChannel para comunicação com o Python
new QWebChannel(qt.webChannelTransport, function (channel) {
    window.api = channel.objects.api;

    document.getElementById("select-file").addEventListener("click", function () {
        // Simula o clique no input de arquivo
        document.getElementById("file-input").click();
    });

    document.getElementById("file-input").addEventListener("change", function (event) {
        const file = event.target.files[0]; // Obtém o arquivo selecionado
        if (file) {
            const filePath = file.path; // Caminho completo do arquivo
            console.log("Arquivo selecionado:", filePath);

            // Envia o caminho do arquivo para o Python
            window.api.processFile(filePath).then(data => {
                console.log("Dados processados recebidos:", data);
                updateTable(data); // Atualiza a tabela com os dados processados
            }).catch(error => {
                console.error("Erro ao processar o arquivo:", error);
            });
        }
    });

    // Função para atualizar a tabela com os dados processados
    function updateTable(data) {
        const tableBody = document.querySelector("#data-table tbody");
        tableBody.innerHTML = ""; // Limpa a tabela antes de inserir os novos dados

        data.forEach(row => {
            const tr = document.createElement("tr");
            row.forEach(cell => {
                const td = document.createElement("td");
                td.textContent = cell;
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }
});