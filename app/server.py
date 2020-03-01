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
    
# (dict) -> string
# takes a dict representing the board data
# then returns a move response
#def dicision(dict)

# dict -> string
# takes a dict containg board info and produces a direction
def next_move(data):
    turn = data["turn"]            # turn is a int representign the turn in game
    you = data["you"]              # you is a dict representing your snakes data
    board = data["board"]          # board is a dict representing the game board info
    body = you["body"]             # body is a list of dicts representing your snakes location
    head = body[0]                 # head is a dict representing your snakes head
    max = board["height"]          # max is the dimention number e.g. 14 by 14
    max -= 1                       # we start counting at 0 because we are coders
    
    # directions = ["up", "down", "left", "right"]
    # bad_snake(directions, body)
    
    # uhhh... the snake will colide into itself depending on where it's body is
    # are a bunch or if else statements all we need? or can we implement recursion
    # mabey blocks of moves to fill a small 4 by 4 grid, but what about other snakes? 
    # initial size is 3
    # is a stack a good use here? 
    # if you have a head on head collision the smaller snake dies
    
    
    if (head["x"] == 0 and head["y"] == 0):            # top left corner 
        directions = ["down", "right"]
        return body_sensor(directions, body)
        
    elif (head["x"] == max and head["y"] == 0):        # top right corner 
        directions = ["down", "left"]
        return body_sensor(directions, body)
        
    elif (head["x"] == max and head["y"] == max):      # bottom right corner 
        directions = ["up", "left"]
        return body_sensor(directions, body)
        
    elif (head["x"] == 0 and head["y"] == max):        # bottom left corner
        directions = ["up", "right"]
        return body_sensor(directions, body)

    elif (head["x"] == 0):                             # left wall
        directions = ["up", "down","right"]
        return body_sensor(directions, body)
        
    elif (head["y"] == 0):                             # top wall 
        directions = ["down", "left","right"]
        return body_sensor(directions, body)

    elif (head["x"] == max):                           # right wall 
        directions = ["up", "down","left"]
        return body_sensor(directions, body)
        
    elif (head["y"] == max):                           # bottom wall
        directions = ["up", "left","right"]
        return body_sensor(directions, body)

    else:
        directions = ["up", "down", "left", "right"]   # middle of board
        return body_sensor(directions, body)
    


# we want our snake to choose the block that has the least amount of bodies around it 

# list, dict -> string
# should sense the possible options and pick the ones
# that won't result in instant death
def body_sensor(lod, body):
    head = body[0]
    headx = head["x"]
    heady = head["y"]
    right_block = {"x": headx+1, "y": heady}    
    left_block = {"x": headx-1, "y": heady}      
    down_block = {"x": headx, "y": heady+1}   
    up_block = {"x": headx, "y": heady-1}    

    if (right_block in body and "right" in lod):  
        lod.remove("right")
    if (left_block in body and "left" in lod):
        lod.remove("left")    
    if (up_block in body and "down" in lod):
        lod.remove("down")       
    if (down_block in body and "up" in lod):
        lod.remove("up")
        
    if (len(lod) != 0):                 
        if (len(lod) == 1):
            return lod[0]
            
        elif (len(lod) == 2):   # here is where we actually want to compare the options
            block1 = block_picker(lod[0], right_block, left_block, down_block, up_block)
            block2 = block_picker(lod[1], right_block, left_block, down_block, up_block)
            
            choice1 = advanced_body_sensor(block1, body)
            choice2 = advanced_body_sensor(block2, body)
            
            if (choice1 > choice2):
                return lod[0]
            elif (choice2 < choice1):
                return lod[1]
            else:                                      # when they are equal
                return random.choice(lod)
            
        elif (len(lod) == 3):
            block1 = block_picker(lod[0], right_block, left_block, down_block, up_block)
            block2 = block_picker(lod[1], right_block, left_block, down_block, up_block)
            block3 = block_picker(lod[2], right_block, left_block, down_block, up_block)
            
            choice1 = advanced_body_sensor(block1, body)
            choice2 = advanced_body_sensor(block2, body)
            choice3 = advanced_body_sensor(block3, body)
            
            if (choice1 > choice2 and choice1 > choice3):     # choice1 is biggest
                return lod[0]                
            elif (choice2 > choice1 and choice2 > choice3):   # choice2 is biggest
                return lod[1]                
            elif (choice3 > choice1 and choice3 > choice2):   # choice3 is biggest
                return lod[2]                
            elif (choice1 == choice2 and choice1 > choice3):  # choice1 & choice2 are equal, & greater than choice3 
                del lod[2]
                return random.choice(lod)                
            elif (choice1 == choice3 and choice1 > choice2):  # choice1 & choice3 are equal, & greater than choice2 
                del lod[1]
                return random.choice(lod)                
            elif (choice2 == choice3 and choice2 > choice1):  # choice2 & choice3 are equal, & greater than choice1
                del lod[0]
                return random.choice(lod)                
            else:                                             # they are all equal                    
                return random.choice(lod)
            
        else:
            return random.choice(lod)
    else: 
        print("we are surrounded....")
        return "up"
 
# dict, dict -> int
# takes the block and returns the # of options
# the snake has in this block
def advanced_body_sensor(block, body): 
    blockx = block["x"]
    blocky = block["y"]
    right_block = {"x": blockx+1, "y": blocky} 
    left_block = {"x": blockx-1, "y": blocky}
    down_block = {"x": blockx, "y": blocky+1}
    up_block = {"x": blockx, "y": blocky-1} 
    count = 0                                 # count of available moves                    
    
    if (right_block not in body):
        count += 1       
    if (left_block not in body):
        count += 1        
    if (down_block not in body):
        count += 1        
    if (up_block not in body): 
        count += 1
        
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