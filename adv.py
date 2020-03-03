from room import Room
from player import Player
from world import World
from utils import Queue, inverse_order, Graph

import random
from ast import literal_eval

# Load world
world = World()
g = Graph()
traversal_path = []

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# initiate player to starting room
current_room = world.starting_room
room_id = current_room.id  # current rooms id

g.create_world(room_graph)


def player_travel(direction):
    return player.travel(direction)


def get_directions():
    # track unexplored exits
    path = []

    for exits in player.current_room.get_exits():

        if g.rooms[player.current_room.id][exits] == '?':
            path.append(exits)
    return random.choice(path)


def bfs_traverse_dungeon(rooms_id):
    # Fill this out with directions to walk
    # Create an empty queue
    q = Queue()
    # enqueue rooms
    q.enqueue([rooms_id])
    # store visited in an empty set
    visited = set()
    # while the dequeue is not empty...
    while q.size > 0:
        # Deque ,the first path
        v = q.dequeue()
        # check if the last room is not been visited
        last = v[-1]
        # get all possible exits to the back of the queue
        # print(g.get_exits(last))
        # if we find and exit in the room
        if list(g.rooms[last].values()).count('?') != 0:
            # add the path to unplored
            return v
        if last not in visited:
            # mark as visited
            visited.add(last)
            for next_room in g.rooms[last].values():
                new_list = v.copy()
                new_list.append(next_room)
                q.enqueue(new_list)


# a visited set
visited = set()

# while the lenght of visited is not the length of room_graph
while len(visited) < len(room_graph):
    if list(g.rooms[player.current_room.id].values()).count('?') != 0:
        current = player.current_room.id
        # get random exit
        random_exit = get_directions()
        # add all directions that have '?' to the unexplored array
        player_travel(random_exit)
        traversal_path.append(random_exit)

        # if the current room has not been visited
        if current not in visited:
            # add it to the visited set
            visited.add(current)
        # assign rooms

        g.rooms[current][random_exit] = player.current_room.id
        g.rooms[player.current_room.id][inverse_order[random_exit]] = current
    else:
        # backtrack and find other rooms
        reverse_path = bfs_traverse_dungeon(player.current_room.id)
        # for each room id
        if reverse_path == None:
            break
        for each_room in reverse_path:
            # get the direction of current room
            for directions in g.rooms[player.current_room.id]:
                # check if rooms match
                if g.rooms[player.current_room.id][directions] == each_room:
                    # travel in that direction
                    player.travel(directions)
                    traversal_path.append(directions)
                    break


visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room.id)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room.id)

# TRAVERSAL TEST
if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
