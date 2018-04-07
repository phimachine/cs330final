"use strict"

function getAppAccessToken(){
    console.log("getting an app access token")
    let config={}
    config.method="GET"
    config.header={'Content-Type':'application/json','Accept':'application/json'}

    let get_string="https://graph.facebook.com/oauth/access_token?client_id={app-id}\n" +
        "    &client_secret={app-secret}\n" +
        "    &grant_type=client_credentials"
}

function tryApi(userId){
    console.log("accessing a random Facebook user")
    let config={}
    config.method="GET"
    config.header={'Content-Type':'application/json','Accept':'application/json'}

    let get_string="https://graph.facebook.com/v2.12/"+userId+"&access_token="

    let answer=fetch(get_string,config)
        .then(function(response){
            return response.json()
        })
        .catch(error => console.error("error:", error))
        .then(myJson=>{
            console.log(myJson)
        })
}

tryApi(1000019)