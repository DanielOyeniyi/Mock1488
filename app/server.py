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
    #print("START:", json.dumps(data))

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
    print("MOVE:", json.dumps(data["turn"])) # just raw text... move is irrelavent
    
    # try and remember past moves (with size being snake length)
    directions = ["up", "down", "left", "right"]
    move = random.choice(directions)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    response = {"move": "right", "shout": shout}
    print()
    response = next_move(data)
    print(response)
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

# (dict) -> str
# takes a dict containg board info and produces a direction
# turn is a int
# you is a dict
# board is a dict
# body is a list of dicts
# head is a dict representing x,y coordinates
def next_move(data):
    turn = data["turn"]
    you = data["you"]
    board = data["board"]
    body = you["body"]
    head = body[0] 
    range = board["height"]
    range -= 1 # we start counting at 0
    
    # directions = ["up", "down", "left", "right"]
    # bad_snake(directions, body)
    
    # uhhh... the snake will colide into itself depending on where it's body is
    # are a bunch or if else statements all we need? or can we implement recursion
    # mabey blocks of moves to fill a small 4 by 4 grid, but what about other snakes? 
    # or if your body size is bigger than 3, initial size is 3
    
    
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
        move = random.choice(directions)
        return move
    
    








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