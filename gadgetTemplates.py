#%%
import svgwrite
import colorsys
# dwg = svgwrite.Drawing('gadget_1.svg', profile='tiny', size=(300, 300))

# draw_gadget_1(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, start_x=50, start_y=50)

# dwg.save()

# conversion_factor = 3.78

# def hsl_to_rgb(h, s, l):
#     h = h / 360
#     s = s / 100
#     l = l / 100
#     r, g, b = colorsys.hls_to_rgb(h, l, s)
#     return (int(r*255), int(g*255), int(b*255))

# grid_rgb_color = hsl_to_rgb(0, 0, 48)
# grid_rgb_str = f'rgb({grid_rgb_color[0]},{grid_rgb_color[1]},{grid_rgb_color[2]})'
# valley_rgb_color = hsl_to_rgb(232, 100, 50)
# valley_rgb_str = f'rgb({valley_rgb_color[0]},{valley_rgb_color[1]},{valley_rgb_color[2]})'
# mountain_rgb_color = hsl_to_rgb(0, 100, 50)
# mountain_rgb_str = f'rgb({mountain_rgb_color[0]},{mountain_rgb_color[1]},{mountain_rgb_color[2]})'

# grid_line_width = 0.189
# crease_line_width = 0.325*conversion_factor
# grid_size = 10
# cell_size = 18.9

def draw_up_right(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    rotation = 0
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (0,1,0,2), (1,0,1,1)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,1,2,1)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (0,0,0,1), (1,1,1,2)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (0,2,2,2)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_up_left(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    rotation = 0
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (1,0,1,1), (2,1,2,2)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,1,2,1)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (1,1,1,2), (2,0,2,1)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (0,2,2,2)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_down_right(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    rotation = 0
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (0,0,0,1), (1,1,1,2)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,1,2,1)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (1,0,1,1), (0,1,0,2)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (0,0,2,0)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_down_left(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    rotation = 0
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (1,1,1,2), (2,0,2,1)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,1,2,1)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (1,0,1,1), (2,1,2,2)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (0,0,2,0)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_fold(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    if name == "down":
        rotation = 0
    if name == "right":
        rotation = 270
    if name == "left":
        rotation = 90
    if name == "up":
        rotation = 180
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Horizontal
    horizontal_valley_coords = [
        (0,1,2,1)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Horizontal
    horizontal_mountain_coords = [
        (0,0,2,0)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_transition_form1(dwg, grid_size_x, grid_size_y, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    #adjust rotation here; default = up + l top r bottom
    if name == "transition_up_leftright":
        rotation = 0
    elif name == "transition_down_leftright":
        rotation = 180
    elif name == "transition_left_downup":
        rotation = 270
    elif name == "transition_right_downup":
        rotation = 90

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y

        if rotation == 0:
            return (x0, y0)

        elif rotation == 270:
            new_x = start_x + (y0 - start_y)
            new_y = start_y - (x0 - start_x)
            return (new_x, new_y+grid_size_x*cell_size)
        
        elif rotation == 180:
            new_x = start_x - (x0 - start_x)
            new_y = start_y - (y0 - start_y)
            return (new_x+grid_size_x*cell_size, new_y+grid_size_y*cell_size)

        elif rotation == 90:
            new_x = start_x - (y0 - start_y)
            new_y = start_y + (x0 - start_x)
            return (new_x + grid_size_y*cell_size, new_y)

        
    if rotation == 0 or rotation == 180:
        dwg.add(dwg.rect(
            insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
            size=(grid_size_x*cell_size-crease_line_width, grid_size_y*cell_size-crease_line_width),
            stroke='black',
            fill='white',
            stroke_width=0
        ))
    elif rotation == 90 or rotation == 270:
        dwg.add(dwg.rect(
            insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
            size=(grid_size_y*cell_size-crease_line_width, grid_size_x*cell_size-crease_line_width),
            stroke='black',
            fill='white',
            stroke_width=0
        ))


    for i in range(1, grid_size_x):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size_x), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size_y):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size_y, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (1,0,1,3)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,1,1,1)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Diagonal
    diagonal_valley_coords = [
        (1,1,2,2), (0,2,1,3)
    ]
    for x1, y1, x2, y2 in diagonal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (2,0,2,2), (0,2,0,3)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (1,1,2,1)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))
    # Diagonal
    diagonal_mountain_coords = [
        (0,2,1,1), (1,3,2,2)
    ]
    for x1, y1, x2, y2 in diagonal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_transition_form2(dwg, grid_size_x, grid_size_y, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    #adjust rotation here; default = up + l top r bottom
    if name == "transition_up_rightleft":
        rotation = 0
    elif name == "transition_down_rightleft":
        rotation = 180
    elif name == "transition_left_updown":
        rotation = 270
    elif name == "transition_right_updown":
        rotation = 90

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y

        if rotation == 0:
            return (x0, y0)

        elif rotation == 270:
            new_x = start_x + (y0 - start_y)
            new_y = start_y - (x0 - start_x)
            return (new_x, new_y+grid_size_x*cell_size)
        
        elif rotation == 180:
            new_x = start_x - (x0 - start_x)
            new_y = start_y - (y0 - start_y)
            return (new_x+grid_size_x*cell_size, new_y+grid_size_y*cell_size)

        elif rotation == 90:
            new_x = start_x - (y0 - start_y)
            new_y = start_y + (x0 - start_x)
            return (new_x + grid_size_y*cell_size, new_y)


        
    if rotation == 0 or rotation == 180:
        dwg.add(dwg.rect(
            insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
            size=(grid_size_x*cell_size-crease_line_width, grid_size_y*cell_size-crease_line_width),
            stroke='black',
            fill='white',
            stroke_width=0
        ))
    elif rotation == 90 or rotation == 270:
        dwg.add(dwg.rect(
            insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
            size=(grid_size_y*cell_size-crease_line_width, grid_size_x*cell_size-crease_line_width),
            stroke='black',
            fill='white',
            stroke_width=0
        ))
    for i in range(1, grid_size_x):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size_x), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size_y):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size_y, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (1,0,1,3)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (1,1,2,1)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Diagonal
    diagonal_valley_coords = [
        (0,2,1,1), (1,3,2,2)
    ]
    for x1, y1, x2, y2 in diagonal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (0,0,0,2), (2,2,2,3)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (0,1,1,1)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))
    # Diagonal
    diagonal_mountain_coords = [
        (1,1,2,2), (0,2,1,3)
    ]
    for x1, y1, x2, y2 in diagonal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_gadget_1(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    if name == "one_extruded_u":
        rotation = 0
    elif name == "one_extruded_d":
        rotation = 180
    elif name == "one_extruded_r":
        rotation = 90
    else:
        rotation = 270
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    
    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (2, 0, 2, 3), (2, 4, 2, 6),
        (4, 3, 4, 4), (6, 3, 6, 4),
        (8, 0, 8, 3), (8, 4, 8, 6),
        (3, 8, 3, 10), (7, 8, 7, 10)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0, 3, 10, 3), (0, 7, 2, 7),
        (8, 7, 10, 7), (4, 8, 6, 8)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Diagonal
    diagonal_valley_coords = [
        (2, 7, 4, 6), (3, 8, 4, 6),
        (6, 6, 8, 7), (6, 6, 7, 8),
        (2, 7, 3, 8), (7, 8, 8, 7)
    ]
    for x1, y1, x2, y2 in diagonal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (4, 0, 4, 3), (4, 4, 4, 10),
        (2, 3, 2, 4), (2, 6, 2, 7),
        (8, 3, 8, 4), (8, 6, 8, 7),
        (6, 0, 6, 3), (6, 4, 6, 10)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (0, 4, 10, 4), (0, 6, 10, 6),
        (3, 8, 4, 8), (6, 8, 7, 8)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_gadget_2_ortho(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    if name == "two_extruded_ortho_ur":
        rotation = 0
    elif name == "two_extruded_ortho_dl":
        rotation = 180
    elif name == "two_extruded_ortho_dr":
        rotation = 90
    else:
        rotation = 270
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))

    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (2,0,2,3), (2,4,2,6),
        (3,8,3,10), (4,3,4,4),
        (6,2,6,3), (7,3,7,10),
        (8,0,8,2)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,3,7,3), (8,2,10,2),
        (6,6,7,6), (0,7,2,7),
        (4,8,6,8), (7,8,10,8),
        (6,4,7,4)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Diagonal
    diagonal_valley_coords = [
        (7,3,8,2), (5,3,6,4),
        (2,7,4,6), (3,8,4,6),
        (2,7,3,8)
    ]
    for x1, y1, x2, y2 in diagonal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (2,3,2,4), (2,6,2,7),
        (4,0,4,3), (4,4,4,10),
        (6,0,6,2), (6,3,6,10)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (6,2,8,2), (0,4,6,4),
        (7,4,10,4), (0,6,6,6),
        (7,6,10,6), (3,8,4,8),
        (6,8,7,8)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))
    # Diagonal
    diagonal_mountain_coords = [
        (5,3,6,2), (6,4,7,3)
    ]
    for x1, y1, x2, y2 in diagonal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_gadget_2_linear(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    if name == "two_extruded_linear_ud":
        rotation = 0
    else:
        rotation = 90
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))

    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (2,0,2,3), (2,4,2,6),
        (2,7,2,10), (4,3,4,4),
        (4,6,4,7), (6,3,6,4),
        (6,6,6,7), (8,0,8,3),
        (8,4,8,6), (8,7,8,10)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,3,10,3), (0,7,10,7)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Diagonal
    diagonal_valley_coords = [
        
    ]
    for x1, y1, x2, y2 in diagonal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (4,0,4,3), (4,4,4,6),
        (4,7,4,10), (6,0,6,3),
        (6,4,6,6), (6,7,6,10),
        (2,3,2,4), (2,6,2,7),
        (8,3,8,4), (8,6,8,7)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (0,4,10,4), (0,6,10,6)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))
    # Diagonal
    diagonal_mountain_coords = [
        
    ]
    for x1, y1, x2, y2 in diagonal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_gadget_3(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    if name == "three_extruded_u":
        rotation = 0
    elif name == "three_extruded_d":
        rotation = 180
    elif name == "three_extruded_r":
        rotation = 90
    else:
        rotation = 270
    
    cx = start_x + (grid_size * cell_size) / 2
    cy = start_y + (grid_size * cell_size) / 2

    def translate(x, y):
        x0 = start_x + x
        y0 = start_y + y
        if rotation == 0:
            return (x0, y0)
        elif rotation == 90:
            return (cx - (y0 - cy), cy + (x0 - cx))
        elif rotation == 180:
            return (cx - (x0 - cx), cy - (y0 - cy))
        elif rotation == 270:
            return (cx + (y0 - cy), cy - (x0 - cx))
        
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))

    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (2,0,2,2), (3,3,3,10),
        (4,3,4,4), (6,2,6,3),
        (7,3,7,10), (8,0,8,2)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (0,2,2,2), (8,2,10,2),
        (2,4,3,4), (6,4,7,4),
        (3,3,7,3), (3,6,4,6),
        (6,6,7,6), (0,8,3,8),
        (4,8,6,8), (7,8,10,8)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Diagonal
    diagonal_valley_coords = [
        (2,2,3,3), (7,3,8,2),
        (5,3,6,4), (3,5,4,4)
    ]
    for x1, y1, x2, y2 in diagonal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (2,2,2,4), (4,0,4,3),
        (4,4,4,10), (6,0,6,2),
        (6,3,6,10)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (6,2,8,2), (0,4,2,4),
        (3,4,6,4), (7,4,10,4),
        (0,6,3,6), (4,6,6,6),
        (7,6,10,6), (3,8,4,8),
        (6,8,7,8)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))
    # Diagonal
    diagonal_mountain_coords = [
        (5,3,6,2), (3,3,4,4),
        (6,4,7,3), (2,4,3,5)
    ]
    for x1, y1, x2, y2 in diagonal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

def draw_gadget_4(dwg, grid_size, cell_size, grid_rgb_str, grid_line_width, valley_rgb_str, crease_line_width, mountain_rgb_str, name, start_x, start_y):
    def translate(x, y):
        return (start_x + x, start_y + y)
    dwg.add(dwg.rect(
        insert=(start_x+crease_line_width/2, start_y+crease_line_width/2),
        size=(grid_size*cell_size-crease_line_width, grid_size*cell_size-crease_line_width),
        stroke='black',
        fill='white',
        stroke_width=0
    ))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(i*cell_size, 0), end=translate(i*cell_size, cell_size*grid_size), stroke=grid_rgb_str, stroke_width=grid_line_width))
    for i in range(1, grid_size):
        dwg.add(dwg.line(start=translate(0, i*cell_size), end=translate(cell_size*grid_size, i*cell_size), stroke=grid_rgb_str, stroke_width=grid_line_width))

    # Draw valley folds
    # Vertical
    vertical_valley_coords = [
        (2,0,2,2), (2,8,2,10),
        (3,3,3,7), (4,3,4,4),
        (4,7,4,8), (6,2,6,3),
        (6,6,6,7), (7,3,7,7),
        (8,0,8,2), (8,8,8,10)
    ]
    for x1, y1, x2, y2 in vertical_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_valley_coords = [
        (10,2, 8,2), (2,2, 0,2),
        (7,3, 3,3), (7,4, 6,4),
        (3,4, 2,4), (8,6, 7,6),
        (4,6, 3,6), (7,7, 3,7),
        (10,8, 8,8), (2,8, 0,8)
    ]
    for x1, y1, x2, y2 in horizontal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Diagonal
    diagonal_valley_coords = [
        (2,2,3,3), (7,3,8,2),
        (5,3,6,4), (3,5,4,4),
        (6,6,7,5), (4,6,5,7),
        (2,8,3,7), (7,7,8,8)
    ]
    for x1, y1, x2, y2 in diagonal_valley_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=valley_rgb_str, stroke_width=crease_line_width))

    # Draw mountain folds
    # Vertical
    vertical_mountain_coords = [
        (2,2,2,4), (4,0,4,3),
        (4,4,4,7), (4,8,4,10),
        (6,0,6,2), (6,3,6,6),
        (6,7,6,10), (8,6,8,8)
    ]
    for x1, y1, x2, y2 in vertical_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))

    # Horizontal
    horizontal_mountain_coords = [
        (8,2, 6,2), (10,4, 7,4),
        (6,4, 3,4), (2,4, 0,4),
        (10,6, 8,6), (7,6, 4,6),
        (3,6, 0,6), (4,8, 2,8)
    ]
    for x1, y1, x2, y2 in horizontal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))
    # Diagonal
    diagonal_mountain_coords = [
        (5,3,6,2), (3,3,4,4),
        (6,4,7,3), (2,4,3,5),
        (7,5,8,6), (3,7,4,6),
        (6,6,7,7), (4,8,5,7)
    ]
    for x1, y1, x2, y2 in diagonal_mountain_coords:
        dwg.add(dwg.line(start=translate(x1*cell_size, y1*cell_size), end=translate(x2*cell_size, y2*cell_size), stroke=mountain_rgb_str, stroke_width=crease_line_width))
# %%
