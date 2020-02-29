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
    
    
# list, dict -> string 
# takes a list of possible directions and a dict 
# representing your snakes body locations and produce a move
# that won't make the snake eat itself
def bad_direction(lod, body): 
    # first focus on a 3 body snake
    # might have to individual cases depending on the contents of the 
    # lod, but is it posible to remove the bad directions from the dict? 
    # yes loop through the list, and if it comtains bad directions then don't 
    # append it to you good directions list
    # first deal with the case where the snakes body(block after the head)
    # then if it is a perfect line
    # replicate if it is more than 3
    # you start with only 1 head
    
    head = body[0]
    try:
        after_head = body[1]
    except IndexError:  
        return random.choice(lod)    
        
    # if body is to the right of head and on the same line
    if (head["x"] + 1 == after_head["x"] and head["y"] == after_head["y"]):
        return good_direction(lod, "right")
        
    # if body is to the left of the head and on the same line
    elif (head["x"] - 1 == after_head["x"] and head["y"] == after_head["y"]):
        return good_direction(lod, "left")
        
    # if body is below the head and on the same line
    elif (head["y"] + 1 == after_head["y"] and head["x"] == after_head["x"]):
        return good_direction(lod, "down")
        
    # if body is above the head and on the same line
    elif (head["y"] - 1 == after_head["y"] and head["x"] == after_head["x"]): 
        return good_direction(lod, "up")
        
    else:
        return random.choice(lod)



# should sense the possible options and pick the ones
# that won't result in instant death
def body_sensor(lod, body):
    head = body[0]
    headx = head["x"]
    heady = head["y"]
    option1 = {"x": headx+1, "y": heady}    # right block
    option2 = {"x": headx-1, "y": heady}    # left block   
    option3 = {"x": headx, "y": heady+1}    # down block
    option4 = {"x": headx, "y": heady-1}    # up block 

    if (option1 in body and "right" in lod): 
        lod.remove("right")
        
    if (option2 in body and "left" in lod):
        lod.remove("left")
        
    if (option3 in body and "down" in lod):
        lod.remove("down")
        
    if (option4 in body and "up" in lod):
        lod.remove("up")
        
    if (len(lod) != 0):
        return random.choice(lod)
    else: 
        print("we are surrounded....")
        return "up"
    
    
    
    


# list, string -> string 
# takes a list of directions and a bad direction
# then returns a list of only good directions
def good_direction(lod, bad): 
    lod.remove(bad)
    good_list = lod
    return good_list 


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