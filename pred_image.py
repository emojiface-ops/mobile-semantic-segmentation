from __future__ import print_function

import time

import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from keras.utils import CustomObjectScope
from sklearn.model_selection import train_test_split

from data import seed, standardize
from loss import np_dice_coef
from nets.MobileUNet import custom_objects

from scipy import misc
import skimage.transform

SAVED_MODEL = 'artifacts/model_224_0.5.h5'
size = 224

def main():
    with CustomObjectScope(custom_objects()):
        model = load_model(SAVED_MODEL)

    img_in = misc.imread("data/border.jpg")

    i_width = 224
    i_height = 224

    img_resize = skimage.transform.resize(img_in, (i_width, i_height), preserve_range=True)
    img = np.copy(img_resize).astype('uint8')

    img_reshape = img.reshape(1, size, size, 3).astype(float)

    t1 = time.time()
    pred = model.predict(standardize(img_reshape)).reshape(size, size)
    elapsed = time.time() - t1
    print('elapsed1: ', elapsed)


    plt.subplot(2, 2, 1)
    plt.imshow(img)
    
    plt.subplot(2, 2, 2)
    plt.imshow(pred)
    
    plt.show()

if __name__ == '__main__':
    main()
