import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

def plot_mataches(x,y):

    plt.title("Noise L2-norm")
    plt.xlabel("Threshold")
    plt.ylabel("Number of Matches")
    plt.plot(x, y, "bo")
    plt.show()

    return 0

if __name__ == "__main__":

    threshold = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    L1 = [0, 0, 13, 42, 102, 192, 301, 448]
    L2 = [0, 0, 12, 41, 96, 179, 294, 440]
    L3 = [0, 0, 11, 38, 85, 165, 280, 431]

    noise_L2 = [0, 0, 1, 13, 37, 81, 153, 271]
    color_L2 = [5, 10, 21, 23, 28, 29, 34, 41]

    # plot_mataches(threshold, L1)
    # plot_mataches(threshold, L2)
    # plot_mataches(threshold, L3)

    # plot_mataches(threshold, color_L2)
    plot_mataches(threshold, noise_L2)
