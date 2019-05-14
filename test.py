from cv2 import *
from Solver import sudoku


def write_on_image(grid_origin, grid_res, img):
    """This function is to write the answers back on the image"""
    font = FONT_HERSHEY_SIMPLEX
    row, col = img.shape  # the size of the image
    row_unit = row // 9  # unit length of the row
    col_unit = col // 9  # unit length of the col

    for i in range(9):
        for j in range(9):
            if grid_origin[i][j] == 0:
                pos = (20+row_unit*j, col_unit*(i+1)-15)
                putText(img, 'x', pos, font, 1, (0, 255, 0), 2, LINE_AA)
    return img


def debugimage(img, name):
    """ Shows an image for debugging. """
    namedWindow(name)  # name on the window
    imshow(name, img)
    waitKey()  # wait for a key to be pressed
    return


img_origin = imread("image.png", 0)
grid = [[0, 0, 6, 0, 5, 4, 9, 0, 0], [1, 0, 0, 0, 6, 0, 0, 4, 2], [7, 0, 0, 0, 8, 9, 0, 0, 0],
        [0, 7, 0, 0, 0, 5, 0, 8, 1], [0, 5, 0, 3, 4, 0, 6, 0, 0], [4, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 3, 4, 0, 0, 0, 1, 0, 0], [9, 0, 0, 8, 0, 0, 0, 5, 0], [0, 0, 0, 4, 0, 0, 3, 0, 7]]
# complete_sudoku = sudoku(grid)
img_res = write_on_image(grid, grid, img_origin)
debugimage(img_res, 'result')