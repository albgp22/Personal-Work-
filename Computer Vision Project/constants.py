# Random seed used along the program execution
SEED = 7

# Image settings
IMG_DIMS = (96, 96)
NGRAYSCALE = 256

# Model variables
LEARNING_RATE_INITIAL = 0.03
LEARNING_RATE_FINAL = 0.001

CONV2D_FIRST_NUMFILTERS = 32
CONV2D_SECOND_NUMFILTERS = 64
CONV2D_THIRD_NUMFILTERS = 128

CONV2D_FIRST_KERNEL = (3, 3)
CONV2D_SECOND_KERNEL = (3, 3)
CONV2D_THIRD_KERNEL = (2, 2)

CONV2D_FIRST_ACTIVATION = 'relu'
CONV2D_SECOND_ACTIVATION = 'relu'
CONV2D_THIRD_ACTIVATION = 'relu'

DROPOUT_FIRST = 0.1
DROPOUT_SECOND = 0.2
DROPOUT_THIRD = 0.2

DENSE_NODES = 600
DENSE_ACTIVATION = 'relu'

SGD_MOMENTUM = 0.9
SGD_NESTEROV = True

# Training parameters
MAX_NUM_IMAGES = 50000

IMAGE_GENERATOR_FLIP = True
IMAGE_GENERATOR_ROTATION = 50
EARLY_STOPPING_PATIENCE = 1

BATCH_SIZE = 150
MAX_EPOCHS = 15
VALIDATION_SPLIT = 0.1

# FaceDetector settings
WIDTH_ANGLE = 90
HEIGHT_ANGLE = 90
NUM_LINES = 5
# INITIALIZE_SETTINGS = (
#     ((1., 1.), (0.1, 0.1)),
#     ((0.9, 0.9), (0.05, 0.05)),
#     ((0.8, 0.8), (0.10, 0.10)),
#     ((0.7, 0.7), (0.15, 0.15)),
#     ((0.6, 0.6), (0.15, 0.15)),
#     #((0.5, 0.5), (0.20, 0.20)),
#     #((0.4, 0.4), (0.35, 0.35)),
#     #((0.3, 0.3), (0.35, 0.35))
# )
# INITIALIZE_SETTINGS = (
#     (1., 0.1),
#     (0.9, 0.1),
#     (0.8, 0.2),
#     (0.7, 0.25),
#     (0.6, 0.25),
# )

# FASTER AND BETTER
DETECT_SETTINGS = (
    (1., 0.1),
    (0.8, 0.25),
    (0.6, 0.45),
)

VELOCITY_MOMENTUM = 0.3
MINIMUM_DEFORMATION = 0.1
STOP_RATIO_THRESHOLD = 0.85
IS_FACE_THRESHOLD = 0.9
RECTANGLE_LOWER_BOUND_THRESHOLD = IMG_DIMS
FACE_WIDTH_WRT_HEIGHT_RATIO = 0.65
FACE_LOST_TRACK_EPSILON = 0.15
MAX_DETECT_ITERATIONS = 50

# Cam settings
CAM_FPS = 20

# Filenames
MODEL_FILE = 'neural_network.h5'
LOGDIR = 'logs'

NAMEX = 'X.data'
NAMEY = 'y.data'



# Variables for the csv dataset
#TRAINING_FACES_FILEPATH = 'training_faces.csv'
#TEST_FACES_FILEPATH = 'test_faces.csv'
#COLS = ('left_eye_center_x', 'left_eye_center_y', 'right_eye_center_x', 'right_eye_center_y', 'nose_tip_x',
#        'nose_tip_y', 'mouth_center_bottom_lip_x', 'mouth_center_bottom_lip_y') # ~7000 entries
