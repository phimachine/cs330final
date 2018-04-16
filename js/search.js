var searchLocation="San Bernadino"
var searchTerm="dinner"

function searchClicked(){

    searchLocation=document.getElementById('inputLocation').value
    searchTerm=document.getElementById('inputTerm').value
    $(window).attr('location',"/googlemaps")
}