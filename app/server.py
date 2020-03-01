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



# only works for one game at a time
@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#00FF7F", "headType": "bendr", "tailType": "round-bum"}
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
    print("MOVE:", json.dumps(data)) # just raw text... move is irrelavent
    
    # try and remember past moves (with size being snake length)
    shout = "I am a python snake!"
    
    move = next_move(data)
    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )
    # create seperate files classes
    # (0,0) is top left
    

# dict -> string
# takes a dict containg board info and produces a direction
def next_move(data):
    turn = data["turn"]                      # turn is a int representign the turn in game
    you = data["you"]                        # you is a dict representing your snakes data
    board = data["board"]                    # board is a dict representing the game board info
    snakes = board["snakes"]                 # locations of occupied spots on the board
    food = board["food"]                     # locations of food on the board
    body = you["body"]                       # body is a list of dicts representing your snakes location
    health = you["health"]                   # health of the snake
    head = body[0]                           # head is a dict representing your snakes head
    max = board["height"]                    # max is the dimention number e.g. 14 by 14
 
    
    if (head["x"] == 0 and head["y"] == 0):            # top left corner 
        directions = ["down", "right"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)
        
    elif (head["x"] == max and head["y"] == 0):        # top right corner 
        directions = ["down", "left"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)
        
    elif (head["x"] == max and head["y"] == max):      # bottom right corner 
        directions = ["up", "left"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)
        
    elif (head["x"] == 0 and head["y"] == max):        # bottom left corner
        directions = ["up", "right"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)

    elif (head["x"] == 0):                             # left wall
        directions = ["up", "down","right"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)
        
    elif (head["y"] == 0):                             # top wall 
        directions = ["down", "left","right"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)

    elif (head["x"] == max):                           # right wall 
        directions = ["up", "down","left"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)
        
    elif (head["y"] == max):                           # bottom wall
        directions = ["up", "left","right"]
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)

    else:
        directions = ["up", "down", "left", "right"]   # middle of board
        return eat_food(body_sensor(directions, body, snakes, max, food), food, body)
    

# list, list -> string
# takes a list of possible directions and 
# picks a direction that will go towards food
def eat_food(lod, food, body):
    head = body[0]
    headx = head["x"]
    heady = head["y"]
    
    # need to find a more efficient path to closest food
    # pick the closest food
    
    nearest = 100
    
    food1 = []
    
    for item in food: 
        x = abs(item["x"] - headx)
        y = abs(item["y"] - heady)
        distance = x + y 
        if (distance < nearest):
            nearest = distance
            food1 = item

    if (headx > food1["x"]):
        if ("left" in lod):
            return "left"
    if (headx < food1["x"]):
        if ("right" in lod):
            return "right"
    if (heady > food1["y"]):
        if ("up" in lod):
            return "up"
    if (heady < food1["y"]):
        if ("down" in lod):
            return "down"

    if (len(lod) != 0):
        return random.choice(lod)
    else: 
        print("Uh oh...")
        return "up"


# list -> list
# makes a list of all the occupied spots on the map
def make_occupied(snakes):
    occupied = []
    for snake in snakes:
        body = snake["body"]
        for block in body: 
            occupied.append(block)
    return occupied
    
def make_tails(snakes): 
    tails = []
    for snake in snakes: 
        body = snake["body"]
        tails.append(body[-1])
    return tails
    
def make_heads(snakes): 
    heads = []
    for snake in snakes: 
        body = snake["body"]
        heads.append(body[0])
    return heads

def make_sizes(snakes): 
    sizes = []
    for snake in snakes: 
        body = snake["body"]
        size = len(body)
        sizes.append(size)
    return sizes


# list, list, int -> string
# should sense the possible options and pick the ones
# that won't result in instant death
def body_sensor(lod, body, snakes, max, food):
    head = body[0]
    headx = head["x"]
    heady = head["y"]
    ownsize = len(body)
    tails = make_tails(snakes)
    heads = make_heads(snakes)
    heads.remove(head)
    sizes = make_sizes(snakes)
    snakes = make_occupied(snakes)
    right_block = {"x": headx+1, "y": heady}    
    left_block = {"x": headx-1, "y": heady}      
    down_block = {"x": headx, "y": heady+1}   
    up_block = {"x": headx, "y": heady-1}    
    
    

    if (right_block in snakes and "right" in lod):  
        lod.remove("right")
    if (left_block in snakes and "left" in lod):
        lod.remove("left")    
    if (down_block in snakes and "down" in lod):
        lod.remove("down")       
    if (up_block in snakes and "up" in lod):
        lod.remove("up")
        
    if (len(lod) != 0):                 
        if (len(lod) == 1):
            return lod
            
        elif (len(lod) == 2):   # here is where we actually want to compare the options
            block1 = block_picker(lod[0], right_block, left_block, down_block, up_block)
            block2 = block_picker(lod[1], right_block, left_block, down_block, up_block)
            
            choice1 = advanced_body_sensor(block1, snakes, tails, heads, sizes, ownsize, max, food)
            choice2 = advanced_body_sensor(block2, snakes, tails, heads, sizes, ownsize, max, food)
            
            if (choice1 > choice2):
                del lod[1]
                return lod
            elif (choice2 > choice1):
                del lod[0]
                return lod
            else:                                      # when they are equal
                return lod
            
        elif (len(lod) == 3):
            block1 = block_picker(lod[0], right_block, left_block, down_block, up_block)
            block2 = block_picker(lod[1], right_block, left_block, down_block, up_block)
            block3 = block_picker(lod[2], right_block, left_block, down_block, up_block)
            
            choice1 = advanced_body_sensor(block1, snakes, tails, heads, sizes, ownsize, max, food)
            choice2 = advanced_body_sensor(block2, snakes, tails, heads, sizes, ownsize, max, food)
            choice3 = advanced_body_sensor(block3, snakes, tails, heads, sizes, ownsize, max, food)
            
            if (choice1 > choice2 and choice1 > choice3):     # choice1 is biggest
                del lod[2]
                del lod[1]
                return lod    
                
            elif (choice2 > choice1 and choice2 > choice3):   # choice2 is biggest
                del lod[2]
                del lod[0]
                return lod    
                
            elif (choice3 > choice1 and choice3 > choice2):   # choice3 is biggest
                del lod[1]
                del lod[0]
                return lod   
                
            elif (choice1 == choice2 and choice1 > choice3):  # choice1 & choice2 are equal, & greater than choice3 
                del lod[2]
                return lod
                
            elif (choice1 == choice3 and choice1 > choice2):  # choice1 & choice3 are equal, & greater than choice2 
                del lod[1]
                return lod 
                
            elif (choice2 == choice3 and choice2 > choice1):  # choice2 & choice3 are equal, & greater than choice1
                del lod[0]
                return lod        
                
            else:                                             # they are all equal                    
                return lod
            
        else:
            return lod
    else: 
        return []
 
# dict, dict, int -> int
# takes the block and returns the # of options
# the snake has in this block
def advanced_body_sensor(block, snakes, tails, heads, sizes, ownsize, max, food):  # can we make it check even more possibilities?
    blockx = block["x"]
    blocky = block["y"]
    right_block = {"x": blockx+1, "y": blocky} 
    left_block = {"x": blockx-1, "y": blocky}
    down_block = {"x": blockx, "y": blocky+1}
    up_block = {"x": blockx, "y": blocky-1} 
    count = 0                                 # count of available blocks                  

    # keep track of sizes, if size is smaller than you attack the head
    # find quickest path to oponents head if smaller

    if (right_block not in snakes):
        count += 1       
    if (left_block not in snakes):
        count += 1        
    if (down_block not in snakes):
        count += 1        
    if (up_block not in snakes): 
        count += 1

    for tail in tails:
        if (right_block == tail):
            count += 1
        if (left_block == tail):
            count += 1
        if (down_block == tail):
            count += 1
        if (up_block == tail):
            count += 1

    counter = 0
    for head in heads:                  # look to kill if bigger, run away if smaller
        if (ownsize > sizes[counter]):           
            if (right_block == head):
                count += 6
            if (left_block == head):
                count += 6
            if (down_block == head):
                count += 6
            if (up_block == head):
                count += 6
                
        else:
            if (right_block == head):
                count -= 2
            if (left_block == head):
                count -= 2
            if (down_block == head):
                count -= 2
            if (up_block == head):
                count -= 2
        counter += 1

    for item in food: 
        if (right_block == item):
            count += 3
        if (left_block == item):
            count += 3
        if (down_block == item):
            count += 3
        if (up_block == item):
            count += 3

    if (blockx == -1 or blockx == max):
        count -= 1
    if (blocky == -1 or blocky == max):
        count -= 1
       
    print(food)
    print(down_block)
    print(count)
    return count
    
    
    
# string, dict, dict, dict, dict -> dict
# takes direction and returns the corresponding block location
def block_picker(direction, right_block, left_block, down_block, up_block):    
    if (direction == "right"):
        return right_block
    elif (direction == "left"):
        return left_block
    elif (direction == "down"):
        return down_block
    else: 
        return up_block

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