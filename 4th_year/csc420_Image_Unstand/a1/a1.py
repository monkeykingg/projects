import numpy as np
import cv2
import math

def MyCorrelation(gray_image, filter, mode):
    filter_rows = filter.shape[0]
    filter_cols = filter.shape[1]
    gray_image_rows = gray_image.shape[0]
    gray_image_cols = gray_image.shape[1]
    half_rows = filter_rows // 2
    half_cols = filter_cols // 2
    # same_pad_image = np.pad(gray_image, half_rows, "constant")
    # full_pad_image = np.pad(gray_image, filter_rows - 1, "constant")

    pad_rows = filter_rows - 1
    pad_cols = filter_rows - 1
    rows_center = int(pad_rows / 2)
    cols_center = int(pad_cols / 2)
    rows_offset = 2 * rows_center
    cols_offset = 2 * cols_center

    same_pad_image = np.zeros(shape=(gray_image_rows + pad_rows, gray_image_cols + pad_cols))
    same_pad_image[rows_center:rows_center + gray_image_rows, cols_center:cols_center + gray_image_cols] = gray_image[0:gray_image_rows,
                                                                               0:gray_image_cols]
    full_pad_image = np.zeros(shape=(gray_image_rows + pad_rows * 2, gray_image_cols + pad_cols * 2))
    full_pad_image[rows_offset: rows_offset + gray_image_rows, cols_offset: cols_offset + gray_image_cols] = gray_image[0:gray_image_cols,
                                                                                 0:gray_image_cols]
    result = []

    if (mode == "same"):

        rows = gray_image_rows
        cols = gray_image_cols

        for m in range(rows):
            temp = []
            for n in range(cols):
                sum = 0
                for p in range(filter_rows):
                    for q in range(filter_cols):
                        sum = sum + filter[p][q] * same_pad_image[m : m+filter_rows, n : n+filter_cols][p][q]
                temp.append(sum)
            result.append(temp)

        output = np.array(result)

    elif (mode == "valid"):

        rows = gray_image_rows - half_rows * 2
        cols = gray_image_cols - half_cols * 2

        for m in range(rows):
            temp = []
            for n in range(cols):
                sum = 0
                for p in range(filter_rows):
                    for q in range(filter_cols):
                        sum = sum + filter[p][q] * gray_image[m : m+filter_rows, n : n+filter_cols][p][q]
                temp.append(sum)
            result.append(temp)

        output = np.array(result)

    elif (mode == "full"):

        rows = gray_image_rows + pad_rows * 2 - half_rows * 2
        cols = gray_image_cols + pad_cols * 2 - half_cols * 2

        for m in range(rows):
            temp = []
            for n in range(cols):
                sum = 0
                for p in range(filter_rows):
                    for q in range(filter_cols):
                        sum = sum + filter[p][q] * full_pad_image[m : m+filter_rows, n : n+filter_cols][p][q]
                temp.append(sum)
            result.append(temp)

        output = np.array(result)

    else:
        output = "Invalid Mode"

    return output


def MyConvolution(gray_image, filter, mode):
    flipped_filter = np.flip(np.flip(filter, axis=0), axis=1)
    return MyCorrelation(gray_image, flipped_filter, mode)

def GaussianPortrait(image, mask):

    blur = cv2.GaussianBlur(image, (15, 15), 15)

    # mask for highlight the background, reversed mask for highlight the person
    reversed_mask = 255 - mask

    new_mask = mask / 255
    new_reversed_mask = reversed_mask / 255

    result = image * new_reversed_mask + blur * new_mask

    return result

def MyPortrait(image, mask):

    blur = MyFilter(image, 9, 15, 15, "same")

    # mask for highlight the background, reversed mask for highlight the person
    reversed_mask = 255 - mask

    new_mask = mask / 255
    new_reversed_mask = reversed_mask / 255

    result = image * new_reversed_mask + blur * new_mask

    return result


def isSeparableFilter(filter):

    if np.linalg.matrix_rank(filter) != 1:
        print("This filter is not separable")
        print("===================================================================")
        return 0

    else:
        print("This filter is separable.")

        result = np.linalg.svd(filter)
        theta = result[1][0]
        theta_sqrt = math.sqrt(theta)
        u = (result[0].T)[0]
        v = (result[2][0] * -1)

        print("The vertical filter is")
        print(theta_sqrt * u * (-1.0))
        print("The horizontal filter is")
        print(theta_sqrt * v)
        print("===================================================================")
        return 1

def AddRandNoise(gray_image, magnitude):
    random_noise = np.random.uniform(low=-magnitude, high=magnitude, size=(gray_image.shape[0], gray_image.shape[1]))
    noisy_image = gray_image + random_noise
    return noisy_image * 255

def MyFilter(image, filter_size, sigma_x, sigma_y, mode):
    # kernel = cv2.getGaussianKernel(15, 9)
    # mode = "same"
    # blur = MyConvolution(image, kernel, mode)

    kernel_x_array = np.fromfunction(lambda x: math.e ** ((-1 * (x - (filter_size - 1) / 2) ** 2) / (2 * sigma_x ** 2)), (filter_size,))
    normalized_kernel_x = kernel_x_array / np.sum(kernel_x_array)
    kernel_x = np.reshape(normalized_kernel_x, newshape=(len(normalized_kernel_x), 1))

    kernel_y_array = np.fromfunction(lambda x: math.e ** ((-1 * (x - (filter_size - 1) / 2) ** 2) / (2 * sigma_y ** 2)),
                                     (filter_size,))
    normalized_kernel_y = kernel_y_array / np.sum(kernel_y_array)
    kernel_y = np.reshape(normalized_kernel_y, newshape=(len(normalized_kernel_y), 1))

    gaussian_filter = np.multiply(kernel_x, np.transpose(kernel_y))

    blur = MyConvolution(image, gaussian_filter, mode)

    return blur

def GaussianfFilter(image):
    blur = cv2.GaussianBlur(image, (5, 5), 1)
    return blur

def MedianFilter(image):
    blur = cv2.medianBlur(image, 5)
    return blur

def BilateralFilter(image):
    blur = cv2.bilateralFilter(image, 9, 75, 75)
    return blur

def AverageFilter(image):
    blur = cv2.blur(image,(3,3))
    return blur

def DenoiseColor(image):
    blur = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    return blur

def AddSaltAndPepperNoise(image, density):

    # gray image
    if len(image.shape) != 3:

        gray_image_rows = image.shape[0]
        gray_image_cols = image.shape[1]
        output = np.zeros(image.shape, np.uint8)

        # density = 0.05, threshold = 0.025 or 0.975
        lower_threshold = density / 2
        upper_threshold = 1 - density / 2

        for i in range(gray_image_rows):
            for j in range(gray_image_cols):
                random = np.random.rand()
                if random < lower_threshold:
                    output[i][j] = 0
                elif random > upper_threshold:
                    output[i][j] = 255
                else:
                    output[i][j] = image[i][j]
        return output

        # color image
    else:

        color_image_rows = image.shape[0]
        color_image_cols = image.shape[1]
        dim = image.shape[2]
        output = np.zeros(image.shape, np.uint8)

        # density = 0.05, threshold = 0.025 or 0.975
        lower_threshold = density / 2
        upper_threshold = 1 - density / 2

        for i in range(color_image_rows):
            for j in range(color_image_cols):
                for k in range(dim):
                    random = np.random.rand()
                    if random < lower_threshold:
                        output[i][j][k] = 0
                    elif random > upper_threshold:
                        output[i][j][k] = 255
                    else:
                        output[i][j][k] = image[i][j][k]
        return output

if __name__ == "__main__":

    img = cv2.imread("./gray.jpg", cv2.IMREAD_GRAYSCALE)
    img_color = cv2.imread("./color.jpg")

    img_origin = cv2.imread("./origin.jpg")
    img_origin_gray = cv2.imread("./origin.jpg", cv2.IMREAD_GRAYSCALE)
    img_mask = cv2.imread("./mask.jpg", cv2.IMREAD_GRAYSCALE)

    filter_0 = np.array([[0]])

    filter_1 = np.array([[0, 0, 0],
                         [0, 1, 0],
                         [0, 0, 0]])

    filter_2 = np.array([[0, 0, 0],
                         [0, 0, 1],
                         [0, 0, 0]])

    filter_3 = np.array([[1, 1, 1],
                         [1, 1, 1],
                         [1, 1, 1]])

    filter_4 = np.array([[-1, -1, -1],
                         [-1, 4, -1],
                         [-1, -1, -1]])

    filter_5 = np.array([[-1, -1, -1],
                         [0, 0, 0],
                         [1, 1, 1]])

    filter_6 = np.array([[1, 2, 1],
                         [2, 4, 2],
                         [1, 2, 1]])

    filter_7 = np.array([[0.1, 0.1, 0.1],
                         [0.1, 0.1, 0.1],
                         [0.1, 0.1, 0.1]])

    filter = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ])

    # result1 = MyCorrelation(img, filter_1, "full")
    # cv2.imwrite("./result1.jpg", result1)
    #
    # result2 = MyCorrelation(img, filter_1, "same")
    # cv2.imwrite("./result2.jpg", result2)
    #
    # result3 = MyCorrelation(img, filter_1, "valid")
    # cv2.imwrite("./result3.jpg", result3)
    #
    # result4 = MyConvolution(img, filter_1, "full")
    # cv2.imwrite("./result4.jpg", result4)
    #
    # result5 = MyConvolution(img, filter_1, "same")
    # cv2.imwrite("./result5.jpg", result5)
    #
    # result6 = MyConvolution(img, filter_1, "valid")
    # cv2.imwrite("./result6.jpg", result6)

    cv2.imwrite("./origin_gray.jpg", img_origin_gray)

    portrait_gaussian = GaussianPortrait(img_origin_gray, img_mask)
    cv2.imwrite("./portrait_Gaussian.jpg", portrait_gaussian)

    # portrait_myfilter = MyPortrait(img_origin_gray, img_mask)
    # cv2.imwrite("./portrait_myfilter.jpg", portrait_myfilter)

    isSeparableFilter(filter_0)
    isSeparableFilter(filter_1)
    isSeparableFilter(filter_3)

    temp = img/255

    noise = AddRandNoise(temp, 0.05)
    cv2.imwrite("./noise.jpg", noise)

    blur = GaussianfFilter(noise)
    cv2.imwrite('./blur.jpg', blur)


    gray_salt_papper = AddSaltAndPepperNoise(img, 0.05)
    cv2.imwrite('./gray_salt_papper.jpg', gray_salt_papper)

    gray_salt_papper_blur_Gaussian = GaussianfFilter(gray_salt_papper)
    cv2.imwrite('./gray_salt_papper_blur_Gaussian.jpg', gray_salt_papper_blur_Gaussian)

    gray_salt_papper_blur_Median = MedianFilter(gray_salt_papper)
    cv2.imwrite('./gray_salt_papper_blur_Median.jpg', gray_salt_papper_blur_Median)


    color_salt_papper = AddSaltAndPepperNoise(img_color, 0.05)
    cv2.imwrite('./color_salt_papper.jpg', color_salt_papper)

    color_salt_papper_blur_Median = MedianFilter(color_salt_papper)
    cv2.imwrite('./color_salt_papper_blur_Median.jpg', color_salt_papper_blur_Median)

    color_salt_papper_blur_Gaussian = GaussianfFilter(color_salt_papper)
    cv2.imwrite('./color_salt_papper_blur_Gaussian.jpg', color_salt_papper_blur_Gaussian)

    color_salt_papper_blur_Median_Average = AverageFilter(color_salt_papper_blur_Median)
    cv2.imwrite('./color_salt_papper_blur_Median_Average.jpg', color_salt_papper_blur_Median_Average)

    color_salt_papper_denoise = DenoiseColor(color_salt_papper)
    cv2.imwrite('./color_salt_papper_denoise.jpg', color_salt_papper_denoise)

    hsv = cv2.cvtColor(color_salt_papper, cv2.COLOR_BGR2HSV)
    temp = MedianFilter(hsv)
    color_salt_papper_blur_Median_hsv = cv2.cvtColor(temp, cv2.COLOR_HSV2BGR)
    cv2.imwrite('./color_salt_papper_blur_Median_hsv.jpg', color_salt_papper_blur_Median_hsv)

    threshold = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    L1 = [0, 0, 13, 42, 102, 192, 301, 448]
    L2 = [0, 0, 12, 41, 96, 179, 294, 440]
    L3 = [0, 0, 11, 38, 85, 165, 280, 431]

    noise_L2 = [0, 0, 1, 13, 37, 81, 153, 271]

    color_L2 = [5, 10, 21, 23, 28, 29, 34, 41]

