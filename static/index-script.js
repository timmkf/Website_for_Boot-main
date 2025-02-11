const joinSession = document.querySelector("#joinSession");
const createSession = document.querySelector("#createSession");

joinSession.onclick = loadJoinSession;
createSession.onclick = loadCreateSession;

function loadJoinSession(){
    window.location = "/joining"
};

function loadCreateSession(){
    window.location = "/config"
}