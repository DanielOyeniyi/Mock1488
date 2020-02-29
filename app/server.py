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
    print("MOVE:", json.dumps()) # just raw text... move is irrelavent
    
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
    range = board["height"]        # range is the dimention number e.g. 14 by 14
    range -= 1                     # we start counting at 0 because we are coders
    
    # directions = ["up", "down", "left", "right"]
    # bad_snake(directions, body)
    
    # uhhh... the snake will colide into itself depending on where it's body is
    # are a bunch or if else statements all we need? or can we implement recursion
    # mabey blocks of moves to fill a small 4 by 4 grid, but what about other snakes? 
    # initial size is 3
    # is a stack a good use here? 
    
    
    if (head["x"] == 0 and head["y"] == 0):            # top left corner 
        directions = ["down", "right"]
        move = random.choice(directions)
        return move
        
    elif (head["x"] == range and head["y"] == 0):      # top right corner 
        directions = ["down", "left"]
        move = random.choice(directions)
        return move
        
    elif (head["x"] == range and head["y"] == range):  # bottom right corner 
        directions = ["up", "left"]
        move = random.choice(directions)
        return move
        
    elif (head["x"] == 0 and head["y"] == range):      # bottom left corner
        directions = ["up", "right"]
        move = random.choice(directions)
        return move

    elif (head["x"] == 0):                             # left wall
        directions = ["up", "down","right"]
        move = random.choice(directions)
        return move
        
    elif (head["y"] == 0):                             # top wall 
        directions = ["down", "left","right"]
        move = random.choice(directions)
        return move

    elif (head["x"] == range):                         # right wall 
        directions = ["up", "down","left"]
        move = random.choice(directions)
        return move
        
    elif (head["y"] == range):                         # bottom wall
        directions = ["up", "left","right"]
        move = random.choice(directions)
        return move

    else:
        directions = ["up", "down", "left", "right"]   # middle of board
        return bad_direction(directions, body)
    
    
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
        
    # please just use the head as it is easier to understand    
        
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

# list, string -> string 
# takes a list of directions and a bad direction
# then returns a list of only good directions
def good_direction(lod, bad): 
    good_list = []
    for direction in lod: 
        if (direction != bad):
            good_list.append(direction)
    return random.choice(good_list)


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