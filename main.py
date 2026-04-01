# Main Python file for openCV practice (spring 2026)

# Imported Libraries
import cv2
import numpy as np

## Project Idea: 
# Draw a number or something using a paint popup window to create training data
# Use some AI to learn a python program to identify new drawing based on the training data

# Initialize canvas
canvas = np.zeros((512, 512, 1), np.uint8)

print("Space - skip\nEnter - save")

# Program loop
while True:
    cv2.imshow("My First Project", canvas)
    key = cv2.waitKey(1) & 0xFF
    
    # quit
    if key == 32 or key == 13: # Space or Enter(CR)
        # [ save the image here ]
        break
    #elif mouse_down:
        # [ mark the image / release ink ]

cv2.destroyAllWindows()
