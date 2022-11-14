// function addClass() {
//     let element = document.getElementById('username');
//     element.classList.add('mystyle');
// }


// function changeBg(input){
//     let file = $("input[type=file]").get(0).files[0];

//     if(file){
//       let reader = new FileReader();

//       reader.onload = function(){

//           $("#avatar_picture").attr("src", reader.result);
//       }

//       reader.readAsDataURL(file);
//     }
// }

// function changeAvatar(input){
//     let file = $("input[type=file]").get(0).files[0];

//     if(file){
//       let reader = new FileReader();

//       reader.onload = function(){
//           $("#previewBg").attr("src", reader.result);
//       }

//       reader.readAsDataURL(file);
//     }
// }

// var URL = window.URL || window.webkitURL

// window.swapImage = function (elm) {
//   var index = elm.dataset.index
//   // URL.createObjectURL is faster then using the filereader with base64
//   var url = URL.createObjectURL(elm.files[0])
//   document.querySelector('img[data-index="'+index+'"]').src = url
// }

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



var autocomplete;



function initialize() {
    initAutocomplete();
    initMap();
    
}


function initMap() {
    var xlng = 13.4050;
var xlat = 52.5200;
    let map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 52.5200, lng: 13.4050 },
        zoom: 12,
    });
    let infoWindow = new google.maps.InfoWindow();

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

                    infoWindow.setPosition(pos);
                    infoWindow.setContent("You are here.");
                    infoWindow.open(map);
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

    new google.maps.Marker({
        position: { lat: xlat, lng: xlng },
        map,
        title: "Hello World!",
      });
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


