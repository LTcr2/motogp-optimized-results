"use strict";


//Show results about Rider based on Rider and Venue selected

function updateResults(results) {
    if (results.code === "OK") {
        $('#rider-results').html("<p>" + results.msg + "</p>");
    }
    else {
        $('#rider-results').addClass("order-error");
        $('#rider-results').html("<p><b>" + results.msg + "</b></p>");
    }
}

function showResults(evt) {
    evt.preventDefault();

    let formInputs = {
        "competitor_name": $("#competitor_name_field").val(),
        "venue_description": $("#venue_name_field").val()
    };

    $.post("/rider_results.json", formInputs, updateResults);
}

$("#results-form").on('submit', showResults);


function updateYoutubeResults(results) {
    if (results.code === "OK") {
        $('#youtube-results').html("<p>" + link + "</p>");
    }
    else {
        $('#youtube-results').addClass("order-error");
        $('#youtube-results').html("<p><b>" + "uh oh" + "</b></p>");
    }
}

function showYoutubeResults(evt) {
    evt.preventDefault():

    let YTformInputs = {
        "competitor_name": $("#competitor_name_field").val(),
        "venue_description": $("#venue_name_field").val()
        "sort_by": $("#sort_by_field").val(),
        "num_results": $("#num_results_field").val()
    }
    $.post("/youtube_results.json", YTformInputs, updateYoutubeResults)
}







