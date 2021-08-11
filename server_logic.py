import random
from typing import List, Dict

import numpy as np

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""

## Finding and getting a next body locations
def get_next_body(origin_bodies, next_move):
  copy_bodies = []
  head = origin_bodies[0]

  if next_move == "up":
    for i in range(len(origin_bodies)): 
      if i == 0:
        copy_bodies.append({"x" : head["x"], "y": head["y"] + 1})
      else:
        copy_bodies.append(origin_bodies[i-1])

  if next_move == "down":
    for i in range(len(origin_bodies)): 
      if i == 0:
        copy_bodies.append({"x" : head["x"], "y": head["y"] - 1})
      else:
        copy_bodies.append(origin_bodies[i-1])


  if next_move == "left":
    for i in range(len(origin_bodies)): 
      if i == 0:
        copy_bodies.append({"x" : head["x"] - 1, "y": head["y"]})
      else:
        copy_bodies.append(origin_bodies[i-1])

  if next_move == "right":
    for i in range(len(origin_bodies)): 
      if i == 0:
        copy_bodies.append({"x" : head["x"] + 1, "y": head["y"]})
      else:
        copy_bodies.append(origin_bodies[i-1])
  return copy_bodies
## end of the function  

## Avoiding dead end
def avoid_dead_end(body_data, moves):
  head = body_data[0]
  x_exit = 0
  y_exit = 0

  for data in body_data:
    x_exit += data["x"] - head["x"]
    y_exit += data["y"] - head["y"]

    for move in moves[3:]:
      if((move == "up" and head["y"] + 1 == data["y"]) or (move == "down" and head["y"] -1 == data["y"])):
        if(x_exit > 0) :
          return "left"
        if(x_exit < 0) : 
          return "right"
      if((move == "right" and head["x"] + 1 == data["x"]) or (move == "left" and head["x"] -1 == data["x"])):
        if(x_exit > 0) :
          return "down"
        if(x_exit < 0) : 
          return "up"

  return "nothing"

def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them

    board_height = data["board"]["height"]
    board_width = data["board"]["width"]

    try:
      if data["you"]["head"]["x"] == 0:
        possible_moves.remove("left")
    except:
      print()

    try:
      if data["you"]["head"]["x"] == board_width - 1:
        possible_moves.remove("right")
    except:
      print()

    try:
      if data["you"]["head"]["y"] == 0:
        possible_moves.remove("down")
    except:
      print()

    try:
      if data["you"]["head"]["y"] == board_height - 1:
        possible_moves.remove("up")
    except:
      print()

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body
    right_count = 0
    left_count = 0

    up_count = 0
    down_count = 0

    for body in data["you"]["body"]:
      if(body["x"] > data["you"]["head"]["x"]):
        right_count += 1
      elif(body["x"] < data["you"]["head"]["x"]) :
        left_count += 1

    for body in data["you"]["body"]:
      if(body["y"] > data["you"]["head"]["y"]):
        up_count += 1
      elif(body["y"] < data["you"]["head"]["y"]) :
        down_count += 1
    
    moving_loop = possible_moves.copy()

    for move in moving_loop:

      if move == "up":
        next_body = get_next_body(data["you"]["body"], "up")
        next_head = next_body[0]

        # head does not collide with own head, first, second body
        next_body_from_3 = np.array(next_body)[3:]

        if next_head in next_body_from_3:
          try:
            possible_moves.remove("up")
          except:
            print()
          try:
            if(right_count > left_count):
              possible_moves.remove("right")
            elif(right_count < left_count):
              possible_moves.remove("left")
          except:
            print()

      if move == "down":
        next_body = get_next_body(data["you"]["body"], "down")
        next_head = next_body[0]

        # head does not collide with own head, first, second body
        next_body_from_3 = np.array(next_body)[3:]

        if next_head in next_body_from_3:
          try:
            possible_moves.remove("down")
          except:
            print()
          try:
            if(right_count > left_count):
              possible_moves.remove("right")
            elif(right_count < left_count):
              possible_moves.remove("left")
          except:
            print()

      if move == "left":
        next_body = get_next_body(data["you"]["body"], "left")
        next_head = next_body[0]

        # head does not collide with own head, first, second body
        next_body_from_3 = np.array(next_body)[3:]

        if next_head in next_body_from_3:
          try:
            possible_moves.remove("left")
          except:
            print()
          try:
            if(up_count > down_count):
              possible_moves.remove("up")
            elif(up_count < down_count):
              possible_moves.remove("down")
          except:
            print()
          
      if move == "right":
        next_body = get_next_body(data["you"]["body"], "right")
        next_head = next_body[0]


        # head does not collide with own head, first, second body
        next_body_from_3 = np.array(next_body)[3:]

        if next_head in next_body_from_3:
          try:
            possible_moves.remove("right")
          except:
            print()
          try:
            if(up_count > down_count):
              possible_moves.remove("up")
            elif(up_count < down_count):
              possible_moves.remove("down")
          except:
            print()

    # isDeadEnd = avoid_dead_end(data["you"]["body"], possible_moves)
  
    # try:
    #   if(isDeadEnd != "nothing"):
    #     possible_moves.remove(isDeadEnd)
    # except:
    #   print()


    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # 1. find the closest food from head
    my_head = data["you"]["head"]
    foods = data["board"]["food"]

    distance_to_foods = []

    index = 0
    closest_food_index = 0

    for food in foods:
      distance_to_food_x = abs(food["x"]-my_head["x"])
      distance_to_food_y = abs(food["y"]-my_head["y"])

      distance_to_food = distance_to_food_x + distance_to_food_y

      if(index > 0) :
        if(distance_to_food < distance_to_foods[closest_food_index]):
          closest_food_index = index
      
      distance_to_foods.append(distance_to_food)
      index += 1

    closest_food = foods[closest_food_index]

    # 2. choose move toward the food
    recommend_possible_moves = possible_moves.copy()
    try:
      if(closest_food["y"] == my_head["y"]):
        recommend_possible_moves.remove("down")
    except:
      print()

    try:
      if(closest_food["y"] == my_head["y"]):
        recommend_possible_moves.remove("up")
    except:
      print()

    try:
      if(closest_food["y"] > my_head["y"]):
        recommend_possible_moves.remove("down")
    except:
      print()

    try:
      if(closest_food["y"] < my_head["y"]):
        recommend_possible_moves.remove("up")
    except:
      print()

    try:
      if(closest_food["x"] == my_head["x"]):
        recommend_possible_moves.remove("left")
    except:
      print()

    try:
      if(closest_food["x"] == my_head["x"]):
        recommend_possible_moves.remove("right")
    except:
      print()

    try:
      if(closest_food["x"] > my_head["x"]):
        recommend_possible_moves.remove("left")
    except:
      print()

    try:      
      if(closest_food["x"] < my_head["x"]):
        recommend_possible_moves.remove("right")
    except:
      print()

    if(len(recommend_possible_moves) != 0):
      possible_moves = recommend_possible_moves

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
