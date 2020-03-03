from room import Room
from player import Player
from world import World

import actions
import random
import json
from ast import literal_eval

# Load world
world = World()

map_file = "map.json"

with open(map_file) as json_file:
    data = json.load(json_file)
    map_data = {}

    for map_id in data:
        map_data[int(map_id)] = data[map_id]

world.load_graph(map_data)

# Used in BFS for backtracking


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

# Primary class used to traverse
# !!! Implement 'free roam' form of traversal for after island is fully mapped, take 'wise explorer' into account


class Adv_Graph:
    def __init__(self):
        self.rooms = world.rooms
        self.player = Player()
        self.last_room = self.player.current_room
        self.travel_and_map(None, True)

    def travel_and_map(self, curr_direction, first_room=False):
        self.last_room = self.player.current_room

        if not first_room:
            # Travelling should store all room data in some variable, maybe on the player
            self.player.travel(curr_direction)

        # Should be pulled from room data variable
        room_id = self.player.current_room_data['room_id']

        if room_id not in self.rooms:  # If not in rooms, it hasn't been put in the world map yet, so we'll need to make a new Room, put it in the map

            room_data = self.player.current_room_data
            coordinates = eval(room_data['coordinates'])
            # Input all room data into a new Room object and set it to its ID in the rooms object
            self.rooms[room_id] = Room(room_data['room_id'], room_data['title'],
                                       room_data['description'], coordinates[0], coordinates[1])
            for exit_dir in room_data['exits']:
                if exit_dir == 'n':
                    self.rooms[room_id].n_to = '?'
                if exit_dir == 's':
                    self.rooms[room_id].s_to = '?'
                if exit_dir == 'e':
                    self.rooms[room_id].e_to = '?'
                if exit_dir == 'w':
                    self.rooms[room_id].w_to = '?'

        self.writeMap(self.rooms)

        self.player.current_room = self.rooms[room_id]

        if curr_direction != None:
            self.last_room.connect_rooms(curr_direction, self.rooms[room_id])

    def writeMap(self, room_dict):
        data = {}

        for room in room_dict:
            data[room] = room_dict[room].__dict__

        with open("map.json", "w") as outfile:
            json.dump(data, outfile)

    def list_all_unexplored(self):
        curr_room = self.rooms[self.player.current_room.id]
        unexplored_directions = []
        print('-- Getting All Room Exits: ', curr_room.get_exits())
        for direction in curr_room.get_exits():
            if curr_room.get_room_in_direction(direction) == '?':
                unexplored_directions.append(direction)
        print('-- Listing All Unexplored Directions: ', unexplored_directions)
        return unexplored_directions

    def explore(self):
        curr_unexplored = self.list_all_unexplored()
        while(len(curr_unexplored) > 0):
            rand_direction = curr_unexplored[random.randint(
                0, len(curr_unexplored) - 1)]
            self.travel_and_map(rand_direction)
            curr_unexplored = self.list_all_unexplored()

    def backtrack(self):
        queue = Queue()
        queue.enqueue([(self.player.current_room.id, None)])
        visited = set()

        while queue.size() > 0:
            curr_path = queue.dequeue()
            curr_vector = curr_path[-1]
            curr_room = curr_vector[0]
            visited.add(curr_room)
            print('-- Finding exits in backtrack: ',
                  self.rooms[curr_room].get_exits())
            for direction in self.rooms[curr_room].get_exits():
                directed_location = self.rooms[curr_room].get_room_in_direction(
                    direction)
                if directed_location == '?':
                    for vector in curr_path:
                        if vector[1] != None:
                            self.player.travel(vector[1])
                            self.player.current_room = self.rooms[self.player.current_room_data['room_id']]
                    return
                if directed_location not in visited:
                    path_copy = curr_path[:]
                    path_copy.append((directed_location, direction))
                    queue.enqueue(path_copy)

    def findRoom(self, target_id):
        queue = Queue()
        queue.enqueue([(self.player.current_room.id, None)])
        visited = set()

        while queue.size() > 0:
            curr_path = queue.dequeue()
            curr_vector = curr_path[-1]
            curr_room = curr_vector[0]
            visited.add(curr_room)
            for direction in self.rooms[curr_room].get_exits():
                directed_location = self.rooms[curr_room].get_room_in_direction(
                    direction)
                if directed_location == target_id:
                    print("Current Path", curr_path)
                    for vector in curr_path:
                        if vector[1] != None:
                            self.player.travel(vector[1])
                            self.player.current_room = self.rooms[self.player.current_room_data['room_id']]
                    self.player.travel(direction)
                    self.player.current_room = self.rooms[self.player.current_room_data['room_id']]
                    return
                if directed_location not in visited:
                    path_copy = curr_path[:]
                    path_copy.append((directed_location, direction))
                    queue.enqueue(path_copy)

    def find_all_rooms(self):
        while True:
            self.explore()
            if len(self.rooms) == 500:
                return
            self.backtrack()

    def traverse(self):
        self.find_all_rooms()

        while True:
            curr_exits = self.player.current_room.get_exits()
            rand_direction = curr_exits[random.randint(0, len(curr_exits) - 1)]
            self.last_room = self.player.current_room
            self.player.travel(rand_direction)
            self.player.current_room = self.rooms[self.player.current_room_data['room_id']]

            playerDict = {}
            playerDict = actions.status()

            # If player's encumbrance is over 1 try and sell to the shop, it seems like you can only sell one item at a time with how we have it setup
            # if playerDict["encumbrance"] >= 1:
            #     self.findRoom(1)
            if "player" not in playerDict["name"]:
                self.findRoom(22)

            # If room id is 1, sell to vendor
            if self.player.current_room_data["room_id"] == 1:
                actions.sell()

            if "shrine" in self.player.current_room_data["description"]:
                actions.pray()

            # If player has less than an 8 encumbrance and there are items in the room pick them up
            # if playerDict["encumbrance"] < 8 and len(self.player.current_room_data['items']) > 0:
            #     actions.pickup()


adv_graph = Adv_Graph()
adv_graph.traverse()
