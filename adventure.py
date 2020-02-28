from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

map_file = "/map.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

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
        self.rooms = {}
        self.player = Player()
        self.last_room = self.player.current_room.id
        self.travel_and_map(None, True)

    def travel_and_map(self, curr_direction, first_room=False):
        self.last_room = self.player.current_room.id

        if not first_room:
            self.player.travel(curr_direction)

        room_id = self.player.current_room.id

        if room_id not in self.rooms:
            directions = self.player.current_room.get_exits()
            self.rooms[room_id] = {}
            for direction in directions:
                self.rooms[room_id][direction] = '?'

        if curr_direction != None:
            if curr_direction == 'n':
                self.rooms[room_id]['s'] = self.last_room
            elif curr_direction == 's':
                self.rooms[room_id]['n'] = self.last_room
            elif curr_direction == 'e':
                self.rooms[room_id]['w'] = self.last_room
            elif curr_direction == 'w':
                self.rooms[room_id]['e'] = self.last_room
            self.rooms[self.last_room][curr_direction] = room_id
    
    def list_all_unexplored(self):
        curr_room = self.rooms[self.player.current_room.id]
        unexplored_directions = []
        for direction in curr_room:
            if curr_room[direction] == '?':
                unexplored_directions.append(direction)
        return unexplored_directions
    
    def explore(self):
        curr_unexplored = self.list_all_unexplored()
        while(len(curr_unexplored) > 0):
            rand_direction = curr_unexplored[random.randint(0, len(curr_unexplored) - 1)]
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
            for direction in self.rooms[curr_room]:
                directed_location = self.rooms[curr_room][direction]
                if directed_location == '?':
                    for vector in curr_path:
                        if vector[1] != None:
                            self.player.travel(vector[1])
                    return
                if directed_location not in visited:
                    path_copy = curr_path[:]
                    path_copy.append((directed_location, direction))
                    queue.enqueue(path_copy)
    
    def find_all_rooms(self):
        while True:
            self.explore()
            if len(self.rooms) == len(room_graph):
                return
            self.backtrack()
    

adv_graph = Adv_Graph()
adv_graph.find_all_rooms()
