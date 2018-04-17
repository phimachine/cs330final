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
        let geoJson=null
        fetch(get_string,config)
            .then(function (response){
                return response.json()
            })
            .catch(error => {
                if (error.name=="SyntaxError"){
                    this.noquery(term,location)
                    return
                }else{
                    console.error("error: ", error)
                }
            })
            .then(myJson=>{
                this.map.data.addGeoJson(myJson)
                // console.log("addGeoJson",myJson)
                // coordinates=myJson['geometry']['coordinates']
                // console.log(myJson['geometry']['coordinates'])
                let coordinates=myJson['geometry']['coordinates']
                // LatLng correct,but geoJson has a different coordinate system.
                // geoJson is longlat and latlng, well, is latlong
                this.map.setCenter(new google.maps.LatLng(coordinates[1],coordinates[0]))
                this.map.setZoom(13)
            })
    }

    noquery(term,location){
        // let map=document.getElementsByClassName('map')[0]
        // $(map).ready(function(){
        //     let box=document.getElementsByClassName("gmnoprint")[0]
        //     let hei=window.getComputedStyle(box).getPropertyValue("height")
        //     console.log(hei)
        //     $('#failureAlert').show()
        // })

        $('#failureAlert').show()

    }


}