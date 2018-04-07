function getLocation(){
    console.log("getting a video information")
    let config={}
    config.method="GET"
    config.header={'Content-Type':'application/json','Accept':'application/json'}

    let get_string="https://www.googleapis.com/youtube/v3/videos?id=AWWG-Wwo9AY&key=AIzaSyCKCdWFx6SW6I0hFaobMpAhE4IMJyOh8ec&part=recordingDetails"

    let answer=fetch(get_string,config)
    .then(function(response){
        return response.json()
    })
    .catch(error => console.error("error:", error))
    .then(myJson=>{
        console.log(myJson)
    })
}

getLocation()