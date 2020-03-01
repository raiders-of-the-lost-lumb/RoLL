import time
import requests
import json
from ignore import PLAYER_TOKEN

token_item = f"Token {PLAYER_TOKEN}"
token_data = {'Authorization': token_item}

class Player:
    def __init__(self):
        self.current_room = None
        self.current_room_data = self.initialize() # Input current room request in here. Status request finding room id or something
    
    def initialize(self):
        response = requests.get(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/init',
            headers=token_data
        )

        json_response = response.json()
        print('Initialize Response: ', json_response)

        cooldown = json_response['cooldown']
        time.sleep(cooldown)

        return json_response

    def travel(self, direction): # Good move("n,s,e,w") returns room
        move_data = {"direction": direction}

        possible_next_room = self.current_room.get_room_in_direction(direction)
        if isinstance(possible_next_room, int):
            move_data["next_room_id"] = str(possible_next_room)

        response = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/move',
            data=json.dumps(move_data),
            headers=token_data
        )

        json_response = response.json()
        print('Move Response: ', json_response)

        items = json_response['items']
        cooldown = json_response['cooldown']

        time.sleep(cooldown)

        self.current_room_data = json_response
    