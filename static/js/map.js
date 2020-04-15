// API call to USGS API to get earthquake data

var test_data=[{'location':[43.6529, -79.3849], 'title':'The Wind Through the Keyhole', 'rating':4.15},
{'location':[43.67719, -79.700219], 'title':'Lock Every Door', 'rating':3.92},
{'location':[43.661198, -79.385265], 'title':'Stone Bleeding', 'rating':3.95},
{'location':[43.6527,-79.3834], 'title':'Mask Market', 'rating':4.03}]



// satellite map
var satelliteMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors,\
        <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.satellite",
        accessToken: API_KEY_Leaflet
      });

// light and dark map visualization
var streetMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
//var streetMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, \
        <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery A© <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 15,
        id: "mapbox.light",
        accessToken: API_KEY_Leaflet
      });


var darkMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, \
        <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery A© <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 15,
        id: "mapbox.dark",
        accessToken: API_KEY_Leaflet
      });

//outdoors map
var outdoorsMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution:"Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, \
        <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery A© <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.outdoors",
        accessToken: API_KEY_Leaflet
      });

// Define a baseMaps object
var baseMaps = {
        "Light Map": streetMap,
        "Dark Map": darkMap,
        "Satellite": satelliteMap,
        "Outdoors": outdoorsMap
      };

var overlayMaps = {
  "Light Map": streetMap,
  
};

// Create our map
var myMap = L.map("map", {
        center: [43.6532, -79.3832],
        zoom: 10,
        layers: [streetMap]
      });

for (var i = 0; i < test_data.length; i++) {
  var owner = test_data[i];
  L.marker(owner.location)
    .bindPopup("<h4>" + owner.title + "</h4> <hr> <h4>Average_rating" + owner.rating + "</h4>").addTo(myMap)};
      
// Create a layer control
// Pass in our baseMaps and overlayMaps
// Add the layer control to the map
L.control.layers(baseMaps,overlayMaps, {
        collapsed: true
      }).addTo(myMap);

// Setting up the legend
