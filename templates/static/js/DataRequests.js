$(document).ready(function () {

    function clearCanvas() {
        var canvas = document.getElementById("inputCanvas");
        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    function getData() {
        $.ajax({
            type: "POST",
            //the url where you want to sent the userName and password to
            url: '/mta_data',
            contentType: "application/json",
            dataType: "json",
            async: true,
            //json object to sent to the authentication url
            data: JSON.stringify({"test_dict":"test_value"}, null, '\t'),

            success: function (data, text) {
                $("#result").text(JSON.stringify(data));
            },
            error: function (request, status, error) {
                alert(request.responseText);
            }
        });
    }

    $("#test_button").click(function () {
        getData();
    });

});