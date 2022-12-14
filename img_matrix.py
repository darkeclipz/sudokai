"""
usage: imgmatrix.py [-h] [--margin m] f w h img [img ...]

Arrange a number of images as a matrix.

positional arguments:
  f           Output filename.
  w           Width of the matrix (number of images).
  h           Height of the matrix (number of images).
  img         Images (w x h files).

optional arguments:
  -h, --help  show this help message and exit
  --margin m  Margin between images: integers are interpreted as pixels,
              floats as proportions.
"""

#! /usr/bin/env python

import argparse
import itertools

import cv2
import numpy as np

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='Arrange a number of images as a matrix.')
    parser.add_argument('f', help='Output filename.')
    parser.add_argument('w', type=int,
                        help='Width of the matrix (number of images).')
    parser.add_argument('h', type=int,
                        help='Height of the matrix (number of images).')
    parser.add_argument('img', nargs='+', help='Images (w x h files).')
    parser.add_argument('--margin', metavar='m', nargs=1,
                        help='Margin between images: integers are '
                             'interpreted as pixels, floats as proportions.')
    args = parser.parse_args()

    w = args.w
    h = args.h
    n = w*h

    if len(args.img) != n:
        raise ValueError('Number of images ({}) does not match '
                         'matrix size {}x{}'.format(w, h, len(args.img)))

    imgs = [cv2.imread(i) for i in args.img]

    if any(i.shape != imgs[0].shape for i in imgs[1:]):
        raise ValueError('Not all images have the same shape.')

    img_h, img_w, img_c = imgs[0].shape

    m_x = 0
    m_y = 0
    if args.margin is not None:
        margin = args.margin[0]
        if '.' in margin:
            m = float(margin)
            m_x = int(m*img_w)
            m_y = int(m*img_h)
        else:
            m_x = int(margin)
            m_y = m_x

    imgmatrix = np.zeros((img_h * h + m_y * (h - 1),
                          img_w * w + m_x * (w - 1),
                          img_c),
                         np.uint8)

    imgmatrix.fill(255)    

    positions = itertools.product(range(w), range(h))
    for (x_i, y_i), img in itertools.izip(positions, imgs):
        x = x_i * (img_w + m_x)
        y = y_i * (img_h + m_y)
        imgmatrix[y:y+img_h, x:x+img_w, :] = img

    cv2.imwrite(args.f, imgmatrix) 