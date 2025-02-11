const home = document.querySelector("#Home");
const Icon1 = document.querySelector("#Icon1");
const Icon2 = document.querySelector("#Icon2");
const Icon3 = document.querySelector("#Icon3");
const Icon4 = document.querySelector("#Icon4");
const Icon5 = document.querySelector("#Icon5");
const Icon6 = document.querySelector("#Icon6");
const Icon7 = document.querySelector("#Icon7");
const Icon8 = document.querySelector("#Icon8");
const AllIcons = document.querySelectorAll("#IconSelector button");

let IconInput = document.querySelector("#IconNumber")
let SelectedIcon = 1;

IconInput.value =SelectedIcon

home.onclick = goHome;

function goHome(){
    window.location = "/"
}

function SelectIcon(IconNumber){
    
    AllIcons.forEach(icon => {
    icon.style.border = "none"; // Entferne den Rahmen von jedem Icon
    });

    SelectedIcon = IconNumber
    let selectedIcon = document.querySelector(`#Icon${IconNumber}`)
    selectedIcon.style.border = "0.1vh solid blue"
    IconInput.value =SelectedIcon
}
// Event-Listener für die Icons hinzufügen
Icon1.onclick = () => SelectIcon(1);
Icon2.onclick = () => SelectIcon(2);
Icon3.onclick = () => SelectIcon(3);
Icon4.onclick = () => SelectIcon(4);
Icon5.onclick = () => SelectIcon(5);
Icon6.onclick = () => SelectIcon(6);
Icon7.onclick = () => SelectIcon(7);
Icon8.onclick = () => SelectIcon(8);


