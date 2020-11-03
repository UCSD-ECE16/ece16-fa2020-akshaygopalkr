import numpy as np


def question_one(array1):
    # This subtracts each element in the numpy in the array by 20
    print(array1 - 20)
    # array1 is a vector, so the shape will be (4,)
    print(array1.shape)


def question_two(array2):
    # I first reshaped array2 into an array with four rows and
    # two columns
    array2_new = array2.reshape(4, 2)
    # Then I used slicing to get the 1st and 2nd row of this reshaped array
    array2_new = array2_new[1:3][:]
    print(array2_new)


def question_three(array1):
    # first horizontally stack the arrays with the each other
    array3 = np.hstack((array1, array1))
    # now we can vertically stack each row for times to get the new array
    array3 = np.vstack((array3, array3, array3, array3))
    print(array3)


def question_four():
    # make an array from -3 to 21 (not included) with step size of 6
    array_41 = np.arange(-3, 21, 6)
    print(array_41)
    # make an array from -7 to -21 with a step size of -2
    array_42 = np.arange(-7, -21, -2)
    print(array_42)


def question_five():
    # This will create an array with 49 evenly
    # spaced numbers from 0 to 100
    array5 = np.linspace(0, 100, 49, True)
    print("Array 5: ", array5)


def question_six():
    # based on all the print statements, this array should have a size of 3x4
    array6 = np.zeros((3, 4))
    # Sets the first row of the numpy array
    array6[0, :] = [12, 3, 1, 2]
    # Only need to modify two elements in this row since the other columns are left as zero
    array6[1, 2:] = [1, 2]
    array6[2, :] = [4, 2, 3, 1]
    print(array6)


def question_seven(string7):
    # split the string separated by each comma
    str_arr = string7.split(",")
    # convert each character in the string to an array
    int_np_row = np.array([int(num) for num in str_arr])
    # this will be the np array that we will perform vertical
    # stacks on
    int_np_arr = np.array(int_np_row)
    for i in range(99):
        # vertically stack one row onto the np array
        int_np_arr = np.vstack((int_np_arr, int_np_row))
    # the shape should be 100x4
    print(int_np_arr.shape)


array1 = np.array([0, 10, 4, 12])
question_one(array1)

array2 = np.array([[0, 10, 4, 12], [1, 20, 3, 41]])
question_two(array2)

question_three(array1)

question_four()

question_five()

question_six()

question_seven("1,2,3,4")

arr = [1,2,3,4]
arr_2 = [-1,-2,-3,-4]
arr_3 = [1,2,3,4]
print(np.linalg.norm([arr,arr_2,arr_3]))
print(np.linalg.norm(arr, ord=1))

