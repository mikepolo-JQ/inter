$(document).ready(function (){
    $("#rating").on("click", function (e){
        e.preventDefault();

        let fdbBox = document.getElementById("feedback-box");

        fdbBox.style.display = "block";

        let top = $("#fdb__title").offset().top;
        console.log(top);
        $("html, body").animate({
            scrollTop: top
        }, 1000)
        fdbBox.classList.add("feedbacks_box_active")
    })
})