# Main Python file for openCV practice (spring 2026)
# Author: Gustav Sand 2026-04-01

## Project Idea:
# Draw a number or something using a paint popup window to create training data
# Use some AI to learn a python program to identify new drawing based on the training data

# Standard libraries:
import os 

# Third-party libraries:
import cv2
import numpy as np
import tensorflow as tf

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
    n = 5 # Square size

    # Switch drawing state and deaw under mouse pointer:
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        canvas[y-n:y+n, x-n:x+n] = 0 # start WITH this first square
    if event == cv2.EVENT_LBUTTONUP:
        drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True: 
            # kan rita lite utanför canvas - TODO: bugfix!
            canvas[y-n:y+n, x-n:x+n] = 0 # Draw with squares

def image_processing(drawing):
    # Should work both with .png and matrix
    temp_drawing = drawing.copy() # Im scared
    temp_drawing = cv2.resize(temp_drawing, (64, 64))
    return temp_drawing

def print_instructions_on_entry(state, last_printed_STATE):
    # prints instructions if not already printed
    # Function returns current state to update "last_printed_STATE"
    if state == last_printed_STATE:
        return state
        # set last_printed_STATE = state
    else:
        if state == STATE_COLLECT:
            print("Draw a Square, circle or triangle\nSpace  - clear\nEnter  - save\nEscape - Finish drawing")
        elif state == STATE_STORE:
            print("What have you drawn?\n1 - Square\n2 - Circle\n3 - Triangle\nEnter - Other\nEscape - ESCAPE!")
        elif state == STATE_TRAIN:
            print("Training AI...")
        elif state == STATE_PREDICT:
            print("Draw something new to test the the CNN!\nSpace - clear\nEnter - predict\ns     - save & label image\nt     - Retrain CNN\nq     - quit")
        return state

initialize_program()

# Program states:            
STATE_COLLECT = 0
STATE_STORE   = 1
STATE_TRAIN   = 2
STATE_PREDICT = 3
current_STATE = STATE_COLLECT
previous_STATE = STATE_COLLECT
last_printed_STATE = None # ONLY FOR UI

# Global variables:
drawing = False

while True:

    # Generate drawings with labels
    if current_STATE == STATE_COLLECT:
        last_printed_STATE = print_instructions_on_entry(current_STATE, last_printed_STATE)

        cv2.imshow("canvasWindow", canvas)
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # Space
            canvas.fill(255)
        elif key == 13: # Enter
            current_STATE = STATE_STORE
        elif key == 27: # Escape
            cv2.moveWindow("canvasWindow", 5000, 5000)
            current_STATE = STATE_TRAIN

    # Label drawings
    elif current_STATE == STATE_STORE:
        last_printed_STATE = print_instructions_on_entry(current_STATE, last_printed_STATE)

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
        elif label_key == 13: # Enter
            label = "other"
        elif label_key == 27: # Escape
            label = "undeclared"
        
        # Save image in labeled folder:
        if label != "undeclared":
            target_dir = f"drawings/{label}" # target_dir - target directory
            os.makedirs(target_dir, exist_ok=True) # If shape-folder soes not exist - create folder
            existing_files = os.listdir(target_dir) # Checks files in target directory
            file_number = len(existing_files) + 1 # Finds the number of files in target directory and decides that the new file gets the next number
            file_path = f"{target_dir}/{label}_{file_number}.png" # new filepath and filename
            cv2.imwrite(file_path, canvas)
            print(f"Saved: {label} with index: {file_number}")
            canvas.fill(255)
            cv2.moveWindow("canvasWindow", 100, 100) # Move back
            
            current_STATE = previous_STATE # Returns to previous state

    # Train AI on drawings
    elif current_STATE == STATE_TRAIN: 
        last_printed_STATE = print_instructions_on_entry(current_STATE, last_printed_STATE)

        # Load training data: [ MAGIC CODE ]
        geometry_drawing = [] # holds processed image of drawing
        geometry_label = [] # holds 0, 1, 2, 3 for Square, Circle, Triangle, Other
        
        categories = ["square", "circle", "triangle", "other"]
        
        # enumerate ger: idx=0, label="square", idx=1, label="circle" osv...
        for idx, label in enumerate(categories):
            target_dir = f"drawings/{label}"
            
            if os.path.exists(target_dir):
                for file in os.listdir(target_dir):
                    file_path = os.path.join(target_dir, file) 
                    # os.path.join är KUNG! (lite säkrare än filsökvägen men inte lika fancy som pathlib)
                    
                    drawing_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    if drawing_image is not None: # Säkerhetskoll om filen är trasig
                        processed_drawing = image_processing(drawing_image)

                        # Save drawing_image and label in lists:
                        geometry_drawing.append(processed_drawing) 
                        geometry_label.append(idx)

        X = np.array(geometry_drawing) # X - list of 2D matrices
        y = np.array(geometry_label) # y - list of labels (0, 1, 2, 3) for (square, circle, triangle, other)

        # Shufle drawings
        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)
        X = X[indices]
        y = y[indices]

        # Split up drawings into training and testing set
        split = int(len(X) * 0.75) # 75% for training, 25% for testing
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        # Normalize pixel values to float 0 - 1 (Beter for training)
        X_train = X_train.astype('float32') / 255.0
        X_test = X_test.astype('float32') / 255.0

        # Generate CNN (with help from my gemeni friend and optimized with "fingerspitz gefiel")
        CNN_model = tf.keras.models.Sequential([ # Sequential ?
            # Input Layer (decided by the drawings shape)
            tf.keras.layers.Input(shape=(64, 64, 1)),
            
            # Feature Extraction
            tf.keras.layers.Conv2D(32, (7, 7), activation='relu'), # convolution filter (48 filters of size 6x6 + ReLU - activtion)
            tf.keras.layers.MaxPooling2D((2, 2)), # Downsampling
            tf.keras.layers.Conv2D(64, (5, 5), activation='relu'), # more conv2 filters (on smaller areas)
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu'), # more conv2 filters (on smaller areas)
            tf.keras.layers.MaxPooling2D((2, 2)),
            # Comment: Features -> downsampling -> Features -> more downsampling -> Features -> more downsampling
            # fewer pixels & bigger scope for each layer

            # Decision Making
            tf.keras.layers.Flatten(), # Flatens out 2D matrix to 1D
            tf.keras.layers.Dense(128, activation='relu'), # decides how to use the features (128 neurons + ReLU)
            tf.keras.layers.Dropout(0.35), # Weird overfitting prevention that turns off neurons

            # Output Layer
            tf.keras.layers.Dense(4, activation='softmax') # 4 outputs (square, circle, triangle, other)
        ]) # Tensorflow makes the CNN harder to understand

        # Train model (Adam - have some momenum & adaptive learning rate)
        custom_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001) # MAX lr = 0.001
        CNN_model.compile(
            optimizer=custom_optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        CNN_model.fit(X_train, y_train, epochs=30, validation_data=(X_test, y_test))

        #  Save model:
        CNN_model.save('geometry_model.keras')
        
        # Continue to prediction state:
        cv2.moveWindow("canvasWindow", 100, 100) 
        current_STATE = STATE_PREDICT

    # Predict geometry on new drawings
    elif current_STATE == STATE_PREDICT:
        last_printed_STATE = print_instructions_on_entry(current_STATE, last_printed_STATE)

        # Show canvas and wait for user to draw something new:
        cv2.imshow("canvasWindow", canvas)
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # Space
            canvas.fill(255)
        elif key == ord('q') or key == 27: # quit (q or escape)
            break
        elif key == 13: # Enter
            print("Predicting...")

            # Behandla användarens bild för att pass modellen:
            test_img = image_processing(canvas) 
            test_img = test_img.astype('float32') / 255.0

            # (batch, height, width, channels) 
            # (64, 64) -> (1, 64, 64, 1) -- "2D -> 4D" (barch of 1 grayscale image)
            test_img = np.expand_dims(test_img, axis=(0, -1))

            # Predict!
            prediction = CNN_model.predict(test_img)

            # Result:
            class_idx = np.argmax(prediction) # Most likeley class
            confidence = np.max(prediction) # Certainty

            # Print:
            labels = ["Kvadrat", "Cirkel", "Triangel", "Other"]
            print(f"Resultat: {labels[class_idx]} ({confidence*100:.1f}% säker)")
            last_printed_STATE = None
            last_printed_STATE = print_instructions_on_entry(current_STATE, last_printed_STATE)
        elif key == ord('s'): # Save image (for later training)
            # Go to saving state and then return!
            previous_STATE = STATE_PREDICT
            current_STATE = STATE_STORE
        elif key == ord('t'): # t - go back and train!
            previous_STATE = STATE_PREDICT
            current_STATE = STATE_TRAIN # Retrain
        
    # Comment: 
    # Challenge: Squares and triangles has similar features
    
    # TODO: Dynamic labeling to predict any kind of drawing decided by dataset or artist
    # Allow Artist to define what should exist in the dataset.

    # TODO: Modify drawings by rotating and moving (maybe "zooming") to increase dataset size
    # Corrects for uncommon angles (eg 45degree square)

    # TODO: Balance dataset
    # Eliminates the risk of model guessing the more common shape

    # TODO: Clean up code and break out into functions and classes
    # Save iamge with label should be its own function
    # Object for canvas and dataset? - idk

cv2.destroyAllWindows()