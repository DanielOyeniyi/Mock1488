# turn is a int
# you is a dict
# board is a dict
# body is a list of dicts
# head is a dict representing x,y coordinates
def next_move(dict):
    turn = dict["turn"]
    you = dict["you"]
    board = dict["board"]
    body = you["body"]
    head = body[0] 
    
    if (head["x"] == 0 or head["x"] == 10):
        return "right"
    elif (head["y"] == 0 or head["y"] == 10):
        return "right"
    else: 
        return "right"
    