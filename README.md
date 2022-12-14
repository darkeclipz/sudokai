# Sudokai

This app is solved Sudoku puzzles using an image as input.
It uses OpenCV and a neural network to extract the data of an image, and then solves it.

## Steps

 1. Normalize the image to 512 by 512 pixels.
 2. Detect lines in the image with `cv.HoughLinesP`.
 3. Create a histogram of the x and y points.
 4. Cluster the points to find the 10 points that define the grid (in both directions).
 5. Use the clustered points to generate the lines of the grid.
 6. Extract each individual cell.
 7. Detect if there is something in the cell.
 8. Classify the cell if there is something in it.
 9. Create a Sudoku puzzle.
 10. Solve the puzzle.
 11. Print the solution.

## Usage

```bash
python main.py --image dataset/10.png
```