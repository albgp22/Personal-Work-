from imagesLoader import get_samples
import constants as C

from sklearn.utils import shuffle
from keras.utils import to_categorical
import numpy as np


def split_dataset(X, y, validation_split=C.VALIDATION_SPLIT):
    assert X.shape[0] == y.shape[0]

    X, y = shuffle(X, y, random_state=C.SEED)
    size = validation_split*X.shape[0]
    return X[size:], X[:size], y[size:], y[:size]


def load_dataset(nameX=C.NAMEX, nameY=C.NAMEY):
    return np.load(nameX), np.load(nameY)


def save_dataset(X, y, nameX=C.NAMEX, nameY=C.NAMEY):
    with open(nameX, 'wb+') as f:
        np.save(f, X)

    with open(nameY, 'wb+') as f:
        np.save(f, y)


def create_dataset(pd_folder, nd_folder, max_num_images=C.MAX_NUM_IMAGES):
    param_pd = ((pd_folder, None, max_num_images, True, False), )
    param_nd = ((nd_folder, None, max_num_images, False, False), )

    X1, y1 = get_samples(param_pd)
    X2, y2 = get_samples(param_nd)
    X = np.append(X1, X2)
    y = np.append(y1, y2)

    X = np.reshape(X, (-1, 1, 96, 96))
    return split_dataset(X, to_categorical(y, num_classes=2))




