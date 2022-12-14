import argparse
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

from sudokai.normalizer import normalize
from sudokai.extractor import extract_puzzle
from sudokai.classifier import classify_cells
from sudokai.solver import solve, print_grid


def cells_to_puzzle_string(cells):
    puzzle = [0] * 81
    for cell in cells:
        puzzle[cell.index] = cell.value
    return puzzle
 

def sudokai(img):
    print('Normalizing image to 512 by 512 pixels...')
    img = normalize(img)
    print('Extracting cells from image...')
    cells = extract_puzzle(img)
    print('Classifying digits...')
    classified_cells = classify_cells(cells)
    print('Solving puzzle...')
    puzzle = cells_to_puzzle_string(classified_cells)
    state, solution = solve(puzzle)
    if not state:
        print("Failed to find a solution.")
    return solution


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SudokAI')
    parser.add_argument('--image', required=True, help='Path to input image.')
    # parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
    args = parser.parse_args()

    if not os.path.exists(args.image):
        raise FileNotFoundError(args.image)

    img = cv2.imread(args.image)
    solution = sudokai(img)
    print_grid(solution)
