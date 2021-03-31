openFeedback = function (elem, pk){
    document.getElementById("fdb_content_"+pk).classList.toggle("fdb_active");
}

openFeedbackinput = function (element){
    element.style.display = "none";
    document.getElementById("fdb-input").style.display = "block";
}

plusInput = function (element){

    element.style.display = "none";

    let topValue, doActiveId, classToMove;

    if(element.id.startsWith("need")) {
        if (element.id.startsWith("need_first")) {
            topValue = -27;
            doActiveId = "second_input_need";
            classToMove = "input_move";
        } else {
            doActiveId = "third_input_need";
            classToMove = "input_move";
        }
    }else{
        if (element.id.startsWith("provide_first")) {
            doActiveId = "second_input_provide";
            classToMove = "input_move_provide";
        } else {
            doActiveId = "third_input_provide";
            classToMove = "input_move_provide";
        }
    }

    function f() {
        document.getElementById(doActiveId).classList.toggle("active_input");
    }

    let moveElements = document.getElementsByClassName(classToMove)

    for(let i = 0; i < moveElements.length; ++i){
        let elementTopValue = parseInt(moveElements[i].style.top)
        if (elementTopValue){
            elementTopValue += 27;
        }else { elementTopValue = topValue}
        moveElements[i].style.top = elementTopValue + "px";
    }

    setTimeout(f, 600);
}

// function to get profile image style,
// reasons of contacts and view active input
const getProfilePageStyles = function (pk){

    let api_url = "/profile/reasons_and_back/1/"

    if(pk){
     api_url = "/profile/reasons_and_back/" + pk + "/";}

    fetch(api_url, {
        method: "POST",
    }).then(
        resp => {
            resp.json().then(
                resp_payload => {
                    //view active input
                    let noActiveInputList = [
                        ["second_input_need_help", "need_first_plus"],
                        ["third_input_need_help", "need_second_plus"],
                        ["second_input_provide_help", "provide_first_plus"],
                        ["third_input_provide_help" , "provide_second_plus"],
                    ]

                    for(let [key, value] of noActiveInputList){
                        let noActiveInput = document.getElementById(key);
                        if(noActiveInput && noActiveInput.value){
                            document.getElementById(value).click()
                        }
                    }

                    // get profile avatar styles and reasons of contacts
                    if (resp_payload.ok) {
                        let contacts_pk = resp_payload.contacts_pk;
                        let contact_reasons = resp_payload.contact_reasons;
                        let contact_background = resp_payload.contact_background;

                        if(pk){
                        document.getElementById("avatar_" + pk).style.borderColor = resp_payload.color_to_pk;}

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
