
import {refreshFromLocalStorage, sendPost} from './tools.js';

function catalogLabels() {
    let labels = document.getElementsByTagName('LABEL');
    for (let i = 0; i < labels.length; i++) {
        if (labels[i].htmlFor !== '') {
            let elem = document.getElementById(labels[i].htmlFor);
            if (elem)
                elem.label = labels[i];
        }
    }
}

function dropdrownRefresh(id, storageKey) {
    let element = document.getElementById(id);
    for(let  i, j = 0; i = element.options[j]; j++) {
        if (i.value === localStorage.getItem(storageKey)) {
            element.selectedIndex = j;
            break;
        }
    }
    element.addEventListener("input", () =>
        localStorage.setItem(storageKey, element.value)
    );
}

function genericRefresh(id, storageKey, func = (e) => {}) {
    let element = document.getElementById(id);
    element.defaultValue = localStorage.getItem(storageKey);
    element.addEventListener("input", (e) => {
        localStorage.setItem(storageKey, element.value)
        func.call(id);
    });
}

function genericSendRefresh(id, storageKey, url, post_key, error, func = (e) => {}) {
    let value = localStorage.getItem(storageKey);
    let element = document.getElementById(id);
    element.defaultValue = value;
    element.addEventListener("input", (e) => {
            localStorage.setItem(storageKey, element.value);
            sendPost(url,
                {[post_key]: element.value},
                error);
            func.call(id);
        }
    );
}

function dropdownSendRefresh(id, storageKey, url, post_key, error, func = (e) => {}) {
    let element = document.getElementById(id);
    for(let  i, j = 0; i = element.options[j]; j++) {
        if (i.value === localStorage.getItem(storageKey)) {
            element.selectedIndex = j;
            break;
        }
    }
    element.addEventListener("input", () => {
        localStorage.setItem(storageKey, element.value);
        sendPost(url, {[post_key]: element.value}, error);
        console.log(id);
        func(id);
    });
}

function disableElementsByCheckbox(checkboxId, elementIdList) {
    let elementList = [];
    console.log(checkboxId);
    let checkbox = document.getElementById(checkboxId);
    for (let i = 0; i < elementIdList.length; i++) {
        elementList.push(document.getElementById(elementIdList[i]));
    }

    if (checkbox.checked) {
        for (let i = 0; i < elementList.length; i++) {
            elementList[i].disabled = true;
            elementList[i].classList.add("input-disabled");
            elementList[i].label.classList.add("input-disabled");
        }
    } else {
        for (let i = 0; i < elementList.length; i++) {
            elementList[i].disabled = false;
            elementList[i].classList.remove("input-disabled");
            elementList[i].label.classList.remove("input-disabled");
        }
    }
}

function f(id) {
    console.log(id);
    disableElementsByCheckbox(id, ["selection-thickness", "selection-color"])
}
window.addEventListener('load', async function () {
    await refreshFromLocalStorage().then(() => {
        catalogLabels()

        dropdrownRefresh("settings-display", "display");

        genericRefresh("selection-color", "selectionColor");
        genericRefresh("selection-thickness", "selectionThickness");
        genericRefresh("selection-automatic", "selectionAutomatic",
            function () {
                disableElementsByCheckbox("selection-automatic", ["selection-thickness", "selection-color"])
            });

        disableElementsByCheckbox("selection-automatic",
            ["selection-thickness", "selection-color"])

        genericSendRefresh("tracking-color", "trackingColor", "/settings/tracking_color",
            "tracking_color", "Could not send tracking color: ");
        genericSendRefresh("tracking-thickness", "trackingThickness", "/settings/tracking_thickness",
            "tracking_thickness", "Could not send tracking thickness: ");
        dropdownSendRefresh("tracking-display", "trackingDisplay", "/settings/tracking_display",
            "tracking_display", "Could not send tracking display: ");


    });

}, false);

