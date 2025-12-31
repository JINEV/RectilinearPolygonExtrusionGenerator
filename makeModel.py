#%%
import ipywidgets as widgets
import numpy as np
from IPython.display import display
from gadgetTemplates import draw_gadget_1, draw_gadget_2_ortho, draw_gadget_2_linear, draw_gadget_3, draw_gadget_4, draw_down_left, draw_down_right, draw_up_left, draw_up_right, draw_fold, draw_transition_form1, draw_transition_form2
import svgwrite
import colorsys

conversion_factor = 3.78

def hsl_to_rgb(h, s, l):
    h = h / 360
    s = s / 100
    l = l / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r*255), int(g*255), int(b*255))
def determine_Gadget(upper, lower, left, right):
    if upper+lower+left+right == 0:
        return "zero_extruded"
    elif upper+lower+left+right == 4:
        return "four_extruded"
    elif upper+lower+left+right == 1:
        if upper == 1:
            return "one_extruded_u"
        if lower == 1:
            return "one_extruded_d"
        if left == 1:
            return "one_extruded_l"
        else:
            return "one_extruded_r"
    elif upper+lower+left+right == 3:
        if upper == 0:
            return "three_extruded_d"
        if lower == 0:
            return "three_extruded_u"
        if left == 0:
            return "three_extruded_r"
        else:
            return "three_extruded_l"
    else:
        if upper == 1 and lower == 1:
            return "two_extruded_linear_ud"
        if left == 1 and right == 1:
            return "two_extruded_linear_lr"
        if upper == 1 and left == 1:
            return "two_extruded_ortho_ul"
        if upper == 1 and right == 1:
            return "two_extruded_ortho_ur"
        if lower == 1 and left == 1:
            return "two_extruded_ortho_dl"
        if lower == 1 and right == 1:
            return "two_extruded_ortho_dr"
def index_prefix(list, string):
    for index, prefix in enumerate(list):
        if string.startswith(prefix):
            return index
        
grid_rgb_color = hsl_to_rgb(0, 0, 48)
grid_rgb_str = f'rgb({grid_rgb_color[0]},{grid_rgb_color[1]},{grid_rgb_color[2]})'
valley_rgb_color = hsl_to_rgb(232, 100, 50)
valley_rgb_str = f'rgb({valley_rgb_color[0]},{valley_rgb_color[1]},{valley_rgb_color[2]})'
mountain_rgb_color = hsl_to_rgb(0, 100, 50)
mountain_rgb_str = f'rgb({mountain_rgb_color[0]},{mountain_rgb_color[1]},{mountain_rgb_color[2]})'

grid_line_width = 0.189
crease_line_width = 0.325*conversion_factor
grid_size = 10
cell_size = 18.9

priority = ["two_extruded_linear", "one_extruded", "priority_two_extruded_linear", "priority_one_extruded", "two_extruded_ortho", "three_extruded", "four_extruded"]
functions = [draw_gadget_2_linear, draw_gadget_1, draw_gadget_2_linear, draw_gadget_1, draw_gadget_2_ortho, draw_gadget_3, draw_gadget_4]
#%%
grid_state = None
colored_squares = []
num_columns = 0
num_rows = 0

def create_grid(rows, cols):
    global grid_state
    grid_state = np.zeros((rows, cols), dtype=int)

    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            button = widgets.Button(
                description='',
                layout=widgets.Layout(width='100%', height='100%', border='1px solid gray')
            )
            button.style.button_color = 'white'
            button.on_click(lambda b, r=r, c=c: on_button_click(b, r, c))
            row.append(button)
        grid.append(row)
    
    return grid

def on_button_click(button, row, col):
    global grid_state
    if button.style.button_color == 'white':
        button.style.button_color = 'black'
        grid_state[row, col] = 1
        colored_squares.append([row, col])
    else:
        button.style.button_color = 'white'
        grid_state[row, col] = 0
        colored_squares.remove([row,col])

def display_grid():
    global num_columns
    global num_rows
    cols = int(input("Enter canvas width: "))
    num_columns = cols
    rows = int(input("Enter canvas height: "))
    num_rows = rows

    grid = create_grid(rows, cols)

    grid_layout = widgets.GridBox(
        children=[button for row in grid for button in row],
        layout=widgets.Layout(
            grid_template_columns=' '.join(['1fr']*cols),
            grid_template_rows=' '.join(['1fr']*rows),
            width='300px',
            height='300px',
            justify_items='center',
            align_items='center'
        )
    )
    square_layout = widgets.Layout(
        width='80vmin',
        height='80vmin',
        justify_content='center',
        align_items='center'
    )
    display(widgets.Box([grid_layout], layout=square_layout))

display_grid()
#%%
gadget_names = []
gadget_names_grid = [[None for _ in range(num_columns)] for _ in range(num_rows)]
to_remove = []

for x, y in colored_squares:
    gadget_name = determine_Gadget(grid_state[x-1, y], grid_state[x+1, y], grid_state[x, y-1], grid_state[x, y+1])
    gadget_names.append(gadget_name)
    gadget_names_grid[x][y] = gadget_name

print("Gadget Layering Iteration 1")
for gadget_row in gadget_names_grid:
    print(gadget_row)

for i in range(num_rows):
    current_one = False
    current_one_index = [None, None]
    current_linear = False
    current_linear_index = [None, None]
    for j in range(num_columns):
        if gadget_names_grid[i][j] is not None:
            if gadget_names_grid[i][j].startswith("two_extruded_linear") and not current_one:
                current_linear = True
                current_linear_index=[i,j]
            elif gadget_names_grid[i][j].startswith("two_extruded_linear") and current_one:
                if abs(j-current_one_index[1]) > 1:
                    gadget_names_grid[i][j] = "priority_" + gadget_names_grid[i][j]
                current_one = True
                current_one_index = [i,j]
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("two_extruded_ortho") or gadget_names_grid[i][j].startswith("three_extruded_l") or gadget_names_grid[i][j].startswith("three_extruded_r") or gadget_names_grid[i][j].startswith("priority")) and current_linear:
                current_one = True
                current_one_index = [i,j]
                if abs(current_one_index[1]-current_linear_index[1]) > 1:
                    gadget_names_grid[current_linear_index[0]][current_linear_index[1]] = "priority_" + gadget_names_grid[current_linear_index[0]][current_linear_index[1]]
                current_linear = False
                current_linear_index = [None, None]
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("two_extruded_ortho") or gadget_names_grid[i][j].startswith("three_extruded_l") or gadget_names_grid[i][j].startswith("three_extruded_r") or gadget_names_grid[i][j].startswith("priority")) and not current_linear:
                current_one = True
                current_one_index = [i,j]
            else:
                current_one = False
                current_linear = False
                current_linear_index = [None, None]
for j in range(num_columns):
    current_one = False
    current_one_index = [None, None]
    current_linear = False
    current_linear_index = [None, None]
    for i in range(num_rows):
        if gadget_names_grid[i][j] is not None:
            if gadget_names_grid[i][j].startswith("two_extruded_linear") and not current_one:
                current_linear = True
                current_linear_index=[i,j]
            elif gadget_names_grid[i][j].startswith("two_extruded_linear") and current_one:
                if abs(i-current_one_index[0]) > 1:
                    gadget_names_grid[i][j] = "priority_" + gadget_names_grid[i][j]
                current_one = True
                current_one_index = [i,j]
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("two_extruded_ortho") or gadget_names_grid[i][j].startswith("three_extruded_u") or gadget_names_grid[i][j].startswith("three_extruded_d") or gadget_names_grid[i][j].startswith("priority")) and current_linear:
                current_one = True
                current_one_index = [i,j]
                if abs(current_one_index[0]-current_linear_index[0]) > 1:
                    gadget_names_grid[current_linear_index[0]][current_linear_index[1]] = "priority_" + gadget_names_grid[current_linear_index[0]][current_linear_index[1]]
                current_linear = False
                current_linear_index = [None, None]
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("two_extruded_ortho") or gadget_names_grid[i][j].startswith("three_extruded_u") or gadget_names_grid[i][j].startswith("three_extruded_d") or gadget_names_grid[i][j].startswith("priority")) and not current_linear:
                current_one = True
                current_one_index = [i,j]
            else:
                current_one = False
                current_linear = False
                current_linear_index = [None, None]

for i in range(num_rows):
    current_one_three = False
    current_one_three_name = None
    current_one = False
    current_one_index = [None, None]
    for j in range(num_columns):
        if gadget_names_grid[i][j] is not None:
            if gadget_names_grid[i][j].startswith("one_extruded_") and not current_one_three:
                current_one = True
                current_one_index=[i,j]
            elif gadget_names_grid[i][j].startswith("one_extruded_") and current_one_three:
                if (gadget_names_grid[i][j][-2:] == "_u" or gadget_names_grid[i][j][-2:] == "_d") and (current_one_three_name[-2:] == "_l" or current_one_three_name[-2:] == "_r"):
                    gadget_names_grid[i][j] = "priority_" + gadget_names_grid[i][j]
                elif (gadget_names_grid[i][j][-2:] == "_r" or gadget_names_grid[i][j][-2:] == "_l") and (current_one_three_name[-2:] == "_u" or current_one_three_name[-2:] == "_d"):
                    gadget_names_grid[i][j] = "priority_" + gadget_names_grid[i][j]
                current_one_three = False
                current_one_three_name = None
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("three_extruded")) and current_one:
                current_one_three = True
                current_one_three_name = gadget_names_grid[i][j]
                if (gadget_names_grid[i][j][-2:] == "_u" or gadget_names_grid[i][j][-2:] == "_d") and (gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_l" or gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_r"):
                    gadget_names_grid[current_one_index[0]][current_one_index[1]] = "priority_" + gadget_names_grid[current_one_index[0]][current_one_index[1]]
                elif (gadget_names_grid[i][j][-2:] == "_r" or gadget_names_grid[i][j][-2:] == "_l") and (gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_u" or gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_d"):
                    gadget_names_grid[current_one_index[0]][current_one_index[1]] = "priority_" + gadget_names_grid[current_one_index[0]][current_one_index[1]]
                current_one = False
                current_one_index = [None, None]
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("three_extruded")) and not current_linear:
                current_one_three = True
                current_one_three_name = gadget_names_grid[i][j]
            else:
                current_one_three = False
                current_one_three_name = None
                current_one = False
                current_one_index = [None, None]
for j in range(num_columns):
    current_one_three = False
    current_one_three_name = None
    current_one = False
    current_one_index = [None, None]
    for i in range(num_rows):
        if gadget_names_grid[i][j] is not None:
            if gadget_names_grid[i][j].startswith("one_extruded_") and not current_one_three:
                current_one = True
                current_one_index=[i,j]
            elif gadget_names_grid[i][j].startswith("one_extruded_") and current_one_three:
                if (gadget_names_grid[i][j][-2:] == "_u" or gadget_names_grid[i][j][-2:] == "_d") and (current_one_three_name[-2:] == "_l" or current_one_three_name[-2:] == "_r"):
                    gadget_names_grid[i][j] = "priority_" + gadget_names_grid[i][j]
                elif (gadget_names_grid[i][j][-2:] == "_r" or gadget_names_grid[i][j][-2:] == "_l") and (current_one_three_name[-2:] == "_u" or current_one_three_name[-2:] == "_d"):
                    gadget_names_grid[i][j] = "priority_" + gadget_names_grid[i][j]
                current_one_three = False
                current_one_three_name = None
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("three_extruded")) and current_one:
                current_one_three = True
                current_one_three_name = gadget_names_grid[i][j]
                if (gadget_names_grid[i][j][-2:] == "_u" or gadget_names_grid[i][j][-2:] == "_d") and (gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_l" or gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_r"):
                    gadget_names_grid[current_one_index[0]][current_one_index[1]] = "priority_" + gadget_names_grid[current_one_index[0]][current_one_index[1]]
                elif (gadget_names_grid[i][j][-2:] == "_r" or gadget_names_grid[i][j][-2:] == "_l") and (gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_u" or gadget_names_grid[current_one_index[0]][current_one_index[1]][-2:] == "_d"):
                    gadget_names_grid[current_one_index[0]][current_one_index[1]] = "priority_" + gadget_names_grid[current_one_index[0]][current_one_index[1]]
                current_one = False
                current_one_index = [None, None]
            elif (gadget_names_grid[i][j].startswith("one_extruded") or gadget_names_grid[i][j].startswith("three_extruded")) and not current_linear:
                current_one_three = True
                current_one_three_name = gadget_names_grid[i][j]
            else:
                current_one_three = False
                current_one_three_name = None
                current_one = False
                current_one_index = [None, None]

print("Gadget Layering Iteration 2")
for gadget_row in gadget_names_grid:
    print(gadget_row)
#%%
#adding filler creases
filler_edge_creases_vert = [[None for _ in range(num_columns-1)] for _ in range(num_rows)]
for i in range(num_rows):
    for j in range(num_columns):
        if gadget_names_grid[i][j] is not None:
            filler_edge_creases_vert[i-1][j-1] = "fill"
            filler_edge_creases_vert[i-1][j] = "fill"
            filler_edge_creases_vert[i][j-1] = "fill"
            filler_edge_creases_vert[i][j] = "fill"
            filler_edge_creases_vert[i+1][j-1] = "fill"
            filler_edge_creases_vert[i+1][j] = "fill"

#down to top vert
for j in range(num_columns-1):
    cur_fill = False
    direction = None
    for i in reversed(range(num_rows)):
        if filler_edge_creases_vert[i][j] is None and cur_fill:
            cur_fill = False
            candidate_gadgets = [[i+2,j],[i+2,j+1]]
            selection_priorities = [-10, -10]
            for idx, candidate_gadget in enumerate(candidate_gadgets):
                if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                    if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                        selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
            if selection_priorities[0] > selection_priorities[1]:
                direction = "right"
            elif selection_priorities[1] > selection_priorities[0]:
                direction = "left"
            else:
                direction = "left"
            filler_edge_creases_vert[i][j] = direction
        elif direction is not None and filler_edge_creases_vert[i][j] is None:
            filler_edge_creases_vert[i][j] = direction
        elif filler_edge_creases_vert[i][j] == "fill":
            cur_fill  = True
            direction = None

#top to down vert
for j in range(num_columns-1):
    cur_fill = False
    direction = None
    for i in range(num_rows):
        if filler_edge_creases_vert[i][j] != "fill" and cur_fill:
            cur_fill = False
            candidate_gadgets = [[i-2,j],[i-2,j+1]]
            selection_priorities = [-10, -10]
            for idx, candidate_gadget in enumerate(candidate_gadgets):
                if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                    if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                        selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
            if selection_priorities[0] > selection_priorities[1]:
                direction = "right"
            elif selection_priorities[1] > selection_priorities[0]:
                direction = "left"
            else:
                direction = "left"
            if filler_edge_creases_vert[i][j] is not None:
                if direction != filler_edge_creases_vert[i][j]:
                    existing = filler_edge_creases_vert[i][j]
                    filler_edge_creases_vert[i][j] = direction
                    direction = existing
                else:
                    filler_edge_creases_vert[i][j] = direction
            else:
                filler_edge_creases_vert[i][j] = direction
        elif direction is not None and filler_edge_creases_vert[i][j] != "fill":
            filler_edge_creases_vert[i][j] = direction
        elif filler_edge_creases_vert[i][j] == "fill":
            cur_fill  = True
            direction = None
#%%
filler_edge_creases_horiz = [[None for _ in range(num_columns)] for _ in range(num_rows-1)]
for i in range(num_rows):
    for j in range(num_columns):
        if gadget_names_grid[i][j] is not None:
            filler_edge_creases_horiz[i-1][j-1] = "fill"
            filler_edge_creases_horiz[i-1][j] = "fill"
            filler_edge_creases_horiz[i-1][j+1] = "fill"
            filler_edge_creases_horiz[i][j-1] = "fill"
            filler_edge_creases_horiz[i][j] = "fill"
            filler_edge_creases_horiz[i][j+1] = "fill"

#right to left horiz
for i in range(num_rows-1):
    cur_fill = False
    direction = None
    for j in reversed(range(num_columns)):
        if filler_edge_creases_horiz[i][j] is None and cur_fill:
            cur_fill = False
            candidate_gadgets = [[i,j+2],[i+1,j+2]]
            selection_priorities = [-10, -10]
            for idx, candidate_gadget in enumerate(candidate_gadgets):
                if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                    if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                        selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
            if selection_priorities[0] > selection_priorities[1]:
                direction = "down"
            elif selection_priorities[1] > selection_priorities[0]:
                direction = "up"
            else:
                direction = "up"
            filler_edge_creases_horiz[i][j] = direction
        elif direction is not None and filler_edge_creases_horiz[i][j] is None:
            filler_edge_creases_horiz[i][j] = direction
        elif filler_edge_creases_horiz[i][j] == "fill":
            cur_fill  = True
            direction = None

#left to right horiz
for i in range(num_rows-1):
    cur_fill = False
    direction = None
    for j in range(num_columns):
        if filler_edge_creases_horiz[i][j] != "fill" and cur_fill:
            cur_fill = False
            candidate_gadgets = [[i,j-2],[i+1,j-2]]
            selection_priorities = [-10, -10]
            for idx, candidate_gadget in enumerate(candidate_gadgets):
                if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                    if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                        selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
            if selection_priorities[0] > selection_priorities[1]:
                direction = "down"
            elif selection_priorities[1] > selection_priorities[0]:
                direction = "up"
            else:
                direction = "up"
            if filler_edge_creases_horiz[i][j] is not None:
                if direction != filler_edge_creases_horiz[i][j]:
                    existing = filler_edge_creases_horiz[i][j]
                    filler_edge_creases_horiz[i][j] = direction
                    direction = existing
                else:
                    filler_edge_creases_horiz[i][j] = direction
            else:
                filler_edge_creases_horiz[i][j] = direction
        elif direction is not None and filler_edge_creases_horiz[i][j] != "fill":
            filler_edge_creases_horiz[i][j] = direction
        elif filler_edge_creases_horiz[i][j] == "fill":
            cur_fill  = True
            direction = None
#%%
filler_center_creases = [[None for _ in range(num_columns-1)] for _ in range(num_rows-1)]
for i in range(num_rows):
    for j in range(num_columns): 
        if gadget_names_grid[i][j] is not None:
            filler_center_creases[i-1][j-1] = "fill"
            filler_center_creases[i-1][j] = "fill"
            filler_center_creases[i][j-1] = "fill"
            filler_center_creases[i][j] = "fill"

for i in range(num_rows-1):
    for j in range(num_columns-1):
        if filler_center_creases[i][j] is None:
            #check upper
            if filler_edge_creases_vert[i][j] != "fill":
                up_dir = filler_edge_creases_vert[i][j]
            else:
                candidate_gadgets = [[i-1,j],[i-1,j+1]]
                selection_priorities = [-10, -10]
                for idx, candidate_gadget in enumerate(candidate_gadgets):
                    if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                        if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                            selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
                if selection_priorities[0] > selection_priorities[1]:
                    up_dir = "right"
                elif selection_priorities[1] > selection_priorities[0]:
                    up_dir = "left"
                else:
                    up_dir = "left"
            #check left
            if filler_edge_creases_horiz[i][j] != "fill":
                left_dir = filler_edge_creases_horiz[i][j]
            else:
                candidate_gadgets = [[i,j-1],[i+1,j-1]]
                selection_priorities = [-10, -10]
                for idx, candidate_gadget in enumerate(candidate_gadgets):
                    if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                        if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                            selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
                if selection_priorities[0] > selection_priorities[1]:
                    left_dir = "down"
                elif selection_priorities[1] > selection_priorities[0]:
                    left_dir = "up"
                else:
                    left_dir = "up"
            #check down
            if filler_edge_creases_vert[i+1][j] != "fill":
                down_dir = filler_edge_creases_vert[i+1][j]
            else:
                candidate_gadgets = [[i+2,j],[i+2,j+1]]
                selection_priorities = [-10, -10]
                for idx, candidate_gadget in enumerate(candidate_gadgets):
                    if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                        if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                            selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
                if selection_priorities[0] > selection_priorities[1]:
                    down_dir = "right"
                elif selection_priorities[1] > selection_priorities[0]:
                    down_dir = "left"
                else:
                    down_dir = "left"
            #check right
            if filler_edge_creases_horiz[i][j+1] != "fill":
                right_dir = filler_edge_creases_horiz[i][j+1]
            else:
                candidate_gadgets = [[i,j+2],[i+1,j+2]]
                selection_priorities = [-10, -10]
                for idx, candidate_gadget in enumerate(candidate_gadgets):
                    if candidate_gadget[0] >= 0 and candidate_gadget[0] < num_rows and candidate_gadget[1] >= 0 and candidate_gadget[1] < num_columns:
                        if gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]] is not None:
                            selection_priorities[idx] = index_prefix(priority, gadget_names_grid[candidate_gadget[0]][candidate_gadget[1]])
                if selection_priorities[0] > selection_priorities[1]:
                    right_dir = "down"
                elif selection_priorities[1] > selection_priorities[0]:
                    right_dir = "up"
                else:
                    right_dir = "up"
            if right_dir == left_dir and up_dir == down_dir:
                filler_center_creases[i][j] = left_dir+up_dir
            elif right_dir == left_dir and up_dir != down_dir:
                filler_center_creases[i][j] = "transition_" + left_dir + "_" + up_dir + down_dir
            elif right_dir != left_dir and up_dir == down_dir:
                filler_center_creases[i][j] = "transition_" + up_dir + "_" + left_dir + right_dir
#%%
save_file_temp = input("Enter name for exported .svg file: ")
save_file = save_file_temp + '.svg'
dwg = svgwrite.Drawing(save_file, profile='tiny', size=(cell_size*(num_columns*2-1)*2, cell_size*(num_rows*2-1)*2))
filler_centers = ["upright", "upleft", "downright", "downleft"]
filler_functions = [draw_up_right, draw_up_left, draw_down_right, draw_down_left]

for i in range(len(filler_edge_creases_horiz)):
    for j in range(len(filler_edge_creases_horiz[i])):
        if filler_edge_creases_horiz[i][j] != "fill":
            start_x = (j*4)*cell_size
            start_y = (i*4+2)*cell_size
            draw_fold(dwg, 2, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, filler_edge_creases_horiz[i][j], start_x, start_y)

for i in range(len(filler_edge_creases_vert)):
    for j in range(len(filler_edge_creases_vert[i])):
        if filler_edge_creases_vert[i][j] != "fill":
            start_x = (j*4+2)*cell_size
            start_y = (i*4)*cell_size
            draw_fold(dwg, 2, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, filler_edge_creases_vert[i][j], start_x, start_y)

for i in range(len(filler_center_creases)):
    for j in range(len(filler_center_creases[i])):
        if filler_center_creases[i][j] != "fill":
            if not filler_center_creases[i][j].startswith("transition"):
                start_x = (j*4+2)*cell_size
                start_y = (i*4+2)*cell_size
                filler_functions[filler_centers.index(filler_center_creases[i][j])](dwg, 2, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, filler_center_creases[i][j], start_x, start_y)

for i, gadget_prefix in enumerate(priority):
    for row_index in range(num_rows):
        for column_index in range(num_columns):
            gadget_name = gadget_names_grid[row_index][column_index]
            if gadget_name is not None:
                if gadget_name.startswith(gadget_prefix):
                    start_x = (((column_index)*2)*2-4)*cell_size
                    start_y = (((row_index)*2)*2-4)*cell_size
                    if gadget_name.startswith("priority_"):
                        functions[i](dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, gadget_name[9:], start_x, start_y)
                    else:
                        functions[i](dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, gadget_name, start_x, start_y)
for i in range(len(filler_center_creases)):
    for j in range(len(filler_center_creases[i])):
        if filler_center_creases[i][j] != "fill":
            if filler_center_creases[i][j].startswith("transition"):
                if filler_center_creases[i][j].endswith("leftright") or filler_center_creases[i][j].endswith("downup"):
                    if filler_center_creases[i][j].endswith("up_leftright") or filler_center_creases[i][j].endswith("left_downup"):
                        start_x = (j*4+2)*cell_size
                        start_y = (i*4+2)*cell_size
                    elif filler_center_creases[i][j].endswith("down_leftright"):
                        start_x = (j*4+2)*cell_size
                        start_y = (i*4+2)*cell_size-1*cell_size
                    else:
                        start_x = (j*4+2)*cell_size-1*cell_size
                        start_y = (i*4+2)*cell_size
                    draw_transition_form1(dwg, 2, 3, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, filler_center_creases[i][j], start_x, start_y)
                else:
                    if filler_center_creases[i][j].endswith("up_rightleft") or filler_center_creases[i][j].endswith("left_updown"):
                        start_x = (j*4+2)*cell_size
                        start_y = (i*4+2)*cell_size
                    elif filler_center_creases[i][j].endswith("down_rightleft"):
                        start_x = (j*4+2)*cell_size
                        start_y = (i*4+2)*cell_size-1*cell_size
                    else:
                        start_x = (j*4+2)*cell_size-1*cell_size
                        start_y = (i*4+2)*cell_size
                    draw_transition_form2(dwg, 2, 3, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, filler_center_creases[i][j], start_x, start_y)

for i in range(1, (num_columns*2-1)*2):
    dwg.add(dwg.line(start=(i*cell_size, 0), end=(i*cell_size, cell_size*(num_columns*2-1)*2), stroke=grid_rgb_str, stroke_width=grid_line_width))
for i in range(1, (num_rows*2-1)*2):
    dwg.add(dwg.line(start=(0, i*cell_size), end=(cell_size*(num_rows*2-1)*2, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
dwg.add(dwg.rect(
        insert=(0, 0),
        size=(cell_size*(num_columns*2-1)*2, cell_size*(num_rows*2-1)*2),
        stroke='black',
        fill='none',
        stroke_width=0.584*conversion_factor
    ))
dwg.save()

print("Crease pattern saved to " + save_file)
# %%
