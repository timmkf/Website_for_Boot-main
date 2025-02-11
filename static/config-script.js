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
    console.log(IconInput.value)
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


const AusrichtungsButton = document.querySelector("#AusrichtungButton")
const AusrichtungInput = document.querySelector("#AusrichtungInput")

let AusrichtungText = "untenDick"

AusrichtungInput.value = AusrichtungText

function Ausrichtung(){
    if (AusrichtungText =="untenDick"){
        AusrichtungText ="obenDick"
    }else{
        AusrichtungText ="untenDick"
    }
    AusrichtungInput.value = AusrichtungText
    console.log(AusrichtungText)
}

AusrichtungsButton.onclick = Ausrichtung


const viererPyramide = document.querySelector("#viererPyramide")
const fünferPyramide = document.querySelector("#fünferPyramide")
const sechserPyramide = document.querySelector("#sechserPyramide")
const siebenerPyramide = document.querySelector("#siebenerPyramide")
const AllPyramide = document.querySelectorAll("#PyramidenSelector button")
const PyramidengroesseInput = document.querySelector("#Pyramidengroesse")

let Pyramidengroesse = 4

PyramidengroesseInput.value=Pyramidengroesse

function GroeßePyramide (PyramideNumber, PyramideText){
    AllPyramide.forEach(pyramide =>{
        pyramide.style.border = "none"
    })
    Pyramidengroesse = PyramideNumber
    let selectedPyramide = document.querySelector(`#${PyramideText}Pyramide`)
    selectedPyramide.style.border = "0.1vh solid blue"
    PyramidengroesseInput.value=Pyramidengroesse
    console.log(PyramidengroesseInput.value)
}

viererPyramide.onclick = () => GroeßePyramide(4, "vierer");
fünferPyramide.onclick = () => GroeßePyramide(5, "fünfer");
sechserPyramide.onclick = () => GroeßePyramide(6, "sechser");
siebenerPyramide.onclick = () => GroeßePyramide(7, "siebener");



const eineKarten = document.querySelector("#eineKarten")
const zweiKarten = document.querySelector("#zweiKarten")
const dreiKarten = document.querySelector("#dreiKarten")
const vierKarten = document.querySelector("#vierKarten")
const AllKarten = document.querySelectorAll("#AnzahlKartenpPSelector button")
const AnzahlKartenInput = document.querySelector("#AnzahlKarten")

let AnzahlKarten = 2

AnzahlKartenInput.value=AnzahlKarten

function KartenAnzahl (KartenNumber, KartenText){
    AllKarten.forEach(Karten =>{
        Karten.style.border = "none"
    })
    AnzahlKarten = KartenNumber
    let selectedKarten = document.querySelector(`#${KartenText}Karten`)
    selectedKarten.style.border = "0.1vh solid blue"
    AnzahlKartenInput.value=AnzahlKarten
    console.log(AnzahlKartenInput.value)
}

eineKarten.onclick = () => KartenAnzahl(1, "eine");
zweiKarten.onclick = () => KartenAnzahl(2, "zwei");
dreiKarten.onclick = () => KartenAnzahl(3, "drei");
vierKarten.onclick = () => KartenAnzahl(4, "vier");


const End1 = document.querySelector("#End1")
const End2 = document.querySelector("#End2")
const End3 =  document.querySelector("#End3")
const AllEnds = document.querySelectorAll("#EndBootSelector button")
const EndInput = document.querySelector("#EndBoot")

let Ends = 2

EndInput.value= Ends

function EndSelector(EndNumber){
    
    AllEnds.forEach(end => {
    end.style.border = "none"; // Entferne den Rahmen von jedem Icon
    });

    Ends = EndNumber
    let selectedEnd = document.querySelector(`#End${EndNumber}`)
    selectedEnd.style.border = "0.1vh solid blue"
    EndInput.value =Ends
    console.log(EndInput.value)
}
// Event-Listener für die Icons hinzufügen
End1.onclick = () => EndSelector(1);
End2.onclick = () => EndSelector(2);
End3.onclick = () => EndSelector(3);






