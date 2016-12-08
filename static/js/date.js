/**
 * Created by ZachBluhm on 12/7/16.
 */
var d = new Date();
var monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];

var date = document.getElementById("date");
var time = document.getElementById("time");

function getDate() {
    date.innerHTML = monthNames[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear();
}

function timer() {
    setTimeout(timer, 1000);
    var d1 = new Date();
    var d = new Date(d1.getUTCFullYear(), d1.getUTCMonth(), d1.getUTCDate(), d1.getUTCHours(), d1.getUTCMinutes(), d1.getUTCSeconds())
    var hours = d.getHours();
    var minutes = d.getMinutes();
    var ampm = hours <= 11 ? 'am' : 'pm';
    time.innerHTML = [hours % 12,
            (minutes < 10 ? "0" + minutes : minutes)
        ].join(':') + ampm;
    setTimeout(timer, 10000);
}

getDate();
timer();