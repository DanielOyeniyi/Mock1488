import random

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
    # or if your body size is bigger than 3
    
    
    if (head["x"] == 0 and head["y"] == 0):            # top left corner 
        directions = ["down", "right"]
        move = random.choice(directions)
        return move
        
    elif (head["x"] == range and head["y"] == 0):      # top right corner 
        directions = ["down", "left"]
        move = random.choice(directions)
        
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
    
    
    
    
    
# (list), dict -> str
# takes a list of directions and a dictionary containing
# your snakes body locations assumes size two
# def bad_snake(lod, body):
    # size = body.length()
    # print(size)

