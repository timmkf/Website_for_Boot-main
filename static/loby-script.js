const socket = io.connect("http://localhost:5000");

const game_container = document.querySelector('#game_container')



socket.on('connect',function (){
    console.log("User_id:", User_id)
    socket.emit('join_room',{
        Username: Username,
        RoomNumber: RoomNumber,
        User_id: User_id
    });
});

socket.on('update_list', function (data){
    const MitspielerListe = document.querySelector('#Mitspieler_Liste')
    MitspielerListe.innerHTML = '';
    for (let i=0 ; i < data.Mitspieler_Liste.length; i++){
        const li = document.createElement('li');
        li.textContent = data.Mitspieler_Liste[i]; // Benutzernamen in das Listenelement einfügen
        
        // Listenelement zur Liste hinzufügen
        MitspielerListe.appendChild(li)
    }
    console.log(data.Mitspieler_Liste)
    console.log(data.Admin)
    let AdminName = document.querySelector('#Admin')
    AdminName.textContent = data.Admin_name
    let Adminid = data.Admin_id
    if (Adminid === User_id && data.Mitspieler_Liste.length >1){
        let Start_Button = document.querySelector('#Start');
        Start_Button.style.backgroundColor = "green";
        Start_Button.style.pointerEvents = "auto";  
        Start_Button.onclick= Game_Start
    }else{
        let Start_Button = document.querySelector('#Start');
        Start_Button.style.backgroundColor = "gray";
        Start_Button.style.pointerEvents = "none";  }
;
});

document.addEventListener("click", function(event) {
    if (event.target.id === "Leave") {
        Leave();
    }})
function Leave(){
    window.location="/leave"
}

function Game_Start(){
    socket.emit('game_start',{RoomNumber: RoomNumber})
}

socket.on('render_game_template',function(data){
    game_container.innerHTML = data.new_container
    
})

socket.on('render_loby_template',function(data){
    game_container.innerHTML = data.new_container
}
)


