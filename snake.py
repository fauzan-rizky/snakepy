import os
import time
import copy
import subprocess
import threading
import readchar
from readchar import key

term_size = os.get_terminal_size()
term_columns = term_size.columns
term_lines = term_size.lines
term_lines -= 1
term_columns -= 1
snake_length = 50
spawn_point = [int(round(term_lines) / 2), int(round(term_columns) / 2)+snake_length]  # Y, X
terminal = []
path = []
direction = "none"
for i in range(term_lines):
        terminal.append([])
        for j in range(term_columns):
            terminal[i].append(" ")
for i in range(snake_length):
        if i == 0:
            terminal[spawn_point[0]][spawn_point[1] - i] = ">" 
        else:
            terminal[spawn_point[0]][spawn_point[1] - i] = "#"
        path.append([int(round(term_lines) / 2), int(round(term_columns) / 2) - i])
def update():
    
    terminal = []
    for i in range(term_lines):
        terminal.append([])
        for j in range(term_columns):
            terminal[i].append(" ")
    past_path = copy.deepcopy(path)
    if direction == "right":
        if path[0][1] + 1 >= term_columns:
            path[0][1] = 0
        else:
            path[0][1] += 1
    if direction == "down":
        if path[0][0] + 1 >= term_lines:
            path[0][0] = 0
        else:
            path[0][0] += 1
    if direction == "left":
        if path[0][1] - 1 < 0:           
            path[0][1] = term_columns - 1  
        else:
            path[0][1] -= 1
    if direction == "up":
        if path[0][0] - 1 < 0:           
            path[0][0] = term_lines - 1  
        else:
            path[0][0] -= 1
    for i in range(snake_length):  
        if i == 0:
            pass
        else: 
            path[i] = past_path[(i-1)]
    for i in range(snake_length):
        if i == 0:
            terminal[path[i][0]][path[i][1]] = "█" 
        else:
            terminal[path[i][0]][path[i][1]] = "█"        
    for x in range(term_lines):
        print(*terminal[x], sep="")
frames = 0
direction = "right"
def listen_input():
    global direction
    while True:
        k = readchar.readkey()
        if k == key.UP and direction != "down":
            direction = "up"
        elif k == key.DOWN and direction != "up":
            direction = "down"
        elif k == key.LEFT and direction != "right":
            direction = "left"
        elif k == key.RIGHT and direction != "left":
            direction = "right"
input_thread = threading.Thread(target=listen_input, daemon=True)
input_thread.start()

frames = 1
while True:

    frames += 1
    
    update()
    print(f"score: {snake_length}")
    if frames%5 == 0:
        snake_length+=1
        path.append([0,0])
    
    time.sleep(1/24)
    print("\033[2J")
