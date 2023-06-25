function updateMap() {
    // Constants
    const API_KEY = "AIzaSyDocN5FdpANWDjJhfctCaqNgF-JNuZIAUE";
    const SIZE = "500x350";
    const ZOOM = 11;
    const CENTER = "-34.924164070184126,138.60093358259886";

    // Getting the bus config from the DOM
    let bus_route = document.getElementById("route").value;
    let wheelchair = document.getElementById("wheelchairCheck").checked;
    let aircon = document.getElementById("airconCheck").checked;
    let payload = JSON.stringify({
        "route": bus_route,
        "wheelchair": wheelchair,
        "aircon": aircon
    });

    // Getting the busses
    fetch("/route", {method: "POST", body: payload, headers: {"Content-Type": "application/json"}})
    .then(response => response.json())
    .then(data => {
        // Converting the busses into markers
        markers = "";
        for (let i = 0; i < data["busses"].length; i++) {
            markers += `&markers=color:blue|${data["busses"][i]["latitude"]},${data["busses"][i]["longitude"]}|`;
        }

        // Set the map image
        let map_image = `https://maps.googleapis.com/maps/api/staticmap?key=${API_KEY}&size=${SIZE}&zoom=${ZOOM}&center=${CENTER}&markers=${markers}`;
        document.getElementById("map").src = map_image;
    })
    .catch(error => console.log(error));
}