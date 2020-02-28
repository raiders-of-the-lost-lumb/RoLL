import time
import requests
import json
from dotenv import load_dotenv
from ignore import PLAYER_TOKEN

token_item = f"Token {PLAYER_TOKEN}"
token_data = {'Authorization': token_item}


def initialize():
    response = requests.get(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/init',
        headers=token_data
    )

    json_response = response.json()
    print(json_response)

    cooldown = json_response['cooldown']
    time.sleep(cooldown)


def pickup():
    item_data = {"name": "treasure"}
    response = requests.post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/take',
        data=json.dumps(item_data),
        headers=token_data
    )

    json_response = response.json()
    print(json_response)

    cooldown = json_response['cooldown']

    time.sleep(cooldown)


def drop():
    item_data = {"name": "treasure"}
    response = requests.post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/drop',
        data=json.dumps(item_data),
        headers=token_data
    )

    json_response = response.json()
    print(json_response)

    cooldown = json_response['cooldown']

    time.sleep(cooldown)

# def examine(object):


# def change_name(name):


# def pray():


# def fly(direction):


# def dash(direction, num_rooms, ids):


# def carry(item):


# def receive(item):


# def warp():


# def recall():
#     response = requests.post(
#         'https://lambda-treasure-hunt.herokuapp.com/api/adv/recall',
#         headers=token_data
#     )

#     json_response = response.json()
#     print(json_response)

#     cooldown = json_response['cooldown']
#     time.sleep(cooldown)

# def return_to_shop():
#     recall()
#     move('w')


# def mine(proof):


# def last_proof():


# def transmogrify(item):


# def balance()


def sell():
    item_data = {"name": "treasure"}
    response = requests.post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell',
        data=json.dumps(item_data),
        headers=token_data
    )

    json_response = response.json()
    print(json_response)

    message = json_response['messages']
    cooldown = json_response['cooldown']

    time.sleep(cooldown)


def status():
    response = requests.post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/status',
        headers=token_data
    )

    json_response = response.json()
    print(json_response)

    cooldown = json_response['cooldown']

    time.sleep(cooldown)


def move(direction):  # Good move("n,s,e,w") returns True if items in room
    move_data = {"direction": direction}
    response = requests.post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/move',
        data=json.dumps(move_data),
        headers=token_data
    )

    json_response = response.json()
    print(json_response)

    items = json_response['items']
    cooldown = json_response['cooldown']

    time.sleep(cooldown)

    return len(items) > 0

