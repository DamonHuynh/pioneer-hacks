const addEventDialog = document.querySelector("#addEvent");
const addMemberDialog = document.querySelector("#addMember"); 
const addMemberBtn = document.querySelector(".addMember");
const addEventBtn = document.querySelector(".addEvent");
const memberForm = document.querySelector("#member");
const eventForm = document.querySelector("#event");



let show = true;
function showCheckboxes() {
    let checkboxes = document.getElementById("checkBoxes");

    if (show) {
        checkboxes.style.display = "block";
        show = false;
    } else {
        checkboxes.style.display = "none";
        show = true;
    }
}

function revealForm(addBtn, form, dialog){
 addBtn.addEventListener("click", () => {
    form.reset();
    dialog.showModal();
});
}

revealForm(addMemberBtn, memberForm, addMemberDialog);
revealForm(addEventBtn, eventForm, addEventDialog);