import time
import requests
import hashlib
import json
import sys
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

        cooldown = json_response['cooldown']

        time.sleep(cooldown)

        self.current_room_data = json_response
    



    def proof_of_work(self, last_proof, difficulty):
        print('Running proof of work')
        proof = 0
        while self.valid_proof(last_proof, proof, difficulty) == False:
            proof += 1

        print('Proof found: ', proof)
        return proof


    def valid_proof(self, last_proof, proof, difficulty):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:difficulty] == '0' * difficulty

    def mine(self):
        r = requests.get(
            "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/",
            headers=token_data
        )
        # Handle non-json response
        try:
            json_response = r.json()
            print('Last Proof response: ', json_response)
            last_proof = json_response['proof']
            difficulty = json_response['difficulty']
            cooldown = json_response['cooldown']
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)

        # Get the string from `last_proof` and use it to look for a new proof
        new_proof = self.proof_of_work(last_proof, difficulty)

        # When found, POST it to the server {"proof": new_proof}
        post_data = {"proof": new_proof}

        print('Post data supposed to be: ', json.dumps(post_data))

        mine_res = requests.post(
            "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/",
            json=post_data,
            headers=token_data
        )

        # min_res_json = mine_res.json()

        print('Mine response: ', mine_res.json())

        time.sleep(cooldown)
