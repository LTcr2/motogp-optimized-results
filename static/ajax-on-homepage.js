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

function createYoutubeVideoWith(results) {

    let videoId = results.items[0].id.videoId
    let youtubeUrl = "https://www.youtube.com/embed/" + videoId

    // $('#youtube-results').html("<p>" + results + "</p>");

    //This SHOULD work when your daily limit is reset.
    $('#youtube-results').html("<iframe src=" + youtubeUrl + "width=\"560\" height=\"315\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen><iframe>");  
}


function showResults(evt) {
    evt.preventDefault();

    let formInputs = {
        "competitor_name": $("#competitor_name_field").val(),
        "venue_description": $("#venue_name_field").val(),
    };

    let YTformInputs = {
        "competitor_name": $("#competitor_name_field").val(),
        "venue_description": $("#venue_name_field").val(),
        "num_results": $("#num_results_field").val(),
        "sort_by": $("#sort_by_field").val()
    }

    $.post("/rider_results.json", formInputs, updateResults);
    $.post("/youtube_results.json", YTformInputs, createYoutubeVideoWith)
}

$("#results-form").on('submit', showResults);







