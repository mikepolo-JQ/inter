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

const getReason = function (pk){

    let api_url = "/profile/reasons_and_back/1/"

    if(pk){
     api_url = "/profile/reasons_and_back/" + pk + "/";}

    fetch(api_url, {
        method: "POST",
    }).then(
        resp => {
            resp.json().then(
                resp_payload => {
                    if (resp_payload.ok) {
                        let contacts_pk = resp_payload.contacts_pk;
                        let contact_reasons = resp_payload.contact_reasons;
                        let contact_background = resp_payload.contact_background;


                        if(pk){
                        document.getElementById("avatar_" + pk).style.borderColor = resp_payload.color_to_pk;}
                        console.log(JSON.stringify(resp_payload));
                        console.log(JSON.stringify(resp_payload.color_to_pk + " is you"));
                        for(let i = 0; i < contacts_pk.length; ++i) {
                            let key_my = contacts_pk[i];

                            let elem = document.getElementById("reason_with_" + contacts_pk[i]);
                            if (elem){
                            elem.textContent = contact_reasons[key_my];}

                            let back = document.getElementById("contact_back_"+contacts_pk[i]);
                            if (back){
                            back.style.borderColor = contact_background[key_my];}
                        }
                    }else {
                        console.log(JSON.stringify(resp_payload));
                    }
                }
            );
        }
    );
}
