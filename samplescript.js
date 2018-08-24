//Search menu function (Homelogin.html and FindProject.html)
function searchmenu(x) {
    var table,input, filter, tr, td, i;
    //x is an indicator, 0 is search input from Homelogin.html
    //and 1 is from Findproject.html
    if(!x){
        input = document.getElementById("searchhome");
        table = document.getElementById("project-table");
    }
    else{
        input = document.getElementById("search1");
        table = document.getElementById("findproject");
    }
    filter = input.value.toUpperCase();
    tr = table.getElementsByTagName("tr");

    //Scan through each row until the wanted project is found
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            }
            //Will display nothing if not found
            else {
                tr[i].style.display = "none";
            }
        }       
    }
}

//Sort table ascending or descending (on Projectdetails page)
function tablesort(tnumber,n) {
    var table, row, indicator, i, curval,newval, swap, method, swapamount = 0;
    
    //if tnumber is 0, it sorts member table
    if (!tnumber){
        table = document.getElementById("mymember");
    }
    //if tnumber is 1, it sorts task table
    else{
        table = document.getElementById("mytask");
    }

    //Indicate if sorting is necessary
    indicator = true;
    //Set the sorting direction to ascending:
    method = "asc"; 

    //switch each position until everything is sorted in ascending or descending
    while (indicator) {
        row = table.getElementsByTagName("tr");
        //Assume no sorting is done yet
        indicator = false;

        for (i = 1; i < (row.length - 1); i++) {
            curval = row[i].getElementsByTagName("td")[n];
            newval = row[i+1].getElementsByTagName("td")[n];
            //Assume no value should be swap
            swap = false;

            if (method == "asc") {
                if (curval.innerHTML.toLowerCase() > newval.innerHTML.toLowerCase()) {
                //Note that it must be swap
                swap= true;
                break;
                }
            } else if (method == "desc") {
                if (curval.innerHTML.toLowerCase() < newval.innerHTML.toLowerCase()) {
                //Note that it must be swap
                swap= true;
                break;
                }
            }
        }
        
        //Swap the two values positions
        if (swap) {
            row[i].parentNode.insertBefore(row[i + 1], row[i]);
            indicator = true;
            swapamount++;      
        } 
        //Check if there is any swap that occurs
        else {
            if (swapamount == 0 && method == "asc") {
                method = "desc";
                indicator = true;
            }
        }
    }    
}

//Dynamic adding of project list
function DisplayNewProject(currproject) {
    var mytable = document.getElementById("project-table");
    var x = mytable.rows.length;
    var row = mytable.insertRow(x);

    //Insert new rows
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);

    //Insert new values
    cell1.innerHTML = currproject.name;
    cell2.innerHTML = currproject.field;
    cell3.innerHTML = currproject.location;
    cell4.innerHTML = currproject.description;
    cell5.innerHTML = currproject.startdate;

    var newview = document.createElement("a");
    newview.href="Projectdetails";
    var txt = document.createTextNode("View");
    newview.className = "view";
    newview.appendChild(txt);
    cell6.appendChild(newview);
}