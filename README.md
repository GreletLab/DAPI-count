
# DAPI Cell Counting and Invasion Analysis Tool

## Overview
This tool automates the analysis of microscopy images of DAPI-stained cells on Boyden chamber membranes. 

## System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python Version**: Python 3.8 or higher
- **Required Libraries**:
  - OpenCV (`cv2`)
  - NumPy
  - scikit-image (`skimage`)
  - Matplotlib
  - Pandas
  - Tkinter (built-in with Python for most OS)

Ensure all dependencies are installed using the `requirements.txt` file (see below).

## Installation Guide
1. Clone the repository:
   ```bash
   git clone https://github.com/GreletLab/DAPI-cell-analysis.git
   cd DAPI-cell-analysis
   ```
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use
1. **Load Images**:
   - Run the script using Python:
     ```bash
     python DAPI_counting_v1.py
     ```
   - Use the GUI to select the folder containing microscopy images.

2. **Adjust Threshold**:
   - Use the slider in the GUI to adjust the threshold value for cell detection.

3. **Analyze Images**:
   - The script processes each image, identifies cells based on DAPI staining, and counts the number of cells per field.

4. **Export Results**:
   - The output is saved as a CSV file containing cell counts and additional metrics for each analyzed image.

## Input and Output
- **Input**: A folder of microscopy images (supported formats: `.png`, `.jpg`, `.tiff`).
- **Output**: A CSV file summarizing the number of cells per image and their invasion metrics.

## Example
1. Place your images in a folder, e.g., `./images/`.
2. Run the script and select the folder through the GUI.
3. Adjust the threshold to match the staining intensity.
4. View the results in the exported CSV file, e.g., `results.csv`.

## Typical Run Time
- **Per Image**: Less than 5 seconds, depending on image resolution.
- **Batch Processing**: Time scales linearly with the number of images.


