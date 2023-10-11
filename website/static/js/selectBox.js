import {refreshFromLocalStorage, sendPost} from './tools.js';

window.addEventListener('load', async function () {
    await refreshFromLocalStorage();

    // your code here
    const d = document.getElementById("mask").querySelector("img");
    let clicked = false;
    let box = -1;

    let start = [0, 0];
    let end = [0, 0];

    d.addEventListener("mousedown", handleMouseDown);
    document.addEventListener("mouseup", handleMouseUp);

    // if more initial, need to add process for video-expand-add
    // document.getElementById("mask").classList.remove("hidden");
    //
    // document.querySelectorAll(".video-add").forEach((elem) => {
    //         elem.onclick = (event) => {
    //             let selection = document.createElement("div");
    //             selection.classList.add("video-add-selection");
    //
    //             // populate options
    //             document.querySelectorAll(".video.hidden").forEach(
    //                 (hiddenVideo) => {
    //                     let option = document.createElement("div");
    //                     option.classList.add("video-add-option");
    //                     let p = document.createElement("p");
    //                     p.innerText = hiddenVideo.id;
    //                     option.appendChild(p);
    //                     option.onclick = () => {
    //                         let img = document.querySelector(".video:not(.hidden) img");
    //                         console.log(img);
    //                         img.classList.remove("video-expand-add");
    //                         console.log(img.classList.toString());
    //                         hiddenVideo.classList.remove("hidden");
    //                         selection.remove();
    //                     }
    //                     selection.appendChild(option);
    //                     console.log(option);
    //                 }
    //             )
    //             selection.style.top = event.pageY + "px";
    //             selection.style.left = event.pageX + "px";
    //             selection.onmouseleave = () => {
    //                 selection.remove();
    //                 console.log("remove add list");
    //             }
    //             console.log(selection);
    //             elem.appendChild(selection);
    //
    //         }
    //
    //         elem.onmouseleave = () => {
    //             elem.replaceChildren();
    //         };
    //     }
    // );


    function getRelativeMousePosition(e) {
        // e = Mouse click event.
        var rect = d.getBoundingClientRect();
        var x = Math.min((e.clientX - rect.left) / rect.width, 1); //x position within the element.
        var y = Math.min((e.clientY - rect.top) / rect.height, 1);  //y position within the element.
        console.log("Left? : " + x + " ; Top? : " + y + ".");

        box = document.createElement("div");
        return [x, y]
    }

    (function () {
        window.currentMouseX = 0;
        window.currentMouseY = 0;

        // Guess the initial mouse position approximately if possible:
        var hoveredElement = document.querySelectorAll(':hover');
        hoveredElement = hoveredElement[hoveredElement.length - 1]; // Get the most specific hovered element

        if (hoveredElement != null) {
            var rect = hoveredElement.getBoundingClientRect();
            // Set the values from hovered element's position
            window.currentMouseX = window.scrollX + rect.x;
            window.currentMouseY = window.scrollY + rect.y;
        }

        // Listen for mouse movements to set the correct values
        window.addEventListener("mousemove", function (e) {
            // console.log("move");
            window.currentMouseX = e.clientX;
            window.currentMouseY = e.clientY;
        }, /*useCapture=*/true);
    }())
    let boxExists = false;
    let boxTop = 0;
    let boxLeft = 0;

    function check_cursor() {
        let border = localStorage.getItem("selectionThickness");
        if (border === null) {
            border = 4;
        }
        let color = localStorage.getItem("selectionColor");
        if (color === null) {
            color = "red";
        }
        // console.log("check");
        if (clicked) {
            // console.log(box)
            if (!boxExists) {
                let boxContainer = document.createElement("div");
                boxContainer.id = "box-container";
                boxContainer.style.position = "fixed";
                boxContainer.style.top = (window.currentMouseY - border) + "px";
                boxTop = window.currentMouseY - border;
                boxContainer.style.height = "1px";
                boxLeft = window.currentMouseX - border;
                boxContainer.style.left = (window.currentMouseX - border) + "px";
                boxContainer.style.width = "1px";
                document.getElementById("content").appendChild(boxContainer);


                box = document.createElement("div");
                box.style.position = "relative";
                box.style.overflow = "visible";
                box.style.border = border + "px solid " + color;
                box.id = "box";
                // console.log("BOX");
                box = document.getElementById("box-container").appendChild(box);
                boxExists = true;
            } else if (boxExists) {
                // console.log("b");
                let width = window.currentMouseX - boxLeft - border;
                let height = window.currentMouseY - boxTop - border;
                // console.log(border, width, height);

                if (width >= 0) {
                    box.style.paddingRight = width + "px";
                    box.style.right = 0;
                } else {
                    box.style.right = -width + "px";
                    box.style.paddingRight = -width + "px";
                }

                // console.log(height + "px")
                if (height >= 0) {
                    box.style.paddingBottom = height + "px";
                    box.style.bottom = 0;
                } else {
                    box.style.paddingBottom = -height + "px";
                    box.style.bottom = -height + "px";
                }

            }

        }
    }

    setInterval(check_cursor, 20);

    function handleMouseUp(e) {
        if (clicked) {
            end = getRelativeMousePosition(e);
            clicked = false;
            box = -1;
            document.getElementById("box").remove();
            document.getElementById("box-container").remove();
            boxExists = false;
            // console.log("up")

            let bbox = [Math.min(start[0], end[0]), Math.min(start[1], end[1]),
                Math.abs(start[0] - end[0]), Math.abs(start[1] - end[1])];

            sendPost(
                "/cam_lock",
                {'lock': false},
                "Couldn't send cam lock. Error ")

            sendPost(
                "/boundary_box",
                {'bbox': bbox},
                "Couldn't send boundary box. Error ")
        }
    }

    function handleMouseDown(e) {
        start = getRelativeMousePosition(e);
        clicked = true;
        sendPost(
            "/cam_lock",
            {'lock': true},
            "Couldn't send cam lock. Error ")
    }

}, false);




