function getLocation(){
    console.log("getting a video information")
    let config={}
    config.method="GET"
    config.header={'Content-Type':'application/json','Accept':'application/json'}

    let get_string="https://www.googleapis.com/youtube/v3/videos?id=AWWG-Wwo9AY&key=&part=recordingDetails"

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


function searchRestaurant(){
    console.log("searching for a restaurant")
    let config={}
    config.method="POST"
    config.header={'Authorization': 'Bearer ',
    'Content-Type': 'application/graphql'}
    config.data={
    business(id: "garaje-san-francisco") {
        name
        id
        alias
        rating
        url
    }
}

    let get_string='https://api.yelp.com/v3/graphql'

    let answer=fetch(get_string,config)
}