"use strict"

// this code has CORS issues. Yelp api does not allow CORS headers.
// Either JSONP or python api.
// Let's use python api.

function getRestaurant(){
    console.log("accessing a random Facebook user")
    let config={}
    config.method="GET"
    config.header={'Authorization':'Bearer ',
        'Content-Type':'application/json','Accept':'application/json',"Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "GET","Access-Control-Allow-Origin":  "https://127.0.0.1:5001"
    }
    config.data=
        '{\n' +
        '    business(id: "garaje-san-francisco") {\n' +
        '        name\n' +
        '        id\n' +
        '        alias\n' +
        '        rating\n' +
        '        url\n' +
        '    }\n' +
        '}'
    config.mode='cors'
    let get_string="https://api.yelp.com/v3/graphql"

    let answer=fetch(get_string,config)
        .then(function(response){
            return response.json()
        })
        .catch(error => console.error("error:", error))
        .then(myJson=>{
            console.log(myJson)
        })
}

getRestaurant()


// curl -X POST -H "Authorization:Bearer " -H "Content-Type: application/graphql" https://api.yelp.com/v3/graphql --data '
// {
//     business(id: "garaje-san-francisco") {
//         name
//         id
//         alias
//         rating
//         url
//     }
// }'