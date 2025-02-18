from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from flask_socketio import SocketIO, join_room, disconnect
from dbboot import save_user, create_room, users_collection, room_collection, find_Mitspieler_list, find_user_and_check_sid, update_sid, find_and_delete_disconnected_user, find_room_admin, change_roomAdmin, close_room, change_room_status, check_room_status, create_game_in_db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_PERMANENT'] = False  # Cookies sollen nur für die Sitzung gelten
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/in_Boot')
def in_Boot():
    return render_template('in_Boot.html')

@app.route('/joining', methods=['GET', 'POST'])
def joining():
    message =""
    if request.method == 'POST':
        existing_rooms = room_collection.distinct('RoomNumber')
        RoomNumber = int(request.form['LobyCode'])
        Username = request.form['Username']
        Mitspieler_Liste = find_Mitspieler_list(RoomNumber)
        Room_Status = check_room_status(RoomNumber)
        if RoomNumber in existing_rooms and Username not in Mitspieler_Liste and Room_Status == 'Loby':
            IconNumber = request.form['IconNumber']
            User_id = save_user(RoomNumber, Username, IconNumber)
            session['Username'] = Username
            session['RoomNumber'] = RoomNumber
            session['User_id'] = str(User_id)
            
            return redirect(url_for('loby', RoomNumber = RoomNumber))
        elif RoomNumber not in existing_rooms:
            message = "Diesen Room gibt es nicht!"
            return render_template('joining.html', message = message)
        elif Room_Status == 'InGame':
            message = "Der Room ist gerade mitten in einem Spiel!"
            return render_template('joining.html', message = message)
        elif Username in Mitspieler_Liste:
            message = "Ein Spieler in diesem Raum hat bereits diesen Nutzernamen, ändere deinen um beitreten zu können!"
            return render_template('joining.html', message = message)
    else:
        return render_template('joining.html', message = message)
    

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        
        Username = request.form['Username']
        IconNumber = request.form['IconNumber']
        AusrichtungInput = request.form['AusrichtungInput']
        Pyramidengroesse = request.form['Pyramidengroesse']
        AnzahlKarten = request.form['AnzahlKarten']
        EndBoot = request.form['EndBoot']
        RoomNumber_and_User_id = create_room(AusrichtungInput, Pyramidengroesse, AnzahlKarten, EndBoot, Username, IconNumber)
        RoomNumber = RoomNumber_and_User_id[0]
        User_id = RoomNumber_and_User_id[1]
        session['Username'] = Username
        session['RoomNumber'] = RoomNumber
        session['User_id'] = str(User_id)
        return redirect(url_for('loby', RoomNumber=RoomNumber))
    else:    
        return render_template('config.html')

@app.route('/loby<int:RoomNumber>')
def loby(RoomNumber):
    User_id = session.get('User_id')
    
    if  'Username' in session and 'RoomNumber' in session and 'User_id' in session and find_user_and_check_sid(User_id):
        # Daten aus der Session laden
        if int(RoomNumber) != int(session['RoomNumber']):
            #hier müsste dann noch die liste Aktualliesiert werden und die lobby und benutzer gelöscht werden
            session.clear() 
            return redirect(url_for('home'))
        Username = session.get('Username')
        RoomNumber = session.get('RoomNumber')
        
        # Die Daten an das Template übergeben
        return render_template('loby.html', Username=Username, RoomNumber=RoomNumber, User_id=User_id)
    else:
        session.clear()
        return redirect(url_for('home'))
    

@app.route('/leave')
def leave():
    session.clear()
    return redirect(url_for('home'))

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['Username'], data['RoomNumber']))
    join_room(data['RoomNumber'])
    Sid = request.sid
    update_sid(data, Sid)
    Mitspieler_Liste = find_Mitspieler_list(data['RoomNumber'])
    Admin_name_and_id = find_room_admin(data['RoomNumber'])
    Admin_name = Admin_name_and_id[0]
    Admin_id = str(Admin_name_and_id[1])
    socketio.emit('update_list', {'Mitspieler_Liste': Mitspieler_Liste, 'Admin_name': Admin_name, 'Admin_id': Admin_id}, room = data['RoomNumber']) 
    

@socketio.on('disconnect')
def handle_disconnect():
    Sid = request.sid
    RoomNumber = users_collection.find_one({'Sid': Sid})['RoomNumber']
    current_Admin_id = find_room_admin(RoomNumber)[1]
    disconnected_User_id = find_and_delete_disconnected_user(Sid)
    Mitspieler_Liste = find_Mitspieler_list(RoomNumber)
    session.clear()
    if Mitspieler_Liste and current_Admin_id == disconnected_User_id:
        change_roomAdmin(RoomNumber)
        Admin_name_and_id = find_room_admin(RoomNumber)
        Admin_name = Admin_name_and_id[0]
        Admin_id = str(Admin_name_and_id[1])
        socketio.emit('update_list', {'Mitspieler_Liste': Mitspieler_Liste, 'Admin_name': Admin_name, 'Admin_id': Admin_id}, room = str(RoomNumber))
        
    elif Mitspieler_Liste and current_Admin_id != disconnected_User_id:
        Admin_name_and_id = find_room_admin(RoomNumber)
        Admin_name = Admin_name_and_id[0]
        Admin_id = str(Admin_name_and_id[1])
        socketio.emit('update_list', {'Mitspieler_Liste': Mitspieler_Liste, 'Admin_name': Admin_name, 'Admin_id': Admin_id}, room = str(RoomNumber))

    else:
        close_room(RoomNumber)
    
    if check_room_status(RoomNumber) == 'InGame' and len(Mitspieler_Liste) <=1 :
        print(change_room_status(RoomNumber))


@socketio.on('game_start')
def handle_game_start(data):
    change_room_status(data['RoomNumber'])
    create_game_in_db(data['RoomNumber'])
    new_content = render_template('playground.html')
    socketio.emit('render_game_template',{'new_container': new_content}, room = data['RoomNumber'])
    

@app.route('/playground')
def playground():
    render_template('playground.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)

