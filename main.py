# Main Python file for openCV practice (spring 2026)

# Imported Libraries
import cv2
import numpy as np

## Project Idea:
# Draw a number or something using a paint popup window to create training data
# Use some AI to learn a python program to identify new drawing based on the training data

def mouse_listener(event, x, y, f, p):
    # 'event'   - mouse event type
    # 'x' & 'y' - coordinates
    # 'f' & 'p' - flags & params
    
    global drawing # For editing draving states
    n = 3 # Square size

    # Switch drawing state and deaw under mouse pointer:
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    if event == cv2.EVENT_LBUTTONUP:
        drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            canvas[y-n:y+n, x-n:x+n] = 0 # Draw a small square

# Initialize canvas
canvas = np.zeros((512, 512, 1), np.uint8)
canvas.fill(255) # White background
drawing = False # Decides if mouse is painting
print("Space - skip\nEnter - save")

# Create window and set mouse callback
cv2.namedWindow("canvasWindow")
cv2.setMouseCallback("canvasWindow", mouse_listener)


# Collect drawings: 
index = 1
while True:
    cv2.imshow("canvasWindow", canvas)
    key = cv2.waitKey(1) & 0xFF
    if key == 32: # Space
        canvas.fill(255) # Clear drawing
    elif key == 13: # Enter
        cv2.imwrite("drawings/drawing_" + str(index) + ".png", canvas) # Saves drawing under drawings folder
        index += 1
        canvas.fill(255) # Clear drawing
    elif key == 27: # Escape
        break # Escape matrix

# TODO: Train AI to recognize drawings

# TODO: Use AI to identify new drawings
    

cv2.destroyAllWindows()
