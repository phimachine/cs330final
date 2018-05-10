var googleMapsAPI

function readSingleFile(e) {
    var file = e.target.files[0]
    if (!file) {
        return
    }
    var reader = new FileReader()
    reader.onload = function(e) {
        googleMapsAPI=e.target.result
        displayContents(googleMapsAPI)
    };
    reader.readAsText(file)
    return googleMapsAPI
}

function readGoogleAPI(e){
    let APIKey=readSingleFile(e)
    print('init')
    initMap(APIKey)
}

function displayContents(contents) {
    var element = document.getElementById('file-content')
    element.textContent = contents
}

window.onload=()=>{
    document.getElementById('google-api')
    .addEventListener('change', readGoogleAPI, false)
}