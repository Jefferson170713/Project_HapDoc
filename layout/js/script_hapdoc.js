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

document.getElementById("menu-clinic").addEventListener("click", function (event) {
    event.preventDefault(); // Evita o comportamento padrão do botão

    const submenu = document.getElementById("clinic-options");

    // Alterna a classe "show" para exibir ou ocultar o submenu
    submenu.classList.toggle("show");
});