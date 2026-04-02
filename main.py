# Main Python file for openCV practice (spring 2026)
# Author: Gustav Sand 2026-04-01

## Project Idea:
# Draw a number or something using a paint popup window to create training data
# Use some AI to learn a python program to identify new drawing based on the training data

# Libraries
import os
import cv2
import numpy as np
import tensorflow as tf # Or is PyTorch better?

def initialize_program():
    global canvas

    # Initialize canvas
    canvas = np.zeros((512, 512, 1), np.uint8)
    canvas.fill(255) # White background

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

def image_processing(drawing):
    # Should work both with .png and matrix
    temp_drawing = drawing.copy() # Im scared
    temp_drawing = cv2.resize(temp_drawing, (64, 64))
    return temp_drawing


initialize_program()

# Program states:
STATE_COLLECT = 0
STATE_STORE   = 1
STATE_TRAIN   = 2
STATE_PREDICT = 3
current_STATE = STATE_COLLECT # Initial state

# Global variables:
index = 1 # Counts drawings
drawing = False # Decides if mouse is painting

print("Draw a Square, circle or triangle\nSpace  - clear\nEnter  - save\nEscape - Finish drawing")

while True:

    # Generate drawings with labels
    if current_STATE == STATE_COLLECT:
        cv2.imshow("canvasWindow", canvas)
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # Space
            canvas.fill(255) # Clear drawing (retry)
        elif key == 13: # Enter
            # Define label for drawing and save drawing
            print("What have you drawn?\n1 - Square\n2 - Circle\n3 - Triangle\nEscape or Enter - Other")
            current_STATE = STATE_STORE # Switch state to label drawing
        elif key == 27: # Escape
            cv2.moveWindow("canvasWindow", 5000, 5000)
            current_STATE = STATE_TRAIN # Escapes state

    # Label drawings
    elif current_STATE == STATE_STORE:
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
        
        # Save image in labeled folder:
        if label != "undeclared":
            target_dir = f"drawings/{label}" # target_dir - the new target direction for new drawing
            os.makedirs(target_dir, exist_ok=True) # If not exist - create
            existing_files = os.listdir(target_dir) # Checkar vilka filer som finns i "target_dir" (mappen för geometrin)
            file_number = len(existing_files) + 1 # Finds the number of files and decides that the new file gets the next number
            file_path = f"{target_dir}/{label}_{file_number}.png" # new filepath and filename
            cv2.imwrite(file_path, canvas) # saves drawing
            print(f"Check! Sparade {label} som nummer {file_number}") # debugg
            canvas.fill(255) # clear canvas
            cv2.moveWindow("canvasWindow", 100, 100) # Move back
            
            current_STATE = STATE_COLLECT
            print("Draw a Square, circle or triangle\nSpace  - clear\nEnter  - save\nEscape - Finish drawing")

    # Train AI
    elif current_STATE == STATE_TRAIN:
        # Train AI to recognize drawings
        print("Training AI...")
        # TODO: 
        # make trainingdata by hand
        # Load drawings and labels, preprocess data, define and train model
        # Image processing?
        # CNN > ANN
        # Start with processing Circle image:

        # TODO Load training data: [ MAGIC CODE ]
        geometry_drawing = [] # holds processed image of drawing
        geometry_label = [] # holds 0, 1, 2 for Square, Circle, Triangle
        
        categories = ["square", "circle", "triangle"]
        
        # enumerate ger: idx=0, label="square", idx=1, label="circle" osv...
        for idx, label in enumerate(categories):
            target_dir = f"drawings/{label}"
            
            if os.path.exists(target_dir):
                for file in os.listdir(target_dir):
                    file_path = os.path.join(target_dir, file) 
                    # os.path.join är KUNG! (lite säkrare än filsökvägen)
                    
                    drawing = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    if drawing is not None: # Säkerhetskoll om filen är trasig
                        processed_drawing = image_processing(drawing)

                        # Save drawing and label in lists:
                        geometry_drawing.append(processed_drawing) 
                        geometry_label.append(idx)

        X = np.array(geometry_drawing) # X - list of 2D matrices
        y = np.array(geometry_label) # y - list of labels (0, 1, 2) for (square, circle, triangle)


        # Thoughts:
        # We need more data than someone wants to draw simple images in this program!
        # Solution, save the existing data in a practical way first - making it easier later on!
        # Later: optimize AI to train on less data (maybe copy and modfy existing data)


        pass

    # Test AI
    elif current_STATE == STATE_PREDICT:
        # TODO: Use AI to identify new drawings
        print("Predicting...")
        pass
    

cv2.destroyAllWindows()
