# Main Python file for openCV practice (spring 2026)
# Author: Gustav Sand 2026-04-01

## Project Idea:
# Draw a number or something using a paint popup window to create training data
# Use some AI to learn a python program to identify new drawing based on the training data

# Libraries
import cv2
import numpy as np

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


# Program states:
STATE_COLLECT = 0
STATE_TRAIN   = 1
STATE_PREDICT = 2
current_STATE = STATE_COLLECT # Initial state

index = 1 # Counts drawings

while True:

    # Generate drawings with labels
    if current_STATE == STATE_COLLECT:
        cv2.imshow("canvasWindow", canvas)
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # Space
            canvas.fill(255) # Clear drawing
        elif key == 13: # Enter
            cv2.imwrite("drawings/drawing_" + str(index) + ".png", canvas) # Saves drawing under drawings folder
            index += 1
            canvas.fill(255) # Clear drawing
        elif key == 27: # Escape
            current_STATE = STATE_TRAIN # Escapes state

    # Train AI
    elif current_STATE == STATE_TRAIN:
        # TODO: Train AI to recognize drawings
        print("Training AI...")
        pass

    # Test AI
    elif current_STATE == STATE_PREDICT:
        # TODO: Use AI to identify new drawings
        print("Predicting...")
        pass
    

cv2.destroyAllWindows()
