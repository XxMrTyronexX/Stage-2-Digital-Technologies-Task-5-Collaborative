// Alerts refresh function
function refreshAlerts() {
    fetch("/alerts")
    .then(response => response.json())
    .then(data => {
        alertsTab = document.getElementById("tab-2");
        alertsTab.innerHTML = "<br><h1 class='font-sans text-5xl font-bold'>Service Alerts</h1><br>";

        for (let i = 0; i < data["alerts"].length; i++) {
            let alertHTML = `<h3>${data["alerts"][i]["title"]}</h3><p>${data["alerts"][i]["content"]}</p><br>`;
            alertsTab.innerHTML += alertHTML;
        }
    })
    .catch(error => console.log(error));
}
refreshAlerts();

// Map function
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
        console.log(data);
        for (let i = 0; i < data["busses"].length; i++) {
            markers += `&markers=color:blue|${data["busses"][i]["latitude"]},${data["busses"][i]["longitude"]}|`;
        }

        // Set the map image
        let map_image = `https://maps.googleapis.com/maps/api/staticmap?key=${API_KEY}&size=${SIZE}&zoom=${ZOOM}&center=${CENTER}${markers}`;
        document.getElementById("map").src = map_image;
    })
    .catch(error => console.log(error));
}

// Tab changing function
function changeTab(button, tabNum) {
    // Adding a border to the bottom of all tabs
    let allTabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < allTabButtons.length; i++)
        allTabButtons[i].style.borderBottomWidth = "2px";

    // Disabling the bottom border on this button
    button.style.borderBottomWidth = "0px";

    // Loop through each tab and hiding it
    let allTabs = document.getElementsByClassName("tab");
    for (let i = 0; i < allTabs.length; i++)
        allTabs[i].style.display = "none";

    // Finally set the tab we want's visibility to block
    let tab = document.getElementById("tab-" + tabNum);
    tab.style.display = "block";
}