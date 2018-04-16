function searchClicked(){
    let searchLocation=document.getElementById('inputLocation').value
    let searchTerm=document.getElementById('inputTerm').value
    document.location.href='googlemaps?location='+searchLocation+"&"+"term="+searchTerm
}

// $(window).keyup(function(event) {
//     if (event.keyCode === 13) {
//         $("#searchButton").click();
//     }
// });