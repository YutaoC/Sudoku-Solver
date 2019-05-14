from cv2 import *
import numpy as np
import tensorflow as tf
from Solver import sudoku
import pytesseract


def debugimage(img, name):
    """ Shows an image for debugging. """
    namedWindow(name)  # name on the window
    imshow(name, img)
    waitKey()  # wait for a key to be pressed
    return


def printsudoku(board):
    """print a sudoku"""
    print("+-------+-------+-------+")
    for i in range(9):
        print("| {} {} {} | {} {} {} | {} {} {} |".format(*board[i]).replace("0", "."))
        if (i + 1) % 3 == 0:
            print("+-------+-------+-------+")


def reshape(img):
    """reshape the image into a standard square"""
    canny = Canny(img, 20, 50)  # get the edges of the image

    # debugimage(canny, "Canny")

    contours, hierarchy = findContours(canny, RETR_TREE, CHAIN_APPROX_SIMPLE)  # compute the contours

    squares = []  # store all the square contours
    for contour in contours:
        contour = approxPolyDP(contour, 0.02 * arcLength(contour, True), True)  # approximate every counter
        if len(contour) == 4 and isContourConvex(contour):  # if the contour have four point and is convex
            squares.append(contour)  # find a square contour

    square = [sorted(squares, key=lambda x: contourArea(x))[-1]]  # find the contour with maximun area
    square[0] = square[0].reshape(-1, 2)

    imgcontours = img
    drawContours(imgcontours, square, -1, (128, 128, 128), 3)  # draw the contour with maximun area

    # debugimage(imgcontours, "squares")

    # sort the points of the biggest contour in a desidered way
    point_old = sorted(square[0], key=lambda x: x[0])  # sort the points of the biggest contour according to first num
    point_old[0:2] = sorted(point_old[0:2], key=lambda x: x[1])  # sort the first two according to the second num
    point_old[2:4] = sorted(point_old[2:4], key=lambda x: x[1])  # sort the last two according to the secong num
    point_old = np.float32(point_old)  # convert it to float
    point_new = np.float32([[0, 0], [0, 450], [450, 0], [450, 450]])  # the points for a desiered standard square

    trans = getPerspectiveTransform(point_old, point_new)  # creat a transfer function
    image = warpPerspective(img, trans, (450, 450))  # reshape the image into a standard square

    # debugimage(image, "ProjectedImage")

    return image  # return the reshaped image


def get_sudoku(image):
    """get the sudoku from the image, store it in a grid"""
    row, col = image.shape  # the size of the image
    row_unit = row // 9  # unit length of the row
    col_unit = col // 9  # unit length of the col
    # model = load_model()  # load the pre-trained model
    grid = [[0 for _ in range(9)] for _ in range(9)]  # create the grid
    empty = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            crop_img = image[10+row_unit*i:row_unit*(i+1)-10, 10+col_unit*j:col_unit*(j+1)-10]  # crop for every block
            if np.amax(crop_img) - np.amin(crop_img) > 100:  # if there is a number in this block
                # grid[i][j] = read_handwritten_num(crop_img, model)  # identify the number and store it
                crop_img = resize(crop_img, (100, 100))
                grid[i][j] = read_printed_num(crop_img)
            else:
                empty[i][j] = 0
    return grid, empty


def load_model():
    """load a pre-trained model to identify the number"""
    model = tf.keras.models.load_model('num_reader.model')
    return model


def read_handwritten_num(image, model):
    """use the loaded model to identify the number"""
    test = cv2.resize(image, (28, 28))  # resize it to the desiered size
    test = np.reshape(test, [1, 784])  # reshape it into a 1-D list
    prediction = model.predict(np.array(test))  # predict the number
    return int(np.argmax(prediction))  # return the prediction result


def read_printed_num(image):
    """Thie functio is to read the number from the image"""
    # TODO
    # to improve the accuracy of the read
    img = resize(image, (28, 28))
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    res = pytesseract.image_to_string(img, config='--psm 10')
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if res not in digits:
        if len(res) > 1:
            res = res[0]
        else:
            res = my_map(res)
    return int(res)


def my_map(res):
    """This function is a temple function will be deleted later"""
    if res in ['i', 'l', 'j', 'r']:
        return '1'
    if res in ['o', 'a']:
        return '0'
    if res in ['g', 'q', 'y']:
        return '9'
    if res in ['t', 'f']:
        return '7'
    if res == 's':
        return '5'
    if res == 'b':
        return '6'
    if res == 'z':
        return '2'
    return res


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
                char = str(grid_res[i][j])
                putText(img, char, pos, font, 1, (0, 255, 0), 2, LINE_AA)
    return img


def main(filename):
    """main function"""
    img = imread(filename, 0)  # read the image
    if img is None:  # if failed
        print("Can't find the file. Please check the filename again!")

    # resize the image if the image is too large
    row, col = img.shape
    if row > col:
        coef = 800 / row
    else:
        coef = 800 / col
    if coef < 1:  # if the larger side is larger than 800
        img = resize(img, (0, 0), fx=coef, fy=coef)

    # print("[?]\tReshaping the image.....")
    img_new = reshape(img)  # reshape the image to a standard square
    # print("[?]\tFetching the Sudoku from the image.....")
    img_origin = img_new
    grid, empty_place = get_sudoku(img_new)  # get the sudoku from the image
    # print("[+]\tFetched Sudoku is as follows")
    # printsudoku(grid)  # print the completed sudoku
    # print("[?]\tCompleting the Sudoku.....")
    complete_sudoku = sudoku(grid)  # complete the sudoku
    # print("[+]\tThe completed Sudoku is as follows")
    # printsudoku(complete_sudoku)  # print the completed sudoku
    # print("[?]\tWriting the answers back to the image.....")
    img_res = write_on_image(empty_place, complete_sudoku, img_origin)
    # print("[+]\tThe completed Sudoku is shown in the image")
    imwrite(filename[:-4]+"_res.png", img_res)

