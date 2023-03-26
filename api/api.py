from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo

app = Flask(__name__)
CORS(app)

users = {'piti': '1',
         'yosef': '1'}
players = []

# Connect to the MongoDB database
client = pymongo.MongoClient(
    "mongodb+srv://yotanel:1234@leagueoflegendsdb.qlqofrr.mongodb.net/?retryWrites=true&w=majority")
db = client['pt_table']


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = db.rooms.find({})
    result = []
    for room in rooms:
        print(len(room['players']))
        # if len(room['players']) == 1:
        #     print("to_be delete")
        #     # Delete room if it has no players
        #     db.rooms.delete_one({'_id': room['_id']})
        #     print("room %s deleted" % room)
        # else:
        result.append({
            'id': str(room['_id']),
            'name': room['name'],
            'admin': room['admin'],
            'players': room['players']
        })
    return jsonify(result)


@app.route('/api/create-room', methods=['POST'])
def create_room():
    # Get the user ID and room name from the request body
    data = request.get_json()
    print(data)
    name = data['name']
    admin = data['admin']
    # create new room document in the database
    result = db.rooms.insert_one({'name': name, 'admin': admin, 'players': [admin]})
    # return the ID of the new room
    return jsonify({'id': str(result.inserted_id)})


@app.route('/api/players', methods=['GET'])
def get_players():
    # Return the list of players in the room
    return jsonify({'players': players})


@app.route('/api/join', methods=['POST'])
def join_room():
    # Get the username from the request body
    username = request.json.get('username')
    if username:
        # Add the player to the list of players in the room
        players.append(username)
        print(players)
        return "Success", 200, {"Access-Control-Allow-Origin": "*"}
    else:
        return jsonify({'status': 'Error', 'message': 'No username provided'})


@app.route('/api/update_user_current_room', methods=['PUT'])
def update_user_current_room():
    user_name = request.json.get('user_name')
    room_id = request.json.get('current_room')
    print(room_id)
    users = db.users.find({})
    for user in users:
        print(user)
        if user == user_name:
            db.users.updateOne({current_room: room_id})
    users = db.users.find({})
    print("%%%%%%%%%%")
    for user in users:
        print(user)
    return "Success", 200, {"Access-Control-Allow-Origin": "*"}

@app.route('/api/leave-room', methods=['PUT'])
def leave_room():
    # Get the username from the request body
    username = request.json.get('username')
    if username:
        # Remove the player from the list of players in the room
        if username in players:
            players.remove(username)
            return "Success", 200, {"Access-Control-Allow-Origin": "*"}
        else:
            return jsonify({'status': 'Error', 'message': 'Player not in room'})
    else:
        return jsonify({'status': 'Error', 'message': 'No username provided'})


# Define route to handle login request
@app.route('/api/login', methods=['POST'])
def login():
    print("login function")
    # Get user name and password from request body
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    print(user_name, password)
    # Find user with matching user name and password
    matching_users = []
    response_data = "failed", 400

    if user_name in users:
        if users[user_name] == password:
            matching_users.append((user_name, users[user_name]))
            response_data = "Success", 200, {"Access-Control-Allow-Origin": "*"}
    return response_data


if __name__ == '__main__':
    app.run(debug=True)
