// function addClass() {
//     let element = document.getElementById('username');
//     element.classList.add('mystyle');
// }


//Profile's and Background's preview picture

const inpFileBg = document.getElementById("bg_picture");
const previewBgContainer = document.getElementById("imageBgPreview");
const imageBgPreview = previewBgContainer.querySelector(".image-preview__image");

inpFileBg.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();
        reader.addEventListener("load", function () {
            imageBgPreview.setAttribute("src", this.result);
        });
        reader.readAsDataURL(file);
    }
});


const inpFileAv = document.getElementById("avatar_picture");
const previewAvContainer = document.getElementById("imageAvPreview");
const imageAvPreview = previewAvContainer.querySelector(".image-preview__image");

inpFileAv.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();
        reader.addEventListener("load", function () {
            imageAvPreview.setAttribute("src", this.result);
        });
        reader.readAsDataURL(file);
    }
});


//Adding markers on the map

var autocomplete;
var xlng;
var xlat;
var marker_user;



function initialize() {
    initAutocomplete();
    initMap();

}


function initMap() {
    let map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 52.5200, lng: 13.4050 },
        zoom: 12,
    });
    // let infoWindow = new google.maps.InfoWindow();

    const locationButton = document.createElement("button");

    locationButton.textContent = "Pan to Current Location";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
    locationButton.addEventListener("click", () => {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    marker_user = new google.maps.Marker({
                        position: pos,
                        map: map,
                        icon: 'https://res.cloudinary.com/devqm7qmb/image/upload/v1668961699/icons8-place-marker-50-3_inyujp.png'
                    });

                    // infoWindow.setPosition(pos);
                    // infoWindow.setContent("You are here.");

                    // infoWindow.open(map);
                    map.setCenter(pos);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });

    // var marker, i, infoWindow_ForMarker, infoWindowOptions

    for (var i = 0; i < locations.length; i++) {
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
            map: map,
            icon: 'https://res.cloudinary.com/devqm7qmb/image/upload/v1668959317/icons8-place-marker-50_kl0zxy.png'
        });

        var infoWindowOptions = {
            // content: 'This is marker',
            position: { lat: locations[i][1], lng: locations[i][2] }

        }

        const infoWindow_ForMarker = new google.maps.InfoWindow(infoWindowOptions)

        infoWindow_ForMarker.setContent(infoWindowContent[i][0])
            // '<div class="row">' + 
            //     '<div class="col-6">' + 
            //         '<div>Title</div>' + 
            //         '<div>Host</div>' + 
            //         '<div>Date</div>' + 
            //         '<div>Description</div>' + 
            //         '<div>Address</div>' + 
            //         '<div>Languages</div>' + 
            //         '<div>Whatsapp link</div>' + 
            //         '<div>Participants</div>' + 
            //         '</div>' + 
            //         '<div class="col-6">' + 
            //         '<div>' + locations_And_partyInfo[i][0] + '</div>' + 
            //         '<div>' + locations_And_partyInfo[i][3] + '</div>' + 
            //         '<div>' + locations_And_partyInfo[i][4] + '</div>' + 
            //         '<div>' + locations_And_partyInfo[i][5] + '</div>' + 
            //         '<div>' + locations_And_partyInfo[i][6] + '</div>' + 
            //         '<div>' + locations_And_partyInfo[i][7] + '</div>' + 
            //         '<div>' + locations_And_partyInfo[i][8] + '</div>' + 
            //         '<div>' + locations_And_partyInfo[i][8] + '</div>' + 
                    // '<div>' + infoWindowContent[i][0] + '</div>' + 
                    // '<div>' + infoWindowContent[i][0] + '</div>' + 
                    // '<div>' + infoWindowContent[i][0] + '</div>' + 
                    // '<div>' + infoWindowContent[i][0] + '</div>' + 
                    // '<div>' + infoWindowContent[i][0] + '</div>' + 
                    // '<div>' + infoWindowContent[i][0] + '</div>' + 
                    // '<div></div>' + 

        //         '</div>' + 
        //     '</div>'
        // );




        // ['<div class="row">' + 
        //         '<div class="col-6">' + 
        //             '<div>Title</div>' + 
        //             '<div>Host</div>' + 
        //             '<div>Date</div>' + 
        //             '<div>Description</div>' + 
        //             '<div>Address</div>' + 
        //             '<div>Languages</div>' + 
        //             '<div>Whatsapp link</div>' + 
        //             '<div>Participants</div>' + 
        //             '</div>' + 
        //             '<div class="col-6">' + 
        //             '<div>' + '{{ party.title }}' + '</div>' + 
        //             '<div>' + '{{ party.author.username }}' + '</div>' + 
        //             '<div>' + '{{ party.date_time }}' + '</div>' + 
        //             '<div>' + '{{ party.description }}' + '</div>' + 
        //             '<div>' + '{{ party.address }}' + '</div>' + 
        //             '<div>' + '{{ party.party_languages }}' + '</div>' + 
        //             '<div>' + '{{ party.whatsapp_link }}' + '</div>' + 
        //             '<div>' + '{{ party.whatsapp_link }}' + '</div>' + 

        //         '</div>' + 
        // '</div>'],
        // infoWindow_ForMarkers.setPosition('');

        const infoWindowOpenOptions = {
            map: map,
            anchor: marker,
            shouldFocus: false
        }

        var currWindow;
        marker.addListener('click', () => {
            if( currWindow ) {
                currWindow.close();
             }

            currWindow = infoWindow_ForMarker;
            infoWindow_ForMarker.open(infoWindowOpenOptions);
        })

        google.maps.event.addListener(map, "click", function(event) {
            infoWindow_ForMarker.close();
        });

        
    }

}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

//Automatic suggestion of an address when you filling a field

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'),
        {
            types: ['establishment'],
            componentRestrictions: { 'country': ['DE'] },
            fields: ['place_id', 'geometry', 'name']
        });
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();
    console.log(place.geometry.location.lat(), place.geometry.location.lng());
    document.getElementById('lat').value = place.geometry.location.lat();
    document.getElementById('lng').value = place.geometry.location.lng();

    if (!place.geometry) {
        //User didn't select a prediction; reset the input field
        document.getElementById('autocomplete').placeholder = 'Where is your party at?';
    } else {
        //Display details about the valid place
        document.getElementById('details').innerHTML = place.name;
    }
}

window.initMap = initMap;



