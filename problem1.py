import os
import cv2
import sys
import numpy as np

def headshot_extractor(input_image_path, output_folder_path, haar_cascade_path):

    # Checking the image path if exists read it with OpenCV
    if os.path.exists(input_image_path):
        input_image = cv2.imread(input_image_path)
    else:
        print("Image not found. Please check the path")
        return 

    # If output folder not exists create a new directory
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Checking the cascade path
    if os.path.exists(haar_cascade_path):
        face_cascade = cv2.CascadeClassifier(haar_cascade_path)
    else:
        print("Haar cascade not found. Please check the path.")
        return
    
    # Grayscaling the image for cascade detector
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # Running the cascade for face detection
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    # Iterating and saving the face images
    for index, (x,y,w,h) in enumerate (faces):
        roi_color = input_image[y:y+h, x:x+w]
        image_name = output_folder_path + "\\" + input_image_path.split('\\')[-1].split('.')[0] + "_face_" + str(index) + "." + input_image_path.split('\\')[-1].split('.')[1]
        cv2.imwrite(image_name, roi_color)
        print("Image ", image_name, " saved.")

    print("Number of faces: ", len(faces))



input_image_path = sys.argv[1] # Example: "TestInputs\\test2.png"
output_folder_path = sys.argv[2] # Example: "Outputs"
haar_cascade_path = sys.argv[3] # Example: "haarcascade_frontalface_default.xml"

headshot_extractor(input_image_path, output_folder_path, haar_cascade_path)