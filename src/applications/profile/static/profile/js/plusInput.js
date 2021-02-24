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


    console.log(parseInt(moveElements[0].style.top) - 10)
    for(let i = 0; i < moveElements.length; ++i){
        let elementTopValue = parseInt(moveElements[i].style.top)
        if (elementTopValue){
            elementTopValue += 27;
        }else { elementTopValue = topValue}
        moveElements[i].style.top = elementTopValue + "px";
    }

    setTimeout(f, 600);
}

