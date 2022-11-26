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

    let myMarkers = [];

    for (var i = 0; i < partyLocations_And_Author.length; i++) {
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(partyLocations_And_Author[i][1], partyLocations_And_Author[i][2]),
            map: map,
            icon: 'https://res.cloudinary.com/devqm7qmb/image/upload/v1668959317/icons8-place-marker-50_kl0zxy.png'
        });

        // Create infowindows
        var infoWindowOptions = {
            position: { lat: partyLocations_And_Author[i][1], lng: partyLocations_And_Author[i][2] }

        }

        const infoWindow_ForMarker = new google.maps.InfoWindow(infoWindowOptions)

        infoWindow_ForMarker.setContent(infoWindowContent[i][0])

        const infoWindowOpenOptions = {
            map: map,
            anchor: marker,
            shouldFocus: false
        }

        var currWindow;
        marker.addListener('click', () => {
            if (currWindow) {
                currWindow.close();
            }

            currWindow = infoWindow_ForMarker;
            infoWindow_ForMarker.open(infoWindowOpenOptions);
        })

        google.maps.event.addListener(map, "click", function (event) {
            infoWindow_ForMarker.close();
        });

        // Push current user's parties markers to the array
        if (partyLocations_And_Author[i][3] == currentUserUsername) {
            myMarkers.push(marker);
        }

    }

    // add event listeners for the buttons
    document.getElementById("show-markers").addEventListener("click", showMarkers);
    document.getElementById("hide-markers").addEventListener("click", hideMarkers);

    // Sets the map on all markers in the array.
    function setMapOnAll(valueOrNull) {

        for (let i = 0; i < myMarkers.length; i++) {
            myMarkers[i].setMap(valueOrNull);
        }
    }

    // Removes the markers from the map, but keeps them in the array.
    function hideMarkers() {
        setMapOnAll(null);
    }

    // Shows any markers currently in the array.
    function showMarkers() {
        setMapOnAll(map);
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



