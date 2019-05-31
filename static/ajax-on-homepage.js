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
