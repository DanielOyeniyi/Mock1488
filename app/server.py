import json
import os
import random

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#FFD700", "headType": "beluga", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    next_move(data)
    print("MOVE:", json.dumps(data))

    move = next_move(data)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


num_loops = 0

# we want to map out all the possible moves. recursion 
# sounds like a great way to do it
# first take into account all of our moves then 
# we take into account the possible moves of other snakes
def next_move(data):
    global num_loops
    num_loops = 0
    return value(data)


# dict, dict -> string
# function checks all the moves up to a certain depth
def value(data):
    head = data["you"]["body"][0]
    snakes = make_snakes(data)
    walls = make_walls(data)
    food = make_food(data)
    
    
    right_block = {"x": head["x"] + 1, "y": head["y"]}
    left_block = {"x": head["x"] - 1, "y": head["y"]}
    down_block = {"x": head["x"], "y": head["y"] + 1}
    up_block = {"x": head["x"], "y": head["y"] - 1}
    
    
    right_val = 0
    left_val = 0
    down_val = 0
    up_val = 0
    
    right_val = value_helper(data, snakes, walls, food, 0,right_block)
    left_val = value_helper(data, snakes, walls, food, 0,left_block)
    down_val = value_helper(data, snakes, walls, food, 0,down_block)
    up_val = value_helper(data, snakes, walls, food, 0,up_block)
    
    print(right_val)
    print(left_val)
    print(down_val)
    print(up_val)
    
    print(num_loops)
    # might need a hint of randomness if there is more than 
    # one max val 
    max_val = max(right_val, left_val, down_val, up_val)
    if (max_val == right_val):
        return "right"
    elif (max_val == left_val):
        return "left"
    elif (max_val == down_val):
        return "down"
    else:
        return "up"

# this is super inneficient
# currently it's just checking available blocks rather than all the available 
# blocks of previous snakes
# for enemy snake moves we can call this but 
# add a bool that determins if numberes will be added or
# subtracted
def value_helper(data, snakes, walls, food, depth, block):
    global num_loops 
    num_loops += 1
    if (depth == 6 or block in snakes or block in walls):
        return 0
    else:
        right_block = {"x": block["x"] + 1, "y": block["y"]}
        left_block = {"x": block["x"] - 1, "y": block["y"]}
        down_block = {"x": block["x"], "y": block["y"] + 1}
        up_block = {"x": block["x"], "y": block["y"] - 1}
        
        right_val = 0
        left_val = 0
        down_val = 0
        up_val = 0
        
        
        # think of proper score calculations, i.e if you can kill a snake
        # then that is worth more than just surviving, food score 
        # should be considered too
        
        right_val = value_helper(data, snakes, walls, food, depth+1, right_block)
        left_val = value_helper(data, snakes, walls, food, depth+1, left_block)
        down_val = value_helper(data, snakes, walls, food, depth+1, down_block)
        up_val = value_helper(data, snakes, walls, food, depth+1, up_block)
            
        if (right_block in food):
            right_val += 3
        if (left_block in food):
            left_val += 3
        if (down_block in food):
            down_val += 3
        if (up_block in food):
            up_val += 3
            
        max_val = max(right_val, left_val, down_val, up_val)
            
        return max_val + 1
    
    

#dict -> list
# returns a list of dicts representing snake locations
def make_snakes(data):
    snakes = []
    for snake in data["board"]["snakes"]:
        for part in snake["body"]:
            if (part != data["you"]["body"][0]):
                snakes.append(part)
    return snakes
#dict -> list
# returns a list of dicts representing wall locations
def make_walls(data):
    walls = []
    for x in range (data["board"]["width"]+1):
        entry = {}
        entry["x"] = x
        entry["y"] = -1
        if (entry not in walls):
            walls.append(entry)
            
        entry = {}
        entry["x"] = x
        entry["y"] = data["board"]["height"]
        if (entry not in walls):
            walls.append(entry)
        
    for y in range (data["board"]["height"]):
        entry = {}
        entry["x"] = -1
        entry["y"] = y
        if (entry not in walls):
            walls.append(entry)
        
        entry = {}
        entry["x"] = data["board"]["width"]
        entry["y"] = y
        if (entry not in walls):
            walls.append(entry)
           
    return walls
# dict -> list
# returns a list of dicts representing food location
def make_food(data):
    food = []
    for item in data["board"]["food"]:
        food.append(item)
    return food
            
@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()