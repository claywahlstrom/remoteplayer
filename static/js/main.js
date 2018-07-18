
var td = new Timedelta(0);

function startTimer(length) {
    doSomething(0, length);
}

function doSomething(now, length) {
    if (now > length) { // base case
        $("input[name=next]").click();
        return;
    }
    td.distance = now;
    console.log("td.distance = " + td.distance);
    document.getElementById("timeprogressed").innerHTML = td.toString();
    setTimeout(function() { doSomething(now + 1000, length) }, 1000);
}

function sendVideo() {
    // need to jsonify and send to background process
    $.getJSON('/background_process', {
        url: $("#url").val(),
    }, function(response) {
        console.log(response.title);
        if (document.getElementById("upnext").innerHTML == "none") {
            document.getElementById("upnext").innerHTML = response.title;
        }
        $("#url").val("");
    })
}

function bindToSubmit() {
    $("#submit").bind("click", function() {
        sendVideo();
        return false;
    });
}

function setButton() {
    if (document.getElementById("currenttitle").innerHTML == "none") {
        $("#submit").prop({type: "submit"});
        $("#submit").unbind("click")
    } else {
        $("#submit").prop({type: "button"});
        bindToSubmit();
    }
}