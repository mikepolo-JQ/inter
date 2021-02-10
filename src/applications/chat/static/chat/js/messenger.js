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

// const like = function (element, post_id) {
//     let api_url = "/blog/post/" + post_id + "/like/";
//
//     fetch(api_url, {
//         method: "POST",
//     }).then(
//         resp => {
//             resp.json().then(
//                 resp_payload => {
//                     if (resp_payload.ok) {
//                         element.firstElementChild.classList.toggle("like_red");
//                         element.lastElementChild.textContent = resp_payload.nr_likes;
//                     } else {
//                         console.log(JSON.stringify(resp_payload));
//                     }
//                 }
//             );
//         }
//     );
// }

