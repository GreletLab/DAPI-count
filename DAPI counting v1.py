import cv2
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label, Scale, HORIZONTAL
import pandas as pd
import os

# Global variables to store the loaded image and threshold
image_resized = None
grayscale_image = None
image_paths = []
threshold_value = 50  # Initial threshold value

# Function to load all images from a selected folder
def load_folder():
    global image_paths
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    if folder_path:
        image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))]
        if image_paths:
            load_first_image(image_paths[0])
    return image_paths

# Function to load the first image for threshold adjustment and convert it to grayscale
def load_first_image(image_path):
    global grayscale_image, image_resized
    print(f"Loading first image: {image_path}")
    
    # Load the image (assuming 3 channels or multi-channel image)
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Failed to load image: {image_path}")
        return
    
    # Resize the image for easier display
    image_resized = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))
    
    # Convert the image to grayscale to work with intensity values across all channels
    grayscale_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)

    # Debugging information
    print(f"Grayscale image shape: {grayscale_image.shape}")
    print(f"Max pixel value in grayscale image: {np.max(grayscale_image)}")
    print(f"Min pixel value in grayscale image: {np.min(grayscale_image)}")
    
    update_image()

# Function to update the highlighted image and contours based on the threshold
def update_image():
    global grayscale_image, image_resized, threshold_value
    if grayscale_image is None or image_resized is None:
        return

    print(f"Updating image with threshold {threshold_value}...")

    # Apply thresholding to isolate bright nuclei
    _, mask = cv2.threshold(grayscale_image, threshold_value, 255, cv2.THRESH_BINARY)

    # Debug: Show number of white pixels in the mask
    print(f"Number of white pixels in mask: {np.sum(mask == 255)}")

    # Perform morphological operations to clean up the mask
    kernel = np.ones((3, 3), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours of the detected nuclei
    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    highlighted_image = image_resized.copy()

    # Draw contours on the image (green contours)
    cv2.drawContours(highlighted_image, contours, -1, (0, 255, 0), 2)  # Green contours with thickness 2

    # Count the number of contours detected
    print(f"Number of detected nuclei (contours): {len(contours)}")

    # Show the updated highlighted image with contours
    cv2.imshow('Highlighted Image', highlighted_image)

    # Call the count_cells function to count connected components (for debugging purposes)
    count_cells(mask_cleaned)

# Function to count the cells using connected component labeling
def count_cells(binary_mask):
    # Use skimage's measure.label to count connected components
    labeled_mask = measure.label(binary_mask)
    regions = measure.regionprops(labeled_mask)
    
    # Count the number of connected components (nuclei)
    total_nuclei = len(regions)
    print(f"Total nuclei counted using connected component labeling: {total_nuclei}")

# Function to analyze a single image and return results
def analyze_image(image_path):
    print(f"Analyzing image: {image_path}")
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))
    
    # Convert the resized image to grayscale
    grayscale_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    
    # Thresholding to isolate DAPI-stained nuclei
    _, mask = cv2.threshold(grayscale_image, threshold_value, 255, cv2.THRESH_BINARY)  # Adjust threshold as needed
    
    # Morphological operations to clean up noise
    kernel = np.ones((3, 3), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Connected component analysis to count nuclei
    labeled_mask = measure.label(mask_cleaned)
    regions = measure.regionprops(labeled_mask)
    total_nuclei = len(regions)

    result = {
        'Image': os.path.basename(image_path),  # Use the basename to only get the file name
        'Total Nuclei': total_nuclei
    }

    print(f"Analysis complete for image: {image_path}, Total Nuclei: {total_nuclei}")
    return result

# Function to analyze all images and save results to CSV
def analyze_all_images():
    print("Analyzing all images...")
    results = []

    for image_path in image_paths:
        result = analyze_image(image_path)
        results.append(result)

    df = pd.DataFrame(results)
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the script
    output_path = os.path.join(script_dir, 'nuclei_summary.csv')  # Define the output path in the script's directory
    df.to_csv(output_path, index=False)
    print(f"Analysis results saved to '{output_path}'")

# Create the GUI
root = Tk()
root.title("DAPI Nuclei Counter")

# Create load folder button
load_button = Button(root, text="Load Folder", command=load_folder)
load_button.pack()

# Create analyze button
analyze_button = Button(root, text="Analyze All", command=analyze_all_images)
analyze_button.pack()

# Create label for instructions
instructions = Label(root, text="Load a folder of images and click 'Analyze All' to count DAPI-stained nuclei.")
instructions.pack()

# Create threshold slider for dynamic adjustment
threshold_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Threshold", command=lambda x: adjust_threshold(x))
threshold_slider.set(threshold_value)  # Set the initial value
threshold_slider.pack()

# Adjust threshold dynamically and update the image
def adjust_threshold(value):
    global threshold_value
    threshold_value = int(value)
    update_image()

# Start the GUI
cv2.imshow('Highlighted Image', np.zeros((100, 100, 3), dtype=np.uint8))  # Show a blank image initially
root.mainloop()

cv2.destroyAllWindows()
