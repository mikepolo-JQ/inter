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



const getReason = function (){
    let api_url = "/profile/reasons/";

    fetch(api_url, {
        method: "POST",
    }).then(
        resp => {
            resp.json().then(
                resp_payload => {
                    if (resp_payload.ok) {
                        let contacts_pk = resp_payload.contacts_pk;
                        let contact_reasons = resp_payload.contact_reasons;

                        console.log(JSON.stringify(contact_reasons["pk1"]));
                        for(let i = 0; i < contacts_pk.length; ++i) {
                            let key_my = "pk" + contacts_pk[i];
                            let elem = document.getElementById("reason_with_" + contacts_pk[i]);
                            elem.textContent = contact_reasons[key_my];
                            console.log(contact_reasons[key_my]);
                        }
                    }else {
                        console.log(JSON.stringify(resp_payload));
                    }
                }
            );
        }
    );
}

