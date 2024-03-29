$(document).ready(function () {

    function updateStationData(station) {
        $.ajax({
            type: "POST",
            url: '/mta_data',
            contentType: "application/json",
            dataType: "json",
            async: true,
            data: JSON.stringify({"station": station.find('.station-name:first').get(0).innerText}, null, '\t'),
            success: function (data) {
                updateStation(station, data)
            },
            error: function (request) {
                console.log(request.responseText);
            }
        });
    }
    function updateStartTime() {
        $.ajax({
            type: "get",
            url: '/start_time',
            async: true,
            success: function (data) {
                console.log("GETTING TIME")
                console.log(data);
                $("#start_time").text(data)
            },
            error: function (request) {
                console.log(request.responseText);
            }
        });
    }

    function updateStation(station, data) {
        updateDirections(station, data, "North");
        updateDirections(station, data, "South");
        updateTime(data["LastUpdated"])
    }

    function updateTime(lastUpdated) {
        console.log(lastUpdated)
        $("#last_updated").text(lastUpdated)
    }

    function updateDirections(station, data, direction) {
        n = data[direction]
        list_items = station.find(".card:".concat(direction === "North" ? "first" : "last")).find(".station-info")
        var i = 0;
        for (var train in n) {
            updateLineItem(list_items.get(i), n[train], train)
            i = i + 1
        }
        if (i < 3) {
            console.log("Only 2 items updated")
            for (let remainingIndex = i; remainingIndex < 3; remainingIndex++) {
                updateLineItem(list_items.get(i), "No Trains Available", "N/A")
            }
        }
    }

    function updateLineItem(listItem, times, train) {
        var timeString;
        if (typeof times === 'string' || times instanceof String) {
            timeString = times;
        } else {
            timeString = times.sort(function (a, b) {
                return a - b;
            }).join(", ");
        }
        $(listItem).find("h1").text(timeString);
        if (imageExists("/static/images/lines/" + train + ".svg")) {

            $(listItem).show()
            $(listItem).find("img").attr("src", "/static/images/lines/" + train + ".svg")
        } else if (train === "N/A") {
            console.log("Route Is NA - Disabling Route")
            console.log($(listItem))
            $(listItem).hide()
        }
    }

    function imageExists(image_url) {
        var http = new XMLHttpRequest();
        http.open('HEAD', image_url, false);
        http.send();
        return http.status != 404;

    }

    const interval = setInterval(function () {
        updateStationData($('#station_1'))
    }, 5000);
    const interval2 = setInterval(function () {
        updateStationData($('#station_2'))
    }, 6000);
    updateStartTime();


});

function setStation(ele) {
    console.log(ele)
    console.log($(ele).text())
    var stop_name = ele.text;

    $.ajax({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/get_stop_id',
        contentType: "application/json",
        dataType: "json",
        async: true,
        //json object to sent to the authentication url
        data: JSON.stringify({"stop_name": stop_name}, null, '\t'),
        success: function (data, text) {
            alert(JSON.stringify(data));
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }
    });
}