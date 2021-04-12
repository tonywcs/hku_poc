function redirect() {
    var input = document.getElementById("dataset").value;
    console.log(input)
    if (input == "custom"){
        window.location.href = 'http://hkusg.herokuapp.com';
    }
    else{
        window.location.href = 'http://hkusg.herokuapp.com/uci';
    }
    return false
}