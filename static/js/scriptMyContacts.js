let map, directionsService, directionsRenderer;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 44.9727, lng: -93.23540000000003 },
    zoom: 14
  });

  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  var names = document.getElementsByClassName("names");
  var locations = document.getElementsByClassName("locations");

  for (let i = 0; i < names.length; i++) {
    createMarkerForLocation(locations[i].innerHTML, names[i].innerHTML, map);
  }

  getMyLocationMarker();
}

function createMarkerForLocation(address, title, map) {
  var geocoder = new google.maps.Geocoder();

  geocoder.geocode({ 'address': address }, function (results, status) {
    if (status === 'OK') {
      var locationPrecise = results[0].geometry.location;

      var offsetLat = (Math.random() - 0.5) * 0.0005;
      var offsetLng = (Math.random() - 0.5) * 0.0005;

      var adjustedLocation = {
        lat: locationPrecise.lat() + offsetLat,
        lng: locationPrecise.lng() + offsetLng
      };

      var marker = new google.maps.Marker({
        map: map,
        position: adjustedLocation,
        title: title
      });

      var infowindow = new google.maps.InfoWindow({
        content: '<div id="content"><div id="bodyContent"><p>' + title + '</p></div></div>'
      });

      marker.addListener('click', function () {
        infowindow.open(map, marker);
      });
    } else {
      console.error('Geocode was not successful for the following reason: ' + status);
    }
  });
}

function getMyLocationMarker() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var myLocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      var marker = new google.maps.Marker({
        position: myLocation,
        map: map,
        title: 'Your Location'
      });

      var infowindow = new google.maps.InfoWindow({
        content: '<div id="content"><div id="bodyContent"><p>Your Current Location</p></div></div>'
      });

      marker.addListener('click', function () {
        infowindow.open(map, marker);
      });

      map.setCenter(myLocation);
      console.log("My location: ", myLocation);
    }, function (error) {
      console.error('Geolocation permission denied or unavailable.');
    }, { enableHighAccuracy: true });
  } else {
    console.error('Geolocation is not supported by this browser.');
  }
}


function getMyDestination() {
  var destinationInput = document.getElementById('destinationInput').value;
  var geocoder = new google.maps.Geocoder();

  geocoder.geocode({ 'address': destinationInput }, function (results, status) {
    if (status === 'OK') {
      var destinationLocation = results[0].geometry.location;
      var destinationAddress = results[0].formatted_address;
      var travelMode = document.querySelector('input[name="travelMode"]:checked').value;

      calculateAndDisplayRoute(destinationLocation, travelMode);
    } else {
      console.error('Geocode was not successful for the following reason: ' + status);
    }
  });
}

function calculateAndDisplayRoute(destinationLocation, travelMode) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var myLocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      directionsService.route({
        origin: myLocation,
        destination: destinationLocation,
        travelMode: google.maps.TravelMode[travelMode]
      }, function (response, status) {
        if (status === 'OK') {
          directionsRenderer.setDirections(response);
        } else {
          console.error('Directions request failed due to ' + status);
        }
      });
    });
  }
}

document.getElementById('destinationForm').addEventListener('submit', function (event) {
  event.preventDefault();
  getMyDestination();
});
