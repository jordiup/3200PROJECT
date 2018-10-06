function logout() {
    var exitting = confirm("Are you sure you want to logout?");
    if (exitting) {
        var url = location.href;
        var base = url.split('db')[0];
        url = base + "db/logout/";
        location.href = url;
        return true;
    }
    else {
        return false;
    }
}

function mydiscard() {
    var url = location.href;
    var base = url.split('db')[0];
    url = base + "db/upload";
    location.href = url;
    var form = document.getElementById("uploadfield");
    form.method = "GET";
}

function addToDb() {
    var button = document.getElementById("commit-button");
    var add = confirm("Are you sure you want to add this file?");
    if(!add) {
        var form = document.getElementById("input_field");
        form.action = "/db/upload/";
        form.method = "GET";
    }
}