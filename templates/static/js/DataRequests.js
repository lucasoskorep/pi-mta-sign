$(document).ready(function () {

    const interval = setInterval(function () {
        updateData($('#station_1'))
        updateData($('#station_2'))
    }, 5000);

    function updateData(station) {

        $.ajax({
            type: "POST",
            //the url where you want to sent the userName and password to
            url: '/mta_data',
            contentType: "application/json",
            dataType: "json",
            async: true,
            //json object to sent to the authentication url
            data: JSON.stringify({"station": station.find('.station-name:first').get(0).innerText}, null, '\t'),
            success: function (data, text) {
                // console.log(data)
                updateStation(station, data)
            },
            error: function (request, status, error) {
                alert(request.responseText);
            }
        });
    }

    function updateStation(station, data) {
        //get first item
        updateDirections(station, data, "North");
        updateDirections(station, data, "South");
    }

    function updateDirections(station, data, direction) {
        // console.log(direction)
        // console.log(".card:".concat(direction === "North" ? "first" : "last"))
        n = data[direction]
        // console.log(data[direction])
        list_items = station.find(".card:".concat(direction === "North" ? "first" : "last")).find(".station-info")
        var i = 0;
        for (var train in n) {
            // console.log(train)
            // console.log(list_items)
            updateLineItem(list_items.get(i), n[train], train)
            i = i + 1
        }
    }

    function updateLineItem(listItem, times, train) {
        // console.log(times)
        $(listItem).find("img").attr("src", "/static/images/lines/" + train + ".svg")
        $(listItem).find("h1").text(times.sort(function (a, b) {
            return a - b;
        }).join(", "));
    }
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