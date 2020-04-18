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
    #next_move(data)
    print("MOVE:", json.dumps(data))


    move = "left" #Notmove > halfWidth to centerB x and Notmove > halfWidth to centerB y

    #move = next_move(data)

    #FIRST PRIORITY - Snake should avoid hitting walls 
    heightBoard = data["board"]["height"] #retrieve height 
    widthBoard = data["board"]["width"]  #retrieve width 

    halfHeight = heightBoard / 2
    halfWidth = widthBoard / 2

    centerBlock = {		#location of center of board
      "centerB":
        {
          "x": halfWidth,
          "y": halfHeight
        }  
    }

              # LOCATION: of snake head
    locHeadX = data["you"]["body"][0]["x"]
    locHeadY = data["you"]["body"][0]["y"]
        
    #If statement to force snake away from boundaries/wall
    #x boundary/walls/corners
    if (locHeadX == (widthBoard-1)):  #farthest x-axis length, a length of 11 is represented by index 10  
                # LOCATION: of neck1 
        neck1X = data["you"]["body"][1]["x"]
        if(neck1X ==(widthBoard-2)):   #if body is in the left column next to the farthest length value
            move = "up"
        else:
            move = "left"

    if (locHeadX == 0):  #closest x-axis length
         
        neck1X = data["you"]["body"][1]["x"]
        if(neck1X ==(1)):
          move = "up"
        else:
          move = "right"


    #y boundary/walls/corners
    if (locHeadY == heightBoard):
        neck1Y = data["you"]["body"][1]["y"]
        if (neck1Y == heightBoard-2):
                move = "right"
        else:
            move = "up"
      
    if (locHeadY == 0):
        neck1Y = data["you"]["body"][1]["y"]
        if (neck1Y == 1):
          move = "right"
        else:
            move = "down"
        

    #END OF FIRST PRIORITY #############################################

        
    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


     
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