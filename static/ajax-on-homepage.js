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
    $('#youtube-results').html("<p>" + results.items[0].id.videoId + "</p>");
   
}

function showYoutubeResults(evt) {
    console.log('I HAVE BEEN CALLED')
    evt.preventDefault();

    let YTformInputs = {
        "competitor_name": $("#competitor_name_field").val()
    }
    $.post("/youtube_results.json", YTformInputs, updateYoutubeResults)
}

$("#video-form").on('submit', showYoutubeResults)






