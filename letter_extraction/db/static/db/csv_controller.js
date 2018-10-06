function downloadCsv(csv, filename) {
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

function exportTableToCsv(html, filename) {
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
    downloadCsv(csv.join("\n"), filename);
}

function toCsv() {
    var table = document.querySelector(".results_table");
    if (table == null) alert("Cannot download an empty result set!");
    var html = table.outerHTML;
    exportTableToCsv(html, "result_table.csv")
}

function backToSearch() {
    var exitting = confirm("Are you sure you want to go back?");
    if (exitting) {
        var url = location.href;
        var base = url.split('db')[0];
        url = base + "db/search/";
        location.href = url;
        return true;
    }
    else {
        return false;
    }
}

function modify_function() {
    var enumeration = document.getElementById("holder").getElementsByTagName("TD")
    var archive_number = enumeration[4]
    document.getElementById("tester").value = archive_number
}


