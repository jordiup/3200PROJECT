function logout(){
    var exitting = confirm("Are you sure you want to logout?");
    if(exitting){
        var url = location.href;
        var base = url.split('db')[0];
        url = base + "db/logout/";
        location.href = url;
        return true;
    }
    else{
        return false;
    }
}