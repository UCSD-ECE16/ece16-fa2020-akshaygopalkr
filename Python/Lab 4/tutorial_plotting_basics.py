import matplotlib.pyplot as plt
import numpy as np
'''
Part 1
'''
def part_one():
    x = [1,2,3,4] # x data vector (as a list)
    y = [1,4,9,16] # y data vector (as a list)
    plt.clf() # clear any existing plot
    plt.plot(x,y) # write the data onto the figure buffer
    plt.show() # show the figure

'''
Part 2
'''
def part_two():
    # This plots the same information as the last plot. This means
    # that mat plot lib treats the first row as x and the second row as y
    # for a 2xn array
    a = np.array([[1,2,3,4],[1,4,9,16]])
    plt.clf()
    plt.plot(x,y)
    plt.show()

'''
Part 3
'''
def part_three():
    a = np.array([[1, 2, 3, 4], [1, 4, 9, 16]])
    x = a[0, :]  # index from a to get [1,2,3,4]
    y = a[1, :]  # index from a to get [1,4,9,16]
    plt.title("First plot!")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(x, x)
    plt.plot(x, y)
    plt.show()

'''
Part 4
'''
def part_four():
    plt.clf()
    plt.subplot(211)
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.subplot(212)
    plt.plot([1, 2, 3, 4], [4, 2, 1, 6])
    plt.show()

part_four()
