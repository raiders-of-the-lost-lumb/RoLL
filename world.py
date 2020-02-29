from room import Room
import random
import math

class World:
    def __init__(self):
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0
    def load_graph(self, room_graph):
        # num_rooms = len(room_graph)
        # rooms = [None] * num_rooms
        grid_size = 1
        for i in room_graph:
            # x = room_graph[i][0][0]
            grid_size = max(grid_size, room_graph[i]["x"], room_graph[i]["y"])
            self.rooms[i] = Room(i, room_graph[i]["name"], room_graph[i]["description"],room_graph[i]["x"], room_graph[i]["y"])

            self.rooms[i].n_to = room_graph[i]["n_to"]
            self.rooms[i].s_to = room_graph[i]["s_to"]
            self.rooms[i].e_to = room_graph[i]["e_to"]
            self.rooms[i].w_to = room_graph[i]["w_to"]
            
        # self.room_grid = []
        # grid_size += 1
        # self.grid_size = grid_size
        # for i in range(0, grid_size):
        #     self.room_grid.append([None] * grid_size)
        # for room_id in room_graph:
        #     room = self.rooms[room_id]
        #     self.room_grid[room.x][room.y] = room
        #     if 'n' in room_graph[room_id][1]:
        #         self.rooms[room_id].connect_rooms('n', self.rooms[room_graph[room_id][1]['n']])
        #     if 's' in room_graph[room_id][1]:
        #         self.rooms[room_id].connect_rooms('s', self.rooms[room_graph[room_id][1]['s']])
        #     if 'e' in room_graph[room_id][1]:
        #         self.rooms[room_id].connect_rooms('e', self.rooms[room_graph[room_id][1]['e']])
        #     if 'w' in room_graph[room_id][1]:
        #         self.rooms[room_id].connect_rooms('w', self.rooms[room_graph[room_id][1]['w']])