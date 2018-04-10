function readSingleFile(e) {
    var file = e.target.files[0];
    if (!file) {
        return;
    }
    var reader = new FileReader();
    reader.onload = function(e) {
        var content = e.target.result;
        displayContents(content);
    };
    reader.readAsText(file);
    console.log("read api")
    return content
}

function readGoogleAPI(e){
    let APIKey=readSingleFile(e)
    initMap(APIKey)
}

function displayContents(contents) {
    var element = document.getElementById('file-content');
    element.textContent = contents;
}

document.getElementById('file-input')
    .addEventListener('change', readSingleFile, false);