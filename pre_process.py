import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

directory_in_str = '../ImagesMasks/'

pathlist = Path(directory_in_str).glob('*.png')

for path in pathlist:

    filename = str(path)
    print(filename)

    img_in = cv2.imread(filename,0)

    ret,img_out = cv2.threshold(img_in, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    backtorgb = cv2.cvtColor(img_out,cv2.COLOR_GRAY2RGB)

    backtorgb[np.where((backtorgb == [0,0,0]).all(axis = 2))] = [0,0,255]
    backtorgb[np.where((backtorgb == [255,255,255]).all(axis = 2))] = [255,0,0]

    out_filename = Path(filename).stem + ".ppm"
    cv2.imwrite(out_filename,backtorgb)
