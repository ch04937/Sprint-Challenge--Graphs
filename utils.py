import random


class Queue:
    def __init__(self):
        self.storage = []
        self.size = 0

    def enqueue(self, val):
        self.size += 1
        self.storage.append(val)

    def dequeue(self):
        if self.size:
            self.size -= 1
            return self.storage.pop(0)
        else:
            return None


class Stack:
    def __init__(self):
        self.storage = []
        self.size = 0

    def push(self, val):
        self.size += 1
        self.storage.append(val)

    def pop(self):
        if self.size:
            self.size -= 1
            return self.storage.pop()
        else:
            return None


inverse_order = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}


class Graph:
    '''
    Represent rooms and connections
    '''

    def __init__(self):
        self.rooms = {}

    def add_rooms(self, room_id):
        '''
        Adds the rooms to the large graph
        '''
        if room_id not in self.rooms:
            self.rooms[room_id] = set()

    def get_exits(self, room_id):
        '''
        Return the exits to the room
        '''
        # print(self.rooms)
        return self.rooms[room_id]

    def create_world(self, room_graph):
        # create the rooms in the room_graph
        for room in room_graph:
            self.add_rooms(room)

        # connect rooms to graph
        for direction in room_graph:
            for d in room_graph[direction][-1]:
                # add the rooms to each other
                self.rooms[direction] = room_graph[direction][-1]
                # mark as unexplored
                self.rooms[direction][d] = '?'
