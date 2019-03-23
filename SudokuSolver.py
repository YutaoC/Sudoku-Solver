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

    squares = [sorted(squares, key=lambda x: contourArea(x))[-1]]  # find the contour with maximun area
    squares[0] = squares[0].reshape(-1, 2)

    imgcontours = img
    drawContours(imgcontours, squares, -1, (255, 0, 0), 3)  # draw the contour with maximun area

    # debugimage(imgcontours, "squares")

    # sort the points of the biggest contour in a desidered way
    point_old = sorted(squares[0], key=lambda x: x[0])  # sort the points of the biggest contour according to first num
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
    for i in range(9):
        for j in range(9):
            crop_img = image[8+row_unit*i:row_unit*(i+1)-8, 8+col_unit*j:col_unit*(j+1)-8]  # crop for every block
            if np.amax(crop_img) - np.amin(crop_img) > 100:  # if there is a number in this block
                # grid[i][j] = read_handwritten_num(crop_img, model)  # identify the number and store it
                grid[i][j] = read_printed_num(crop_img)
    return grid


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
    img = resize(image, (28, 28))
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    res = pytesseract.image_to_string(img, config='--psm 8')
    return res


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

    print("Reshaping the image.....")
    img_new = reshape(img)  # reshape the image to a standard square
    print("Fetching the Sudoku from the image.....")
    grid = get_sudoku(img_new)  # get the sudoku from the image
    print("Fetched Sudoku is as follows")
    printsudoku(grid)  # print the completed sudoku
    print("Completing the Sudoku.....")
    complete_sudoku = sudoku(grid)  # complete the sudoku
    print("The completed Sudoku is as follows")
    printsudoku(complete_sudoku)  # print the completed sudoku


main("SudokuSample2.png")
