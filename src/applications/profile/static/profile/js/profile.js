openFeedback = function (elem, pk){
    document.getElementById("fdb_content_"+pk).classList.toggle("fdb_active");
}

openFeedbackinput = function (element){
    element.style.display = "none";
    document.getElementById("fdb-input").style.display = "block";
}

openFeedbackBox = function (){
    document.getElementById("feedback-box").style.display = "block";

    var offsetY = document.getElementById('fdb__title').offsetTop;
    window.scrollTo(0, offsetY);
}