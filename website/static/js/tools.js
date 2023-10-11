export function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  console.log("cookie");
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

export function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

export function lock() {
    fetch("/lock_id", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
        .then(res => res.json())
        .then(data => {
            setCookie("lock", data["lock_id"], 7);
        })
        .catch(err => {
            console.error('Error: ', err)
            alert('Could not get lock id.')
    })
}

export async function getConfig() {
    return fetch("/settings/server_config", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
        .then(res => res.json())
        .then(data => {
            return data
        })
        .catch(err => {
            console.error('Error: ', err)
            alert('Could not load server config.')
        })
}

export function sendPost(url, data, error_text) {
    fetch(url, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body : JSON.stringify(data)
    })
        .then((response) => {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response;
        })
        .catch((error) => {
            console.error(error);
            alert(error_text + error);
        });
}

export async function refreshFromLocalStorage() {
    await getConfig().then((config) => {

        let settingsDisplay = localStorage.getItem("display");
        if (settingsDisplay === null || settingsDisplay === "undefined") {
            settingsDisplay = config["default_display"];
            localStorage.setItem("display", settingsDisplay);
        } else {
            sendPost("/settings/display",
                {"display": settingsDisplay},
            "Could not send settings display: ");
        }

        let trackingDisplay = localStorage.getItem("trackingDisplay");
        if (trackingDisplay === null || trackingDisplay === "undefined") {
            trackingDisplay = config["tracking_display"];
            localStorage.setItem("trackingDisplay", trackingDisplay);
        } else {
            sendPost("/settings/tracking_display",
                {"tracking_display": trackingDisplay},
            "Could not send tracking display: ");
        }


        let selectionThickness = localStorage.getItem("selectionThickness");
        if (selectionThickness === null || selectionThickness === "undefined") {
            selectionThickness = config["selection_thickness"];
            localStorage.setItem("selectionAutomatic", selectionThickness);
        }

        let selectionColor = localStorage.getItem("selectionColor");
        if (selectionColor === null || selectionColor === "undefined") {
            selectionColor = config["selection_color"];
            localStorage.setItem("selectionColor", selectionColor);
        }

        let selectionAutomatic = localStorage.getItem("selectionAutomatic");
        if (selectionAutomatic === null || selectionAutomatic === "undefined") {
            selectionAutomatic = config["selection_automatic"];
            localStorage.setItem("selectionAutomatic", selectionAutomatic);
        }


        let trackingColor = localStorage.getItem("trackingColor");
        if (trackingColor === null || trackingColor === "undefined") {
            trackingColor = config["tracking_color"];
            localStorage.setItem("trackingColor", trackingColor);
        } else {
            sendPost("/settings/tracking_color",
        {"tracking_color": trackingColor},
        "Could not send tracking color: ");
        }


        let trackingThickness = localStorage.getItem("trackingThickness");
        if (trackingThickness === null || trackingThickness === "undefined") {
            trackingThickness = config["tracking_thickness"];
            localStorage.setItem("trackingThickness", trackingThickness)
        } else {
            sendPost("/settings/tracking_thickness",
            {"tracking_thickness": trackingThickness},
            "Could not send tracking thickness: ");
        }
    });
}

