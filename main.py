# Main Python file for openCV practice (spring 2026)
# Author: Gustav Sand 2026-04-01

## Project Idea:
# Draw a number or something using a paint popup window to create training data
# Use some AI to learn a python program to identify new drawing based on the training data

# Libraries
import os
import cv2
import numpy as np

def initialize_program():
    # Initialize canvas
    canvas = np.zeros((512, 512, 1), np.uint8)
    canvas.fill(255) # White background
    print("Draw a Square, circle or triangle\nSpace  - clear\nEnter  - save\nEscape - Finish drawing")

    # Create window and set mouse callback
    cv2.namedWindow("canvasWindow")
    cv2.setMouseCallback("canvasWindow", mouse_listener)

    os.makedirs("drawings", exist_ok=True) # Creates folder for drawings if doesnt exist
    # Comment: YOU CAN DELETE PREVIOUS DRAWINGS MANUALY IF YOU WANT!

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


initialize_program()

# Program states:
STATE_COLLECT = 0
STATE_LABEL   = 1
STATE_TRAIN   = 2
STATE_PREDICT = 3
current_STATE = STATE_COLLECT # Initial state

# Global variables:
index = 1 # Counts drawings
drawing = False # Decides if mouse is painting

while True:

    # Generate drawings with labels
    if current_STATE == STATE_COLLECT:
        cv2.imshow("canvasWindow", canvas)
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # Space
            canvas.fill(255) # Clear drawing (retry)
        elif key == 13: # Enter
            # Define label for drawing and save drawing
            print("What have you drawn?\n1 - Square\n2 - Circle\n3 - Triangle")
            current_STATE = STATE_LABEL # Switch state to label drawing
        elif key == 27: # Escape
            current_STATE = STATE_TRAIN # Escapes state

    # Label drawings
    elif current_STATE == STATE_LABEL:
        # Force the artist to take a brak and label the drawing
        cv2.moveWindow("canvasWindow", 5000, 5000) # Moves the window in a weird way (lower right corner of my screen)
        label_key = cv2.waitKey(1) & 0xFF
        label = "undeclared"
        if label_key == 49: # '1'
            label = "square"
        elif label_key == 50: # '2'
            label = "circle"
        elif label_key == 51: # '3'
            label = "triangle"
        elif label_key == 27 or label_key == 13: # Escape or Enter
            label = "other"
        else:
            pass
        if label != "undeclared":
            cv2.imwrite("drawings/drawing_" + str(index) + "_ " + label + ".png", canvas) # Saves drawing under drawings folder
            index += 1
            canvas.fill(255) # Clear drawing
            cv2.moveWindow("canvasWindow", 100, 100) # Moves "back" the window
            current_STATE = STATE_COLLECT # Continue collecting drawings

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
