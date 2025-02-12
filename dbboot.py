from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson import ObjectId


client = MongoClient("mongodb+srv://timmarkg09:0nBA21wkS8uMq5c1@socketiotest.rsker.mongodb.net/?retryWrites=true&w=majority&appName=SocketIOTest")


Boot_db = client.get_database("Boot")

users_collection=Boot_db.get_collection("users")
room_collection=Boot_db.get_collection("rooms")
deck_collection=Boot_db.get_collection("deck")
games_collection=Boot_db.get_collection("games")

def save_user(RoomNumber, Username, IconNumber):
    User_id = users_collection.insert_one({'RoomNumber': int(RoomNumber), 'Username':Username, 'IconNumber': IconNumber, 'Sid': None})
    return User_id.inserted_id

def generate_unique_roomnumber():
    RoomNumber = 100000
    existing_rooms = room_collection.distinct('RoomNumber')
    while RoomNumber in existing_rooms:
        RoomNumber +=1
    return RoomNumber

def create_room(AusrichtungInput, Pyramidengroesse, AnzahlKarten, EndBoot, Username, IconNumber):
    RoomNumber = generate_unique_roomnumber()
    #es kann zu Problemen mit der RoomNumber kommen wenn später gleichzeitig einen room eröffnen, deswegen später room als id und room für save_user finden mithilfe von admin
    User_id = save_user(RoomNumber, Username, IconNumber)
    room_collection.insert_one({'RoomNumber':RoomNumber, 'AusrichtungInput':AusrichtungInput, 'Pyramidengroesse':Pyramidengroesse, 'AnzahlKarten':AnzahlKarten, 'EndBoot':EndBoot, 'Admin':User_id, 'Status': 'Loby' })
    return RoomNumber, User_id

def find_user_and_check_sid(User_id):
    # Benutzer mit User_id finden und nur das Feld 'Sid' abfragen
    user = users_collection.find_one({'_id': ObjectId(User_id)}, {'Sid': 1})
    print(user)
    # Prüfen, ob der Benutzer existiert und ob 'Sid' gefüllt ist
    if user and user.get('Sid') or user is None:  # Wenn der Benutzer existiert und 'Sid' nicht leer ist
        print('darf nicht rein')
        return False
    else:  # Wenn der Benutzer nicht existiert oder 'Sid' leer ist
        print('darf  rein')
        return True
    

def update_sid(data, Sid):
    User_id = ObjectId(data['User_id'])
    users_collection.update_one({'_id': User_id}, 
                                {'$set': {'Sid': Sid}})

def find_Mitspieler_list(RoomNumber):
    Mitspieler_list = users_collection.find({'RoomNumber': int(RoomNumber)}, {'_id': 0, 'Username': 1})
    return [user['Username'] for user in Mitspieler_list]

def find_and_delete_disconnected_user(Sid):
    User_id = users_collection.find_one({'Sid': Sid},{'_id': 1})
    users_collection.delete_one({'Sid': Sid})
    return User_id['_id']

def change_roomAdmin(RoomNumber):
    NewAdmin_id = users_collection.find_one({"RoomNumber": RoomNumber})['_id']
    room_collection.find_one_and_update({'RoomNumber': RoomNumber},{"$set": {"Admin": NewAdmin_id}})
    
    
def find_room_admin(RoomNumber):
    Room = room_collection.find_one({'RoomNumber': int(RoomNumber)})
    Admin_id = Room['Admin']
    Admin_name = users_collection.find_one({'_id': Admin_id})['Username']
    return Admin_name, Admin_id

def change_room_status(RoomNumber):
    room_collection.find_one_and_update({'RoomNumber': int(RoomNumber)},{'$set': {'Status': 'InGame'}})

def check_room_status(RoomNumber):
    Room_status = room_collection.find_one({'RoomNumber': RoomNumber})
    if Room_status:
        return(Room_status['Status'])
    else:
        return(False)

def create_game_in_db(RoomNumber):
    Mitspieler_list = find_Mitspieler_list(RoomNumber)
    games_collection.insert_one({'_id': int(RoomNumber), 'players': Mitspieler_list, 'status': 'running', "turn": Mitspieler_list[0]})

def fill_deck():
    deck_collection.insert_many([{
  "_id": "skat_standard",
  "cards": [
    {"suit": "herz", "rank": "ass"},
    {"suit": "herz", "rank": "10"},
    {"suit": "herz", "rank": "könig"},
    {"suit": "herz", "rank": "dame"},
    {"suit": "herz", "rank": "bube"},
    {"suit": "herz", "rank": "9"},
    {"suit": "herz", "rank": "8"},
    {"suit": "herz", "rank": "7"},
    
    {"suit": "karo", "rank": "ass"},
    {"suit": "karo", "rank": "10"},
    {"suit": "karo", "rank": "könig"},
    {"suit": "karo", "rank": "dame"},
    {"suit": "karo", "rank": "bube"},
    {"suit": "karo", "rank": "9"},
    {"suit": "karo", "rank": "8"},
    {"suit": "karo", "rank": "7"},
    
    {"suit": "pik", "rank": "ass"},
    {"suit": "pik", "rank": "10"},
    {"suit": "pik", "rank": "könig"},
    {"suit": "pik", "rank": "dame"},
    {"suit": "pik", "rank": "bube"},
    {"suit": "pik", "rank": "9"},
    {"suit": "pik", "rank": "8"},
    {"suit": "pik", "rank": "7"},
    
    {"suit": "kreuz", "rank": "ass"},
    {"suit": "kreuz", "rank": "10"},
    {"suit": "kreuz", "rank": "könig"},
    {"suit": "kreuz", "rank": "dame"},
    {"suit": "kreuz", "rank": "bube"},
    {"suit": "kreuz", "rank": "9"},
    {"suit": "kreuz", "rank": "8"},
    {"suit": "kreuz", "rank": "7"}
  ]
},{
  "_id": "skat_2decks",
  "cards": [
    {"suit": "herz", "rank": "ass"},
    {"suit": "herz", "rank": "10"},
    {"suit": "herz", "rank": "könig"},
    {"suit": "herz", "rank": "dame"},
    {"suit": "herz", "rank": "bube"},
    {"suit": "herz", "rank": "9"},
    {"suit": "herz", "rank": "8"},
    {"suit": "herz", "rank": "7"},
    
    {"suit": "karo", "rank": "ass"},
    {"suit": "karo", "rank": "10"},
    {"suit": "karo", "rank": "könig"},
    {"suit": "karo", "rank": "dame"},
    {"suit": "karo", "rank": "bube"},
    {"suit": "karo", "rank": "9"},
    {"suit": "karo", "rank": "8"},
    {"suit": "karo", "rank": "7"},
    
    {"suit": "pik", "rank": "ass"},
    {"suit": "pik", "rank": "10"},
    {"suit": "pik", "rank": "könig"},
    {"suit": "pik", "rank": "dame"},
    {"suit": "pik", "rank": "bube"},
    {"suit": "pik", "rank": "9"},
    {"suit": "pik", "rank": "8"},
    {"suit": "pik", "rank": "7"},
    
    {"suit": "kreuz", "rank": "ass"},
    {"suit": "kreuz", "rank": "10"},
    {"suit": "kreuz", "rank": "könig"},
    {"suit": "kreuz", "rank": "dame"},
    {"suit": "kreuz", "rank": "bube"},
    {"suit": "kreuz", "rank": "9"},
    {"suit": "kreuz", "rank": "8"},
    {"suit": "kreuz", "rank": "7"},

    {"suit": "herz", "rank": "ass"},
    {"suit": "herz", "rank": "10"},
    {"suit": "herz", "rank": "könig"},
    {"suit": "herz", "rank": "dame"},
    {"suit": "herz", "rank": "bube"},
    {"suit": "herz", "rank": "9"},
    {"suit": "herz", "rank": "8"},
    {"suit": "herz", "rank": "7"},
    
    {"suit": "karo", "rank": "ass"},
    {"suit": "karo", "rank": "10"},
    {"suit": "karo", "rank": "könig"},
    {"suit": "karo", "rank": "dame"},
    {"suit": "karo", "rank": "bube"},
    {"suit": "karo", "rank": "9"},
    {"suit": "karo", "rank": "8"},
    {"suit": "karo", "rank": "7"},
    
    {"suit": "pik", "rank": "ass"},
    {"suit": "pik", "rank": "10"},
    {"suit": "pik", "rank": "könig"},
    {"suit": "pik", "rank": "dame"},
    {"suit": "pik", "rank": "bube"},
    {"suit": "pik", "rank": "9"},
    {"suit": "pik", "rank": "8"},
    {"suit": "pik", "rank": "7"},
    
    {"suit": "kreuz", "rank": "ass"},
    {"suit": "kreuz", "rank": "10"},
    {"suit": "kreuz", "rank": "könig"},
    {"suit": "kreuz", "rank": "dame"},
    {"suit": "kreuz", "rank": "bube"},
    {"suit": "kreuz", "rank": "9"},
    {"suit": "kreuz", "rank": "8"},
    {"suit": "kreuz", "rank": "7"}
  ]
}])   




def close_room(RoomNuber):
    room_collection.delete_one({'RoomNumber': RoomNuber})

def delete_all_useres():
    users_collection.delete_many({})

def delete_all_rooms():
    room_collection.delete_many({})
    
#delete_all_useres()

#delete_all_rooms()

#fill_deck()

#save_user("3", "Tim", "1")

#create_room("untenDick", "vierer", "eine", 2, "DFR", 3)

#def get_user(username):
 #   user_data = users_collection.find_one({'_id': username})
  #  if user_data:
   #     return User(user_data['_id'], user_data['email'], user_data['password'])
    #else:
     #   return None