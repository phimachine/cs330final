/*
 * Copyright 2017 Google Inc. All rights reserved.
 *
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
 * file except in compliance with the License. You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under
 * the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific language governing
 * permissions and limitations undervar map;
 */
// Style credit: https://snazzymaps.com/style/1/pale-dawn
const mapStyle = [
    {
        "featureType": "administrative",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "lightness": 33
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
            {
                "color": "#f2e5d4"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#c5dac6"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "all",
        "stylers": [
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#c5c6c6"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#e4d7c6"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#fbfaf7"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#acbcc9"
            }
        ]
    }
];


// Escapes HTML characters in a template literal string, to prevent XSS.
// See https://www.owasp.org/index.php/XSS_%28Cross_Site_Scripting%29_Prevention_Cheat_Sheet#RULE_.231_-_HTML_Escape_Before_Inserting_Untrusted_Data_into_HTML_Element_Content
function sanitizeHTML(strings) {
    const entities = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'};
    let result = strings[0];
    for (let i = 1; i < arguments.length; i++) {
        result += String(arguments[i]).replace(/[&<>'"]/g, (char) => {
            return entities[char];
        });
        result += strings[i];
    }
    return result;
}

function initMap() {
    console.log('initiating map')

    // Create the map.
    // TODO need to initiate the view at correct position.
    const map = new google.maps.Map(document.getElementsByClassName('map')[0], {
        zoom: 7,
        center: {lat: 52.632469, lng: -1.689423},
        styles: mapStyle
    });



    yelpQuery = new YelpQuery(map)
    // console.log(map)

    // Load the stores GeoJSON onto the map.
    yelpQuery.query('dinner', "San Francisco, CA")
    // map.data.loadGeoJson("yelpquery?term="+term+"&location="+location);

    // Define the custom marker icons, using the store's "category".
    // Not going to define it for our application just yet.
    // map.data.setStyle(feature => {
    //     return {
    //         icon: {
    //             url: `img/icon_cafe.png`,
    //             scaledSize: new google.maps.Size(64, 64)
    //         }
    //     };
    // });

    const apiKey = 'AIzaSyAsidkmuLavmoPyURZMxIyBZ0_lB4XqUAI';
    const infoWindow = new google.maps.InfoWindow();
    infoWindow.setOptions({pixelOffset: new google.maps.Size(0, -30)});

    // Show the information for a store when its marker is clicked.


    //
    // map.data.addListener('click', event => {
    //     const category = event.feature.getPrssoperty('category');
    //     const name = event.feature.getProperty('name');
    //     const description = event.feature.getProperty('description');
    //     const hours = event.feature.getProperty('hours');
    //     const phone = event.feature.getProperty('phone');
    //     const position = event.feature.getGeometry().get();
    //     const content = sanitizeHTML`
    //   <img style="float:left; width:200px; margin-top:30px" src="img/logo_${category}.png">
    //   <div style="margin-left:220px; margin-bottom:20px;">
    //     <h2>${name}</h2><p>${description}</p>
    //     <p><b>Open:</b> ${hours}<br/><b>Phone:</b> ${phone}</p>
    //     <p><img src="https://maps.googleapis.com/maps/api/streetview?size=350x120&location=${position.lat()},${position.lng()}&key=${apiKey}"></p>
    //   </div>
    // `;

    // TODO get the html right
    map.data.addListener('click', event => {
        let date = new Date()

        const category = event.feature.getProperty('category').join("/")
        const name = event.feature.getProperty('name')
        const todayhours = event.feature.getProperty('hours')[0]["open"][date.getDay()]
        console.log(todayhours)
        const todayhoursstring = (todayhours['start'].slice(0, 2) + ":" + todayhours['start'].slice(2, 4) +
            "-" + todayhours['end'].slice(0, 2) + ":" + todayhours['end'].slice(2, 4))
        const imageUrl = event.feature.getProperty('image_url')
        console.log(imageUrl)
        const phone = event.feature.getProperty('phone')
        const price = event.feature.getProperty('price')
        const rating = event.feature.getProperty('rating')
        const rating_png="img/yelp_stars/extra_large/extra_large_"+rating+"_half@3x.png"
        const address = event.feature.getProperty('location')['display_address'].join(", ")
        const position = event.feature.getGeometry().get();
        const description = "foo bar"
        // from html:
        const content = sanitizeHTML`
            <div><img style=\"float:left; width:300px; margin-top:0px\" src=\"${imageUrl}\">
            <div style="margin-left:320px; margin-bottom:20px;">
                <h2>${name}<br/>
                <img style=\"float:left; width:100px; margin-top:5px\" src=\"${rating_png}\"><br/>
                </h2>
                
                <p>
                <b>Price:</b> ${price}<br/>
                <b>Category:</b> ${category}<br/>
                <b>Today's hour:</b> ${todayhoursstring}<br/>
                <b>Phone:</b> ${phone}<br/>
                <b>Address:</b> ${address}<br/>
                </p>
                <p><b>Google Streetview:</b><br/>
            </div></div>
            
            <div>
                <img  style=\"margin-top:10px\" src=\"https://maps.googleapis.com/maps/api/streetview?size=350x120&location=${position.lat()},${position.lng()}&key=${apiKey}\"></p>
            </div>
        `

        infoWindow.setContent(content);
        infoWindow.setPosition(position);
        infoWindow.open(map);


        google.maps.event.addListener(infoWindow,'domready',function(){
            $('#div-main-infoWindow')//the root of the content
                .closest('.gm-style-iw')
                .parent().addClass('custom-iw')
            console.log('added')
        });
    });

}
