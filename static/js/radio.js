$(document).ready(function(){

    $('#map').css('display', 'none');

    var radios = document.forms["Trends"].elements["Trend"];

    for(var i = 0, max = radios.length; i < max; i++) {
        radios[i].onclick = function() {
            if (this.value === "Sunburst") {
                $("#sun-burst").fadeIn(700);
                $("#map").fadeOut(700);
            } else {
                $("#map").fadeIn(700);
                $("#sun-burst").fadeOut(700);
            }
        }
    }

});