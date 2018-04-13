class YelpQuery {
    constructor(map){
        this.map=map
    }

    query(term, location){
        let config={}

        config.method='GET'
        config.header={'Content-Type':'application/json','Accept':'application/json'}

        let get_string="/yelpquery?term="+term+"&location="+location
        // console.log(get_string)
        fetch(get_string,config)
            .then(function (response){
                return response.json()
            })
            .catch(error => console.error("error: ", error))
            .then(myJson=>{
                this.map.data.addGeoJson(myJson)
            })
    }
}