import constants as C

from matplotlib import pyplot
from matplotlib import patches

counter = 0


def plot_rectangle(image, inner_rectangle, outer_rectangle, title=None):
    global counter

    fig, ax = pyplot.subplots(1)
    if title is not None:
        fig.suptitle(title)

    ax.imshow(image.reshape(image.shape[1:]), cmap='gray')

    rect1 = patches.Rectangle((inner_rectangle[0][1], inner_rectangle[0][0]),
                              height=inner_rectangle[1], width=inner_rectangle[2], facecolor='none', edgecolor='g')
    rect2 = patches.Rectangle((outer_rectangle[0][1], outer_rectangle[0][0]),
                              height=outer_rectangle[1], width=outer_rectangle[2], facecolor='none', edgecolor='r')
    ax.add_patch(rect1)
    ax.add_patch(rect2)

    fig.savefig('outputs/image{}.jpg'.format(counter))
    counter += 1
    pyplot.show()
    pyplot.close(fig)


def plot_image(image):
    fig, ax = pyplot.subplots(1)
    ax.imshow(C.NGRAYSCALE * image, cmap='gray')
    pyplot.show()
