import cv2
import numpy as np
from .normalizer import resize_and_pad


class SudokuCell:
    def __init__(self, index, img):
        self.index = index
        self.img = img


def detect_cluster(xs, window):
    xs = np.sort(xs)
    cluster = [xs[0]]
    points = []
    for i in range(0, len(xs)):
        x = xs[i]
        if abs(x - np.mean(cluster)) < window:
            cluster.append(x)
        else:
            points.append(np.mean(cluster))
            cluster = [x]
    points.append(np.mean(cluster))
    return points


def extract_cells(xs, ys):
    result = []
    for i in range(len(xs)-1):
        x1, x2 = xs[i:i+2]
        for j in range(len(ys)-1):
            y1, y2 = ys[j:j+2]
            result.append((int(x1), int(y1), int(x2), int(y2), 9*j+i))
    return result


def extract_puzzle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    xs, ys = [], []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        xs.append(x1), xs.append(x2)
        ys.append(y1), ys.append(y2)
    k = 0.1
    x_window = k * np.std(xs)
    y_window = k * np.std(ys)
    points_x = detect_cluster(xs, x_window)
    points_y = detect_cluster(ys, y_window)
    cells = extract_cells(points_x, points_y)
    if len(cells) != 81:
        raise RuntimeError(
            "Failed to detect 81 cells, found {} cells instead.".format(len(cells))
        )
    result = []
    for x1, y1, x2, y2, i in cells:
        w, h = x2 - x1, y2 - y1
        roi = gray[y1:y1+h, x1:x1+w]
        crop_size = 16
        size = 128
        roi_resized = resize_and_pad(roi, (size + 2*crop_size, size + 2*crop_size), 255)
        roi_cropped = roi_resized[crop_size:crop_size+size,crop_size:crop_size+size]
        _, roi_threshold = cv2.threshold(roi_cropped, 127, 255, cv2.THRESH_BINARY_INV)
        fp = 2
        cv2.floodFill(roi_threshold, None, (fp, fp), (0, 0, 0))
        cv2.floodFill(roi_threshold, None, (fp, size-fp), (0, 0, 0))
        cv2.floodFill(roi_threshold, None, (size-fp, fp), (0, 0, 0))
        cv2.floodFill(roi_threshold, None, (size-fp, size-fp), (0, 0, 0))
        pixel_count = cv2.countNonZero(roi_threshold)
        if pixel_count > 250:
            
            result.append(SudokuCell(i, roi_threshold))
    return result
    

