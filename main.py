from functions import *
from PIL.Image import open
from sys import argv


def search(place):
    points = get_points(place)
    content = get_image(get_place_info(place), points)
    open(content).show()


if __name__ == "__main__":
    place = " ".join(argv[1:])
    search(place)
