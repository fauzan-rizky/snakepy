import os
import sys
import time
import copy
import random
from readchar import key
from blessed import Terminal

term_size = os.get_terminal_size()
term_columns = term_size.columns
term_lines = term_size.lines
term_lines -= 0
term_columns -= 0
snake_length = 10
spawn_point = [int(round(term_lines) / 2), int(round(term_columns) / 2)+snake_length]  # Y, X
terminal = []
path = []
direction = "none"

term = Terminal()

apple_location = []
apple_exists = False

for i in range(term_lines):
        terminal.append([])
        for j in range(term_columns):
            terminal[i].append(" ")

for i in range(snake_length):
        if i == 0:
            terminal[spawn_point[0]][spawn_point[1] - i] = "#" 
        else:
            terminal[spawn_point[0]][spawn_point[1] - i] = "#"
        path.append([int(round(term_lines) / 2), int(round(term_columns) / 2) - i])

def listen_input():
    global direction
    val = term.inkey(timeout=0.001)
    if val.name == "KEY_UP" and direction != "down":
        direction = "up"
    elif val.name == "KEY_DOWN" and direction != "up":
        direction = "down"
    elif val.name == "KEY_LEFT" and direction != "right":
        direction = "left"
    elif val.name == "KEY_RIGHT" and direction != "left":
        direction = "right"
    elif val.lower() == 'q':
        game_over()

def generate_apple():
    global terminal, apple_exists, apple_location
    if apple_location == [] and apple_exists == False:
        apple_location = [random.randint(5, term_lines-5), random.randint(5,term_columns-5)]
        apple_exists = True
    else:
        pass

def check_meal(head):
    global apple_location, apple_exists, snake_length, path
    if head == apple_location:
        apple_exists = False
        apple_location = []
        snake_length += 1
        path.append([0,0])

def check_collision(target, checkpath):
    if target in checkpath:
        game_over()

def render_terminal():
    global terminal, term_lines, term_columns
    terminal = []
    for i in range(term_lines):
        terminal.append([])
        for j in range(term_columns):
            terminal[i].append(" ")

def draw_border():
    
    global term, term_columns, term_lines
    print(term.clear())
    bars = ["█" for i in range(term_columns)]
    for i in range(term_lines):
        if i == 0 or i == term_lines - 1:
            with term.location(x=0,y=i):
                print("".join(bars), end="")
        else:    
            with term.location(x=0, y=i):
                print("█", end="")
            with term.location(x=term_columns,y=i):
                print("█", end="")

def draw_snake():
    global path
    for entry in path:
        with term.location(entry[1], entry[0]):
            print("#")
    
def update():

    render_terminal()
    
    past_path = copy.deepcopy(path)

    if direction == "right":
        if path[0][1] + 1 >= term_columns:
            game_over()
        else:
            path[0][1] += 1
            check_collision(path[0], past_path)
    if direction == "down":
        if path[0][0] + 1 >= term_lines:
            game_over()
        else:
            path[0][0] += 1
            check_collision(path[0], past_path)
    if direction == "left":
        if path[0][1] - 1 < 0:           
            game_over()
        else:
            path[0][1] -= 1
            check_collision(path[0], past_path)
    if direction == "up":
        if path[0][0] - 1 < 0:           
            game_over() 
        else:
            path[0][0] -= 1
            check_collision(path[0], past_path)

    for i in range(snake_length):  
        if i == 0:
            pass
        else: 
            path[i] = past_path[(i-1)]

    for i in range(snake_length):
        if i == 0:
            terminal[path[i][0]][path[i][1]] = "#" 
        else:
            terminal[path[i][0]][path[i][1]] = "#" 

    generate_apple()
    terminal[apple_location[0]][apple_location[1]] = "Q"
    
    draw_border()
    draw_snake()

    with term.location(apple_location[1],apple_location[0]):
            print("Q")
 
def game_over():
    print(term.clear())
    print("GAME OVER!")
    print(f"Score: {snake_length-10}")
    sys.exit()

frames = 0
direction = "right"

frames = 1

with term.hidden_cursor(), term.cbreak():
    while True:

        listen_input()

        update()

        check_meal(path[0])
        score_counter = f"score: {snake_length-10}"
        margins = [" " for x in range((term_columns//2)-len(score_counter)//2)]


        time.sleep(1/10)
