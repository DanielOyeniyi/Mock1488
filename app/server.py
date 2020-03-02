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
    ownsize = len(body)                      # size of your own snake
    health = you["health"]                   # health of the snake
    head = body[0]                           # head is a dict representing your snakes head
    max = board["height"]                    # max is the dimention number e.g. 14 by 14
    max -= 1
    
    # you could use less parameters if you just sent the board
    # yeah, it would be way easier to read, it makes more sense
    
    if (head["x"] == 0 and head["y"] == 0):            # top left corner 
        directions = ["down", "right"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)
        
        
    elif (head["x"] == max and head["y"] == 0):        # top right corner 
        directions = ["down", "left"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)
        
        
    elif (head["x"] == max and head["y"] == max):      # bottom right corner 
        directions = ["up", "left"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)
        
        
    elif (head["x"] == 0 and head["y"] == max):        # bottom left corner
        directions = ["up", "right"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)


    elif (head["x"] == 0):                             # left wall
        directions = ["up", "down","right"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)
        
        
    elif (head["y"] == 0):                             # top wall 
        directions = ["down", "left","right"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)
        

    elif (head["x"] == max):                           # right wall 
        directions = ["up", "down","left"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)
        
        
    elif (head["y"] == max):                           # bottom wall
        directions = ["up", "left","right"]
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)


    else:
        directions = ["up", "down", "left", "right"]   # middle of board
        safe_directions = body_sensor(directions, head, snakes, max, food, ownsize)
        return chase_or_feast(safe_directions, snakes, head, ownsize, food, body)
    
# list, list, dict, int, list, int  
def chase_or_feast(lod, snakes, head, ownsize, food, body):
    headx = head["x"]
    heady = head["y"]
    sizes = make_sizes(snakes)
    nearest = 100
    
    target = []
    for snake in snakes:
        snake_body = snake["body"]
        snake_head = snake_body[0]
        x = abs(snake_head["x"] - headx)
        y = abs(snake_head["y"] - heady)
        distance = x + y
        if (distance < nearest):
            if (snake_body != body):
                nearest = distance 
                target = snake_head
            
            
    if (len(target) != 0):
        if (headx > target["x"]):
            if ("left" in lod):
                return "left"
        if (headx < target["x"]):
            if ("right" in lod):
                return "right"
        if (heady > target["y"]):
            if ("up" in lod):
                return "up"
        if (heady < target["y"]):
            if ("down" in lod):
                return "down"

    if (len(lod) != 0):
        return eat_food(lod, food, head)
    else: 
        print("Uh oh...")
        return "up"
    

# list, list -> string
# takes a list of possible directions and 
# picks a direction that will go towards food
def eat_food(lod, food, head):
    headx = head["x"]
    heady = head["y"]
    
 
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
    
# list -> list
# makes a list of all the tails on the board
def make_tails(snakes): 
    tails = []
    for snake in snakes: 
        body = snake["body"]
        tails.append(body[-1])
    return tails
  
# list -> list
# makes a list of all the heads on the board
def make_heads(snakes): 
    heads = []
    for snake in snakes: 
        body = snake["body"]
        heads.append(body[0])
    return heads

# list -> list
# makes a list of all the snakes sizes
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
def body_sensor(lod, head, snakes, max, food, ownsize):
    headx = head["x"]
    heady = head["y"]
    tails = make_tails(snakes)
    heads = make_heads(snakes)
    heads.remove(head)
    sizes = make_sizes(snakes)
    snakes = make_occupied(snakes)
    
    
    right_block = {"x": headx+1, "y": heady}    
    left_block = {"x": headx-1, "y": heady}      
    down_block = {"x": headx, "y": heady+1}   
    up_block = {"x": headx, "y": heady-1}    
    
    
    # removing isntanst death options
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
            
        elif (len(lod) == 2):   
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
            else:                                      
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
 
# dict, list, list, list, int, int, list -> int
# takes the block and returns the # of options
# the snake has in this block
def advanced_body_sensor(block, snakes, tails, heads, sizes, ownsize, max, food):  # can we make it check even more possibilities?
    blockx = block["x"]
    blocky = block["y"]
    
    # reachable directions
    right_block = {"x": blockx+1, "y": blocky} 
    left_block = {"x": blockx-1, "y": blocky}
    down_block = {"x": blockx, "y": blocky+1}
    up_block = {"x": blockx, "y": blocky-1}             

    # unreachable(diagonal) directions
    top_right_block = {"x": blockx+1, "y": blocky-1}
    top_left_block = {"x": blockx-1, "y": blocky-1}
    bottom_right_block = {"x": blockx+1, "y": blocky+1}
    bottom_left_block = {"x": blockx-1, "y": blocky+1}
    
    blocks = [right_block, left_block, down_block, up_block, top_right_block, 
             top_left_block, bottom_right_block, bottom_left_block]
    
    count = 0           # a weighted measurement of the block priority
      
    # now case like, don't be agressive if you are close to walls or something
    # e.g. don't chase if your body and another head are in the way
    # go along your body rather than pathing in tight spots to give self room 
    # smaller board makes you focus on proper pathing
    # can I use the same method I used to target food to tartget heads?
    # better counting is key
    
    if (block in food):
        count += 2
        
    for block1 in blocks: 
        count += zone_check(block1, snakes, max)
    
    
    for tail in tails:
        for block1 in blocks: 
            count += zone_check_tails(block1, tail)

    counter = 0
    for head in heads:                  # look to kill if bigger, run away if smaller
        for block1 in blocks:
            count += zone_check_heads(block1, head, ownsize, sizes, counter)
        counter += 1
    
    if (block["x"] == -1 or block["x"] == max+1):
        count -= 1
    if (block["y"] == -1 or block["y"] == max+1):
        count -= 1
    
    print(count)
    return count

# dict, list -> int
# takes a block and checks if any snake is 
# in this block or not
def zone_check(block, snakes, max):
    if (block in snakes): 
        return -1
    if (block not in snakes):
        if (block["x"] != max+1 and block["x"] != -1):
            if (block["y"] != max+1 and block["y"] != -1):
                return 1 
    return 0
    
# dict, dict -> int
# takes a block and checks if tail is in it or not
def zone_check_tails(block, tail):
    if (block == tail):
        return 1
    return 0
    
# dict, dict, int, list, int ->  int
# takes a block and checks if head is in it or not
def zone_check_heads(block, head, ownsize, sizes, counter):
    if (ownsize > sizes[counter]):
        if (block == head):
            return 5
    if (block == head):
        return -5
    return 0
    
# dict, dict -> int
# takes a block and checks if food is in it or not
def zone_check_food(block, item):
    if (block == item):
        return 2
    return 0
    
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