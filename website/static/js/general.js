import {sendPost, lock, getCookie, setCookie} from "./tools.js";

window.addEventListener('load', async function () {
    let orig = document.getElementById("header-widgets");
    let bala = document.getElementById("header-widgets-balancer");
    console.log(orig.offsetWidth);
    if (window.screen.width > 500) {
        bala.style.width = orig.offsetWidth + "px";
    } else {
        bala.style.width = "20px";
    }

    let lockBtn = document.getElementById("read-write-toggle");
    lockBtn.onclick = lock;

    let darkLightBtn = document.getElementById("dark-light-toggle");
    let a = darkLightBtn.querySelector("a");
    darkLightBtn.onclick = () => {
        let html = document.querySelector("html");
        if (html.classList.contains("dark-mode")) {
            a.innerText = "🌑";
        } else {
            a.innerText = "🌕";
        }
        html.classList.toggle("dark-mode");

        if (getCookie("dark_mode") === "true") {
            setCookie("dark_mode", "false", "365");
        } else {
            setCookie("dark_mode", "true", "365");
        }
    };
    if (getCookie("dark_mode") === "true") {
        document.querySelector("html").classList.add("dark-mode");
        a.innerText = "🌕";
    } else {
        document.querySelector("html").classList.remove("dark-mode");
        a.innerText = "🌑";
    }

}, false);