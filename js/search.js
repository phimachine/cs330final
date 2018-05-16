// function searchClicked(){
//     let searchLocation=document.getElementById('inputLocation').value
//     let searchTerm=document.getElementById('inputTerm').value
//     document.location.href='googlemaps?location='+searchLocation+"&"+"term="+searchTerm
// }

$("#queryForm").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#searchButton").click()
    }
});

$("#queryForm").submit(function(e) {
    e.preventDefault();
    e.returnValue = false;

    // do things
    let searchLocation=document.getElementById('inputLocation').value
    let searchTerm=document.getElementById('inputTerm').value
    document.location.href='googlemaps?location='+searchLocation+"&"+"term="+searchTerm
})
