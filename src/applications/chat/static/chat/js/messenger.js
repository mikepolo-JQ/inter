// document.oncontextmenu = function (){
//     return false;
// }

window.onload = function(){
    let messages = document.getElementById("messages")
    var offsetY = document.getElementById('start_page').offsetTop;
    messages.scrollTo(0, offsetY);
}

openMenu = function (element) {
    element.firstElementChild.classList.toggle("msg-menu-active");

}

chatUpdate = function (chat_pk, last_message_createtime) {
    // let api_url = "/messenger/chat/" + chat_pk + "/update/" + last_message_createtime + "/";
    console.log("YES");

    // fetch(api_url, {
    //     method: "POST",
    // }).then(
    //     resp => {
    //         resp.json().then(
    //             resp_payload => {
    //                 if (resp_payload.ok) {
    //                     console.log(JSON.stringify(resp_payload));
    //                 } else {
    //                     console.log(JSON.stringify(resp_payload));
    //                 }
    //             }
    //         );
    //     }
    // );
}

