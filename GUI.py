from tkinter import *
from SudokuSolver import *

root = Tk()

root.title("Sudoku Solver")
root.resizable(width=FALSE, height=FALSE)
root.geometry('1000x700')


def retrieve_input():
    """This function is to get the path from a text an show the imput image"""
    global image_path
    image_path = text_1.get("1.0", "end-1c") # get the path
    if not image_path:
        label_2.config(text='Warning!\nEnter the path first\nthen click "Show the image!"', fg='red')
        return
    try:
        photo1 = PhotoImage(file=image_path)
    except:
        label_2.config(text='Warning!\nCan not find the image\nplease check the path again', fg='red')
        return
    # show the imput image
    label_photo = Label(root, image=photo1)
    label_photo.image = photo1
    label_photo.grid(row=3, column=0, padx=10)
    label_2.config(text='Click "Solve the Sudoku!" to solve', fg='black')
    return


def calculate():
    """This function is to calculate the sudoku"""
    try:
        PhotoImage(file=image_path)  # check if the path is valid
    except:
        label_2.config(text='Warning!\nCan not find the image\nplease check the path again', fg='red')
        return
    try:
        main(image_path)  # actual calculate program
    except NameError:
        label_2.config(text='Warning!\nShow the image first\nthen click "Slove the Sudoku!"', fg='red')
        return
    label_2.config(text='Completed!', fg='black')
    # show the imput image
    photo2 = PhotoImage(file=image_path[:-4]+'_res.png')
    label_photo_1 = Label(root, image=photo2)
    label_photo_1.image = photo2
    label_photo_1.grid(row=3, column=1)
    return


# label 1
label_1 = Label(root, height=3, width=35, text='Enter the path to your sudoku image >>',
                font=("Arial Bold", 20))
label_1.grid()
# text 1
text_1 = Text(root, height=1, width=50)
text_1.grid(row=0, column=1)
# button 1
button_1 = Button(root, text='  Show the image!  ', command=lambda: retrieve_input(), font=("Arial", 20))
button_1.grid(row=1, column=1, padx=20)
# label 2
label_2 = Label(root, height=3, width=35, text='Please enter the path above!',
                font=("Arial Bold", 20))
label_2.grid(row=1, column=0)
# button 2
button_1 = Button(root, text='  Solve the Sudoku!  ', command=lambda: calculate(), font=("Arial", 20))
button_1.grid(row=2, columnspan=2, pady=20)
# size the cloumn
root.grid_columnconfigure(2, minsize=600)
# main loop
root.mainloop()
