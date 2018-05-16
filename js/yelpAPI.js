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
        let self=this
        fetch(get_string,config)
            .then(function (response){
                if (response.status==204){
                    self.nonefound(term,location)
                    console.log("none found")
                    return null
                }
                return response.json()
            })
            .catch(error => {
                console.error("error: ", error)
            })
            .then(myJson=>{
                console.log(myJson)

                if (myJson==null){
                    this.nonefound()
                }else{
                    this.map.data.addGeoJson(myJson)
                    // console.log("addGeoJson",myJson)
                    // coordinates=myJson['geometry']['coordinates']
                    // console.log(myJson['geometry']['coordinates'])
                    let coordinates=myJson['geometry']['coordinates']
                    // LatLng correct,but geoJson has a different coordinate system.
                    // geoJson is longlat and latlng, well, is latlong
                    this.map.setCenter(new google.maps.LatLng(coordinates[1],coordinates[0]))
                    this.map.setZoom(13)
                }

            })
    }

    nonefound(term, location){
        // let map=document.getElementsByClassName('map')[0]
        // $(map).ready(function(){
        //     let box=document.getElementsByClassName("gmnoprint")[0]
        //     let hei=window.getComputedStyle(box).getPropertyValue("height")
        //     console.log(hei)
        //     $('#failureAlert').show()
        // })

        $('#headerslot').html(`
            <div class="alert alert-warning d-flex justify-content-between align-items-center">
              No restaurants found.
              <button type="button" class="btn btn-secondary text-center" data-dismiss="alert">close</button>
            </div>
                    
        `)
        // No need to do anything.
    }


}