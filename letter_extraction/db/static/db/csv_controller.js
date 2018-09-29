function download_csv(csv, filename) {
    var csvFile;
    var downloadLink;
    csvFile = new Blob([csv], { type: "text/csv" });
    downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
}

function export_table_to_csv(html, filename) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");

    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");

        for (var j = 0; j < cols.length; j++) {
            var text = cols[j].innerText;
            var edited = text.replace(/,/g, ";");
            row.push(edited);
        }

        csv.push(row);
    }
    download_csv(csv.join("\n"), filename);
}

function to_csv() {
    var html = document.querySelector(".results_table").outerHTML;
    export_table_to_csv(html, "result_table.csv")
}