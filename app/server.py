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
    print("MOVE:", json.dumps(data))

    # Choose a random direction to move in
    directions = ["up", "down", "left", "right"]
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

def next_move(data):

    head = data["you"]["body"][0]
    directions = optimal_directions(data)
    directions = avoid_heads(data, head, directions)
    
    return target(data, head, directions)

# list, list, dict -> string
# takes a list of possible directions and 
# picks a direction that will goes towards food
def target(data, head, directions):
    

    heads = make_enemy_heads(data, head)
    sizes = make_sizes(data)
    own_size = len(data["you"]["body"])
    target = {}
    pathX = 100
    pathY = 100
    sizing = 0
    
    counter = 0
    for bad_head in heads: 
        if (own_size > sizes[counter]):
            difference = own_size - sizes[counter]
            x = abs(bad_head["x"] - head["x"])
            y = abs(bad_head["y"] - head["y"])
            if (difference > sizing):
                sizing = difference
                target = bad_head
    
    if (len(target) != 0):
        return pathing(data, head, target, directions, pathX, pathY) 
    return hungry(data, directions, data["board"]["food"], head)

# list, list, dict -> string
# takes a list of possible directions and 
# picks a direction that will goes towards food
def hungry(data, directions, food, head):
    path = 100   
    pathx = 100
    pathy = 100
    target = {}
    
    for item in food: 
        x = abs(item["x"] - head["x"])
        y = abs(item["y"] - head["y"])
        distance = x + y 
        if (distance < path):
            path = distance
            pathX = x
            pathY = y
            target = item
            
    return pathing(data, head, target, directions, pathX, pathY)

def chase_tail(data, head, directions):  
    pathx = 100
    pathy = 100
    target = data["you"]["body"][-1]
    
    pathX = abs(target["x"] - head["x"])
    pathY = abs(target["y"] - head["y"])
    
    if (len(directions) != 0):
        return pathing(data, head, target, directions, pathX, pathY)
    return "up"

def pathing(data, head, target, directions, pathX, pathY): 
    if (head["x"] <= target["x"] and head["y"] <= target["y"]):
        if ("right" in directions and "down" in directions):
            if (pathX > pathY):
                return "right"
            if (pathX < pathY):
                return "down" 
            return random.choice(["right", "down"])
            
        if ("down" in directions):  
            return "down"
            
        if ("right" in directions):
            return "right"
        
    if (head["x"] <= target["x"] and head["y"] >= target["y"]):
        if ("right" in directions and "up" in directions):
            if (pathX > pathY):
                return "right"
            if (pathX < pathY):
                return "up" 
            return random.choice(["right", "up"])
            
        if ("up" in directions):  
            return "up"
            
        if ("right" in directions):
            return "right"
            
    if (head["x"] >= target["x"] and head["y"] <= target["y"]):
        if ("left" in directions and "down" in directions):
            if (pathX > pathY):
                return "left"
            if (pathX < pathY):
                return "down" 
            return random.choice(["left", "down"])
            
        if ("down" in directions):  
            return "down"
            
        if ("left" in directions):
            return "left"
            
    if (head["x"] >= target["x"] and head["y"] >= target["y"]):
        if ("left" in directions and "up" in directions):
            if (pathX > pathY):
                return "left"
            if (pathX < pathY):
                return "up" 
            return random.choice(["left", "up"])
            
        if ("up" in directions):  
            return "up"
            
        if ("left" in directions):
            return "left"
    return chase_tail(data, head, directions)

# dict , int, int-> list
# takes a list representing a block on the map and 
# returns a list of available directions
def avoid_heads(data, head, directions):
    right_block = {"x": head["x"] + 1, "y": head["y"]}
    left_block = {"x": head["x"] - 1, "y": head["y"]}
    down_block = {"x": head["x"], "y": head["y"] + 1}
    up_block = {"x": head["x"], "y": head["y"] - 1}
    
    snakes = make_snakes(data)
    tails = make_tails(data)
    enemy_heads = make_enemy_heads(data, head)
    
    if (check_around(data, right_block, enemy_heads) != True and "right" in directions):
        directions.remove("right")
    if (check_around(data, left_block, enemy_heads) != True and "left" in directions):
        directions.remove("left")
    if (check_around(data, down_block, enemy_heads) != True and "down" in directions):
        directions.remove("down")
    if (check_around(data, up_block, enemy_heads) != True and "up" in directions):
        directions.remove("up")

    if (len(directions)==0):
        directions = optimal_directions_tails(data) # same thing but with heads?
        if (check_around(data, right_block, enemy_heads) != True and "right" in directions):
            directions.remove("right")
        if (check_around(data, left_block, enemy_heads) != True and "left" in directions):
            directions.remove("left")
        if (check_around(data, down_block, enemy_heads) != True and "down" in directions):
            directions.remove("down")
        if (check_around(data, up_block, enemy_heads) != True and "up" in directions):
            directions.remove("up")

    if (len(directions)==0):  
        if (right_block in tails):
            directions.append("right") 
        if (left_block in tails):
            directions.append("left")
        if (down_block in tails):
            directions.append("down")
        if (up_block in tails):
            directions.append("up")
            
    if (len(directions)==0):
        if (check_around_surrounded(data, right_block, enemy_heads) != True and right_block not in snakes):
            directions.append("right")
        if (check_around_surrounded(data, left_block, enemy_heads) != True and left_block not in snakes):
            directions.append("left")
        if (check_around_surrounded(data, down_block, enemy_heads) != True and down_block not in snakes):
            directions.append("down")
        if (check_around_surrounded(data, up_block, enemy_heads) != True and up_block not in snakes):
            directions.append("up")
        
    if (len(directions)==0):
        if (check_around(data, right_block, enemy_heads) != True and right_block not in snakes):
            directions.append("right")
        if (check_around(data, left_block, enemy_heads) != True and left_block not in snakes):
            directions.append("left")
        if (check_around(data, down_block, enemy_heads) != True and down_block not in snakes):
            directions.append("down")
        if (check_around(data, up_block, enemy_heads) != True and up_block not in snakes):
            directions.append("up")
    return directions

# dict, list -> bool
# takes a dicts and returns true if the block is safe
# returns false if the block is dangerous
def check_around(data, block, heads):
    right_block = {"x": block["x"]+1, "y": block["y"]}
    left_block = {"x": block["x"]-1, "y": block["y"]}
    down_block = {"x": block["x"], "y": block["y"]+1}
    up_block = {"x": block["x"], "y": block["y"]-1}
    
    own_size = len(data["you"]["body"])
    sizes = make_sizes(data)
    heads = make_enemy_heads(data, data["you"]["body"][0])
    
    # makes it so that if you are surrounded, go towards the snake
    # that is of equal size
    
    safe = True 
    counter = 0
    for head in heads:
        if (own_size <= sizes[counter]):
            if (right_block == head):
                safe = False
            if (left_block == head):
                safe = False
            if (down_block == head):
                safe = False
            if (up_block == head):
                safe = False
        counter += 1
    return safe
    
# dict, list -> bool
# takes a dicts and returns true if the block is safe
# returns false if the block is dangerous
def check_around_surrounded(data, block, heads):
    right_block = {"x": block["x"]+1, "y": block["y"]}
    left_block = {"x": block["x"]-1, "y": block["y"]}
    down_block = {"x": block["x"], "y": block["y"]+1}
    up_block = {"x": block["x"], "y": block["y"]-1}
    
    own_size = len(data["you"]["body"])
    sizes = make_sizes(data)
    heads = make_enemy_heads(data, data["you"]["body"][0])
    
    # makes it so that if you are surrounded, go towards the snake
    # that is of equal size
    
    safe = True 
    counter = 0
    for head in heads:
        if (own_size == sizes[counter]):
            if (right_block == head):
                safe = False
            if (left_block == head):
                safe = False
            if (down_block == head):
                safe = False
            if (up_block == head):
                safe = False
        counter += 1
    return safe
    
checked = []
def optimal_directions(data):
    head = data["you"]["body"][0]
    snakes = make_snakes(data)
    
    right_block = {"x": head["x"] + 1, "y": head["y"]}
    left_block = {"x": head["x"] - 1, "y": head["y"]}
    down_block = {"x": head["x"], "y": head["y"] + 1}
    up_block = {"x": head["x"], "y": head["y"] - 1}
    
    checked.clear()
    right = links(data, head, snakes, "right")
    checked.clear()
    left = links(data, head, snakes, "left")
    checked.clear()
    down = links(data, head, snakes, "down")
    checked.clear()
    up = links(data, head, snakes, "up")
    
    values = [right, left, down, up]
    values.sort(reverse=True)
    directions = []
    
    for num in range(4):
        if (values[num] == right and "right" not in directions):
            directions.append("right")
        if (values[num] == left and "left" not in directions):
            directions.append("left")
        if (values[num] == down and "down" not in directions):
            directions.append("down")
        if (values[num] == up and "up" not in directions):
            directions.append("up")
    
    
    if (values[0] > values[1]):
        return [directions[0]]
    if (values[0] > values[2]):
        return [directions[0], directions[1]]
    if (values[0] > values[3]):
        return [directions[0], directions[1], directions[2]]
    return directions  
   
def links(data, block, snakes, direction):
    counter = 0
    if (direction == "right"):
        counter += links_v2(data, block, snakes, "right", 0)
        
    if (direction == "left"):
        counter += links_v2(data, block, snakes, "left", 0)
    
    if (direction == "down"):
        counter += links_v2(data, block, snakes, "down", 0)
    
    if (direction == "up"):
        counter += links_v2(data, block, snakes, "up", 0)
    return counter     

def links_v2(data, block, snakes, direction, count):
    right_block = {"x": block["x"] + 1, "y": block["y"]}
    left_block = {"x": block["x"] - 1, "y": block["y"]}
    down_block = {"x": block["x"], "y": block["y"] + 1}
    up_block = {"x": block["x"], "y": block["y"] - 1}
    
    
    if (direction == "right"):
        if (right_block in snakes or right_block["x"] == data["board"]["width"] or right_block in checked):
            return count
        checked.append(right_block)
        return links_v2(data, right_block, snakes, direction, count + 1) + links(data, right_block, snakes, "down") + links(data, right_block, snakes, "up")
        
    if (direction == "left"):
        if (left_block in snakes or left_block["x"] == -1 or left_block in checked):
            return count
        checked.append(left_block)
        return links_v2(data, left_block, snakes, direction, count + 1) + links(data, left_block, snakes, "down") + links(data, left_block, snakes, "up")
        
    if (direction == "down"):
        if (down_block in snakes or down_block["y"] == data["board"]["height"] or down_block in checked):
            return count
        checked.append(down_block)
        return links_v2(data, down_block, snakes, direction, count + 1)  + links(data, down_block, snakes, "right") + links(data, down_block, snakes, "left")
        
    if (direction == "up"):
        if (up_block in snakes or up_block["y"] == -1 or up_block in checked):
            return count
        checked.append(up_block)
        return links_v2(data, up_block, snakes, direction, count + 1) + links(data, up_block, snakes, "right") + links(data, up_block, snakes, "left")

def optimal_directions_tails(data):
    head = data["you"]["body"][0]
    snakes = make_snakes(data)
    
    right_block = {"x": head["x"] + 1, "y": head["y"]}
    left_block = {"x": head["x"] - 1, "y": head["y"]}
    down_block = {"x": head["x"], "y": head["y"] + 1}
    up_block = {"x": head["x"], "y": head["y"] - 1}
    
    checked.clear()
    right = links_tails(data, head, snakes, "right")
    checked.clear()
    left = links_tails(data, head, snakes, "left")
    checked.clear()
    down = links_tails(data, head, snakes, "down")
    checked.clear()
    up = links_tails(data, head, snakes, "up")
    
    values = [right, left, down, up]
    values.sort(reverse=True)
    directions = []
    
    for num in range(4):
        if (values[num] == right and "right" not in directions):
            directions.append("right")
        if (values[num] == left and "left" not in directions):
            directions.append("left")
        if (values[num] == down and "down" not in directions):
            directions.append("down")
        if (values[num] == up and "up" not in directions):
            directions.append("up")
    
    
    if (values[0] > values[1]):
        return [directions[0]]
    if (values[0] > values[2]):
        return [directions[0], directions[1]]
    if (values[0] > values[3]):
        return [directions[0], directions[1], directions[2]]
    return directions

def links_tails(data, block, snakes, direction):
    counter = 0
    if (direction == "right"):
        counter += links_v2_tails(data, block, snakes, "right", 0)
        
    if (direction == "left"):
        counter += links_v2_tails(data, block, snakes, "left", 0)
    
    if (direction == "down"):
        counter += links_v2_tails(data, block, snakes, "down", 0)
    
    if (direction == "up"):
        counter += links_v2_tails(data, block, snakes, "up", 0)
    return counter 

def links_v2_tails(data, block, snakes, direction, count):
    right_block = {"x": block["x"] + 1, "y": block["y"]}
    left_block = {"x": block["x"] - 1, "y": block["y"]}
    down_block = {"x": block["x"], "y": block["y"] + 1}
    up_block = {"x": block["x"], "y": block["y"] - 1}
    
    tails = make_tails(data)
    
    
    if (direction == "right"):
        if ((right_block in snakes or right_block["x"] == data["board"]["width"] or right_block in checked) and right_block not in tails):
            return count
        checked.append(right_block)
        return links_v2_tails(data, right_block, snakes, direction, count + 1) + links_tails(data, right_block, snakes, "down") + links_tails(data, right_block, snakes, "up")
        
    if (direction == "left"):
        if ((left_block in snakes or left_block["x"] == -1 or left_block in checked) and left_block not in tails):
            return count
        checked.append(left_block)
        return links_v2_tails(data, left_block, snakes, direction, count + 1) + links_tails(data, left_block, snakes, "down") + links_tails(data, left_block, snakes, "up")
        
    if (direction == "down"):
        if ((down_block in snakes or down_block["y"] == data["board"]["height"] or down_block in checked) and down_block not in tails):
            return count
        checked.append(down_block)
        return links_v2_tails(data, down_block, snakes, direction, count + 1)  + links_tails(data, down_block, snakes, "right") + links_tails(data, down_block, snakes, "left")
        
    if (direction == "up"):
        if ((up_block in snakes or up_block["y"] == -1 or up_block in checked) and up_block not in tails):
            return count
        checked.append(up_block)
        return links_v2_tails(data, up_block, snakes, direction, count + 1) + links_tails(data, up_block, snakes, "right") + links_tails(data, up_block, snakes, "left")
    
def make_snakes(data):
    snakes = []
    for snake in data["board"]["snakes"]:
        for part in snake["body"]:
            snakes.append(part)
    return snakes
    
# list, list -> list
# makes a list of enemy snake heads 
def make_heads(data):
    heads = []
    for snake in data["board"]["snakes"]:
        heads.append(snake["body"][0])
    return heads
    
# list, list -> list
# makes a list of enemy snake heads 
def make_enemy_heads(data, head):
    heads = []
    for snake in data["board"]["snakes"]:
        if (snake["body"][0] != head):
            heads.append(snake["body"][0])
    return heads

# list -> list
# makes a list of tails
def make_tails(data):
    tails = []
    for snake in data["board"]["snakes"]: 
        tails.append(snake["body"][-1])
    return tails
    
# list -> list
# makes a list of all the snakes sizes
def make_sizes(data): 
    sizes = []
    for snake in data["board"]["snakes"]: 
        body = snake["body"]
        size = len(body)
        sizes.append(size)
    return sizes
    
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