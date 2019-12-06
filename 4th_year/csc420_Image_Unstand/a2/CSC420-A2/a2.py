import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
from scipy import ndimage as nd
from matplotlib.patches import ConnectionPatch
import heapq

def OneDimLinearInterpolation(image, d, direction):

    image_rows = image.shape[0]
    image_cols = image.shape[1]

    temp_image = np.zeros(shape=(image_rows, image_cols*d, 3))

    rows = temp_image.shape[0]
    cols = temp_image.shape[1]

    result = []

    if direction == 0:

        for m in range(rows):
            temp = []
            for n in range(cols):
                i = n/d
                if i.is_integer():
                    output = image[m, int(i)]
                else:
                    x = i
                    x_1 = math.floor(x)
                    x_2 = math.ceil(x)
                    if x_2 == image_cols:
                        break
                    else:
                        r_1 = (x_2 - x) / (x_2 - x_1)
                        r_2 = (x - x_1) / (x_2 - x_1)
                        output = r_1 * image[m, x_1] + r_2 * image[m, x_2]
                temp.append(output)
            result.append(temp)

    output_image = np.array(result)

    if direction == 1:

        rotated_image = np.rot90(image, -1)
        temp_result = OneDimLinearInterpolation(rotated_image, d, 0)
        output_image = np.rot90(temp_result, 1)

    return output_image


def TwoDimLinearInterpolation(image, d):

    image_rows = image.shape[0]
    image_cols = image.shape[1]

    temp_image = np.zeros(shape=((image_rows - 1) * d + 1, (image_cols - 1) * d + 1, 3))

    temp_image[::d, ::d] = image.copy()

    one_d_filter = []
    for i in range(d):
        one_d_filter.append(i/d)
    for i in range(d, -1, -1):
        one_d_filter.append(i/d)

    one_d_filter = np.array(one_d_filter)

    two_d_filter = np.matmul(np.transpose(np.array([one_d_filter])), np.array([one_d_filter]))
    print(two_d_filter)

    result = cv2.filter2D(temp_image,-1,two_d_filter)

    return result

def harris(image, alpha, threshold, radius):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 7)
    ddepth = cv2.CV_64F

    # STEP1: Compute gradient Ix and Iy
    Ix = cv2.Sobel(src=blur, ddepth=ddepth, dx=1, dy=0, ksize=5)
    Iy = cv2.Sobel(src=blur, ddepth=ddepth, dx=0, dy=1, ksize=5)

    # STEP2: Compute Ix^2, Iy^2 and Ix*Iy
    IxIy = np.multiply(Ix, Iy)
    Ix2 = np.multiply(Ix, Ix)
    Iy2 = np.multiply(Iy, Iy)

    # STEP3: Average(Gaussian)
    Ix2_blur = cv2.GaussianBlur(Ix2, (7, 7), 10)
    Iy2_blur = cv2.GaussianBlur(Iy2, (7, 7), 10)
    IxIy_blur = cv2.GaussianBlur(IxIy, (7, 7), 10)

    # STEP4: Compute R
    det = np.multiply(Ix2_blur, Iy2_blur) - np.multiply(IxIy_blur, IxIy_blur)
    trace = Ix2_blur + Iy2_blur
    R = det - alpha * np.multiply(trace, trace)

    # plt.subplot(1, 2, 1), plt.imshow(image), plt.axis('off')
    # plt.subplot(1, 2, 2), plt.imshow(R, cmap='gray'), plt.axis('off')
    # plt.imshow(R, cmap="gray")
    # plt.show()

    #R = R * (R > (threshold * R.max())) * (R > 0)
    R[R < threshold] = 0

    plt.subplot(1, 2, 1), plt.imshow(image), plt.axis('off'), plt.show()
    plt.subplot(1, 2, 2), plt.imshow(R, cmap='gray'), plt.axis('off'), plt.show()
    plt.imshow(R, cmap="gray")
    plt.show()

    # result = non_max_suppress(R, radius)
    # plt.imshow(result, cmap="gray")
    # plt.show()

    return 0

def harris2(image, alpha, threshold):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 7)
    ddepth = cv2.CV_64F

    # STEP1: Compute gradient Ix and Iy
    Ix = cv2.Sobel(src=blur, ddepth=ddepth, dx=1, dy=0, ksize=5)
    Iy = cv2.Sobel(src=blur, ddepth=ddepth, dx=0, dy=1, ksize=5)

    # STEP2: Compute Ix^2, Iy^2 and Ix*Iy
    IxIy = np.multiply(Ix, Iy)
    Ix2 = np.multiply(Ix, Ix)
    Iy2 = np.multiply(Iy, Iy)

    # STEP3: Average(Gaussian)
    Ix2_blur = cv2.GaussianBlur(Ix2, (7, 7), 10)
    Iy2_blur = cv2.GaussianBlur(Iy2, (7, 7), 10)
    IxIy_blur = cv2.GaussianBlur(IxIy, (7, 7), 10)

    matrix = np.zeros((Ix2_blur.shape[0], Ix2_blur.shape[1], 2, 2))
    matrix[:, :, 0, 0] = Ix2_blur
    matrix[:, :, 0, 1] = IxIy_blur
    matrix[:, :, 1, 0] = IxIy_blur
    matrix[:, :, 1, 1] = Iy2_blur

    lambda_result = np.linalg.eigvals(matrix)
    lambda_0 = lambda_result[:, :, 0]
    lambda_1 = lambda_result[:, :, 1]

    # STEP4: Compute R
    R = lambda_0 * lambda_1 - alpha * (lambda_0 + lambda_1) ** 2
    R[R < threshold] = 0

    plt.subplot(1, 2, 1), plt.imshow(image), plt.axis('off'), plt.show()
    plt.subplot(1, 2, 2), plt.imshow(R, cmap='gray'), plt.axis('off'), plt.show()

    plt.imshow(R, cmap="gray")
    plt.show()

    return 0

def brown(image, radius):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 7)
    ddepth = cv2.CV_64F

    # STEP1: Compute gradient Ix and Iy
    Ix = cv2.Sobel(src=blur, ddepth=ddepth, dx=1, dy=0, ksize=5)
    Iy = cv2.Sobel(src=blur, ddepth=ddepth, dx=0, dy=1, ksize=5)

    # STEP2: Compute Ix^2, Iy^2 and Ix*Iy
    IxIy = np.multiply(Ix, Iy)
    Ix2 = np.multiply(Ix, Ix)
    Iy2 = np.multiply(Iy, Iy)

    # STEP3: Average(Gaussian)
    Ix2_blur = cv2.GaussianBlur(Ix2, (7, 7), 10)
    Iy2_blur = cv2.GaussianBlur(Iy2, (7, 7), 10)
    IxIy_blur = cv2.GaussianBlur(IxIy, (7, 7), 10)

    # STEP4: Compute R
    det = np.multiply(Ix2_blur, Iy2_blur) - np.multiply(IxIy_blur, IxIy_blur)
    trace = Ix2_blur + Iy2_blur
    R = np.divide(det, trace+0.01)

    plt.subplot(1, 2, 1), plt.imshow(image), plt.axis('off'), plt.show()
    plt.subplot(1, 2, 2), plt.imshow(R, cmap='gray'), plt.axis('off'), plt.show()
    plt.imshow(R, cmap="gray")
    plt.show()

    # result = non_max_suppress(R, radius)
    # plt.imshow(result, cmap="gray")
    # plt.show()

    return 0


def brown2(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 7)
    ddepth = cv2.CV_64F

    # STEP1: Compute gradient Ix and Iy
    Ix = cv2.Sobel(src=blur, ddepth=ddepth, dx=1, dy=0, ksize=5)
    Iy = cv2.Sobel(src=blur, ddepth=ddepth, dx=0, dy=1, ksize=5)

    # STEP2: Compute Ix^2, Iy^2 and Ix*Iy
    IxIy = np.multiply(Ix, Iy)
    Ix2 = np.multiply(Ix, Ix)
    Iy2 = np.multiply(Iy, Iy)

    # STEP3: Average(Gaussian)
    Ix2_blur = cv2.GaussianBlur(Ix2, (7, 7), 10)
    Iy2_blur = cv2.GaussianBlur(Iy2, (7, 7), 10)
    IxIy_blur = cv2.GaussianBlur(IxIy, (7, 7), 10)

    matrix = np.zeros((Ix2_blur.shape[0], Ix2_blur.shape[1], 2, 2))
    matrix[:, :, 0, 0] = Ix2_blur
    matrix[:, :, 0, 1] = IxIy_blur
    matrix[:, :, 1, 0] = IxIy_blur
    matrix[:, :, 1, 1] = Iy2_blur

    lambda_result = np.linalg.eigvals(matrix)
    lambda_0 = lambda_result[:, :, 0]
    lambda_1 = lambda_result[:, :, 1]

    # STEP4: Compute R
    R = np.divide(lambda_0 * lambda_1 , (lambda_0 + lambda_1)+0.01)

    plt.subplot(1, 2, 1), plt.imshow(image), plt.axis('off'), plt.show()
    plt.subplot(1, 2, 2), plt.imshow(R, cmap='gray'), plt.axis('off'), plt.show()

    plt.imshow(R, cmap="gray")
    plt.show()

    return 0

# def non_max_suppress(R, radius):
#     filter_size = radius * 2 + 1
#     img_m = R.shape[0]
#     img_n = R.shape[1]
#     c_p = int((filter_size - 1) / 2.0)  # center point of the filter
#
#     offset = c_p * 2
#     # output matrix is same size as image
#     output_matrix = np.zeros(shape=(img_m, img_n))
#     # temp matrix is larger than image
#     cal_matrix = np.zeros(shape=(img_m + offset, img_n + offset))
#     # copy image content to temp matrix
#     cal_matrix[c_p:c_p + img_m, c_p:c_p + img_n] = R[0:img_m, 0:img_n]
#
#     # Non Maximal Suppression
#     rows = output_matrix.shape[0]
#     cols = output_matrix.shape[1]
#
#     for m in range(rows):
#         for n in range(cols):
#             # current calculating matrix
#             current_mtx = np.array(cal_matrix[m:m + filter_size, n:n + filter_size])
#             # transform to circular kernel
#             current_mtx = circular_filter(current_mtx, radius)
#             max_tuple = np.unravel_index(np.argmax(current_mtx), current_mtx.shape)
#             if max_tuple == (c_p, c_p):
#                 output_matrix[m, n] = current_mtx[c_p, c_p]
#             else:
#                 output_matrix[m, n] = 0
#
#     return output_matrix
#
# def circular_filter(patch, r):
#     for i in range(patch.shape[0]):
#         for j in range(patch.shape[1]):
#             # set outside of circle index as zero
#             if np.sqrt(np.square(i - r) + np.square(j - r)) > r:
#                 patch[i,j] = 0
#     return patch


def LOG(image, levels, initial_sigma, scale, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float)

    n = image.shape[0]
    m = image.shape[1]
    offset = 2
    sigma = initial_sigma
    sigma_list = [0]
    increment = 1
    pyramid = np.empty((levels + offset, n, m))

    for level in range(levels):
        new_level = nd.gaussian_laplace(gray, sigma * increment)
        pyramid[level + 1] = new_level
        increment = increment * scale
        sigma_list.append(sigma * increment)

    max_list = []
    for level in range(1, levels):
        # Construct upper current and lower matrix
        # Current Level
        cur_level = pyramid[level]
        cur_level_mtx = np.zeros((n + offset, m + offset))
        cur_level_mtx[1: n + 1, 1: m + 1] = cur_level[0: n, 0: m]
        # Upper Level
        upper_level = pyramid[level - 1]
        up_level_mtx = np.zeros((n + offset, m + offset))
        up_level_mtx[1: n + 1, 1: m + 1] = upper_level[0: n, 0: m]
        # Lower Level
        lower_level = pyramid[level + 1]
        low_level_mtx = np.zeros((n + offset, m + offset))
        low_level_mtx[1: n + 1, 1: m + 1] = lower_level[0: n, 0: m]

        print(cur_level_mtx)

        for row in range(n):
            for col in range(m):
                # Prepare for filtering
                patch_size = 3
                c_p = (patch_size - 1) // 2
                # Get currently filtering matrices from upper, current, lower levels
                upper_mtx = np.array(up_level_mtx[row: row + patch_size, col: col + patch_size])
                cur_mtx = np.array(cur_level_mtx[row: row + patch_size, col: col + patch_size])
                lower_mtx = np.array(low_level_mtx[row: row + patch_size, col: col + patch_size])
                # Get max value form upper, current, lower levels
                up_cur_low_max = []
                up_cur_low_max.append(np.max(upper_mtx))
                up_cur_low_max.append(np.max(cur_mtx))
                up_cur_low_max.append(np.max(lower_mtx))
                max_value = np.amax(up_cur_low_max)
                # Get current filtering center point value
                c_p_value = cur_mtx[c_p, c_p]
                # Threshold
                if max_value == c_p_value and threshold < c_p_value:
                    max_list.append(((row, col), sigma_list[level]))

    for max in max_list:
        cv2.circle(image, (max[0][1], max[0][0]), int(np.round(max[1])) * 3, color=(204, 51, 0), thickness=2)
    plt.imshow(image)
    plt.show()


def sift_extract(image):
    img = cv2.imread(image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialized sift
    sift = cv2.xfeatures2d.SIFT_create(2000)

    # Get keypoints and features
    keypoints, features = sift.detectAndCompute(gray_img, None)
    result = cv2.drawKeypoints(gray_img, keypoints, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, outImage=None)

    cv2.imwrite('sift_keypoints.jpg', result)
    return keypoints, features


def sift_matching(image1, image2, ratio_threshold, norm_level):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    kp_1, des_1 = sift_extract(image1)
    kp_2, des_2 = sift_extract(image2)
    num_des_1 = np.shape(des_1)[0]
    num_des_2 = np.shape(des_2)[0]
    num_matching_keypoint = num_des_1

    candidate_keypoint_location = []
    candidate_distance = []

    # Compare all keypoints
    for i in range(num_des_1):
        distance = []
        for j in range(num_des_2):
            euclidean_dis = euclidean_distance(des_1[i], des_2[j], norm_level)
            distance.append(euclidean_dis)
        # find two smallest distance match
        two_smallest_distance = heapq.nsmallest(2, distance)
        candidate_distance.append(two_smallest_distance)
        # find minimum distance index at keypoint 2
        np_distance = np.array(distance)
        min_dis_index = np.unravel_index(np.argmin(np_distance, axis=None), np_distance.shape)[0]
        candidate_keypoint_location.append(min_dis_index)

    keypoint1 = []
    keypoint2 = []
    keypoints_pairs = {}
    count = 0

    for i in range(num_matching_keypoint):
        ratio = np.true_divide(candidate_distance[i][0], candidate_distance[i][1])
        if ratio < ratio_threshold:
            count = count + 1
            kp1 = kp_1[i]
            kp2 = kp_2[candidate_keypoint_location[i]]
            keypoint1.append(kp1)
            keypoint2.append(kp2)
            keypoints_pairs[(kp1,kp2)] = ratio

    sorted_keypointes = sorted(keypoints_pairs.items(), key=lambda kv: kv[1])

    print("number of matching = ", count)

    top_ten = sorted_keypointes[0:9]
    print(top_ten)

    result_img1 = cv2.drawKeypoints(gray1, keypoint1, outImage=None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    result_img2 = cv2.drawKeypoints(gray2, keypoint2, outImage=None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite("sample1_keypoints_final.jpg", result_img1)
    cv2.imwrite("sample2_keypoints_final.jpg", result_img2)
    show_matching(gray1, keypoint1, gray2, keypoint2)

    return top_ten

def generate_top_ten(image1, image2, top_ten):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    keypoint1 = []
    keypoint2 = []

    for item in top_ten:
        keypoint1.append(item[0][0])
        keypoint2.append(item[0][1])

    show_matching(gray1, keypoint1, gray2, keypoint2)


def euclidean_distance(vector1, vector2, norm_level):
    vector1 = vector1.reshape(-1)
    vector2 = vector2.reshape(-1)
    distance = np.linalg.norm(vector1 - vector2, ord=norm_level)
    return distance

def euclidean_distance2(vector1, vector2):
    vector1_square = np.sum(np.square(vector1), axis=1).reshape(-1, 1)
    vector2_square = np.sum(np.square(vector2), axis=1).reshape(-1, 1)
    vector1_vector2 = np.dot(vector1, np.transpose(vector2))
    distance = np.sqrt(vector1_square - 2 * vector1_vector2 + np.transpose(vector2_square))
    return distance

def show_matching(image1, keypoint1, image2, keypoint2):
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)
    img1 = cv2.drawKeypoints(image1, keypoint1, None)
    img2 = cv2.drawKeypoints(image2, keypoint2, None)
    ax1.imshow(img1)
    ax2.imshow(img2)

    colors = ["white", "red", "blue", "orange", "pink", "yellow"]
    color_i = 0
    for kp1, kp2 in zip(keypoint1, keypoint2):
        coord1 = kp1.pt
        coord2 = kp2.pt
        c = colors[color_i % 6]
        con = ConnectionPatch(xyA=coord2, xyB=coord1, coordsA="data", coordsB="data", axesA=ax2, axesB=ax1, arrowstyle="-", color=c)
        ax2.add_patch(con)
        color_i += 1
    plt.show()

def AddGaussianNoise(image):
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    mean = 0
    sigma = 0.08
    temp = img / 255

    gaussian = np.random.normal(mean, sigma, size=temp.shape)
    noisy_image = temp + gaussian

    return noisy_image * 255


def sift_matching_color(image1, image2, threshold):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    # Only use h of hsv (h include all colour information)
    img1_r = img1[0:img1.shape[0], 0:img1.shape[1], 2]
    img2_r = img2[0:img2.shape[0], 0:img2.shape[1], 2]

    img1_g = img1[0:img1.shape[0], 0:img1.shape[1], 1]
    img2_g = img2[0:img2.shape[0], 0:img2.shape[1], 1]

    img1_b = img1[0:img1.shape[0], 0:img1.shape[1], 0]
    img2_b = img2[0:img2.shape[0], 0:img2.shape[1], 0]

    kp_1, des_1 = sift_extract(image1)
    kp_2, des_2 = sift_extract(image2)

    sift = cv2.xfeatures2d.SIFT_create(2000)

    kp_1, des_1r = sift.compute(img1_r, kp_1)
    kp_2, des_2r = sift.compute(img2_r, kp_2)
    euclidean_dis_r = euclidean_distance2(des_1r, des_2r)

    kp_1, des_1g = sift.compute(img1_g, kp_1)
    kp_2, des_2g = sift.compute(img2_g, kp_2)
    euclidean_dis_g = euclidean_distance2(des_1g, des_2g)

    kp_1, des_1b = sift.compute(img1_b, kp_1)
    kp_2, des_2b = sift.compute(img2_b, kp_2)
    euclidean_dis_b = euclidean_distance2(des_1b, des_2b)


    # find minimum distance index in keypoint 2
    min_keypoints_index_r = np.argmin(euclidean_dis_r, axis=1)
    min_keypoints_index_g = np.argmin(euclidean_dis_g, axis=1)
    min_keypoints_index_b = np.argmin(euclidean_dis_b, axis=1)

    num_matching_keypoint_r = len(min_keypoints_index_r)
    num_matching_keypoint_g = len(min_keypoints_index_g)
    num_matching_keypoint_b = len(min_keypoints_index_b)

    # find smallest and 2nd smallest distance
    smallest_r = np.sort(euclidean_dis_r, axis=1)[:, 0]
    second_smallest_r = np.sort(euclidean_dis_r, axis=1)[:, 1]
    smallest_g = np.sort(euclidean_dis_g, axis=1)[:, 0]
    second_smallest_g = np.sort(euclidean_dis_g, axis=1)[:, 1]
    smallest_b = np.sort(euclidean_dis_b, axis=1)[:, 0]
    second_smallest_b = np.sort(euclidean_dis_b, axis=1)[:, 1]

    # compute ratio
    ratio_r = np.true_divide(smallest_r, second_smallest_r)
    ratio_g = np.true_divide(smallest_g, second_smallest_g)
    ratio_b = np.true_divide(smallest_b, second_smallest_b)

    keypoint1 = []
    keypoint2 = []
    matched_ratio = []
    keypoints_pairs = {}
    count = 0

    for i in range(num_matching_keypoint_r):
        if ratio_r[i] < threshold:
            count = count + 1
            kp1 = kp_1[i]
            kp2 = kp_2[min_keypoints_index_r[i]]
            keypoint1.append(kp1)
            keypoint2.append(kp2)
            matched_ratio.append(ratio_r[i])
            keypoints_pairs[(kp_1[i], kp2)] = ratio_r[i]

    for i in range(num_matching_keypoint_g):
        if ratio_g[i] < threshold:
            count = count + 1
            kp1 = kp_1[i]
            kp2 = kp_2[min_keypoints_index_g[i]]
            keypoint1.append(kp1)
            keypoint2.append(kp2)
            matched_ratio.append(ratio_g[i])
            keypoints_pairs[(kp_1[i], kp2)] = ratio_g[i]

    for i in range(num_matching_keypoint_b):
        print(ratio_b[i])
        if ratio_b[i] < threshold:
            count = count + 1
            kp1 = kp_1[i]
            kp2 = kp_2[min_keypoints_index_b[i]]
            keypoint1.append(kp1)
            keypoint2.append(kp2)
            matched_ratio.append(ratio_b[i])
            keypoints_pairs[(kp_1[i], kp2)] = ratio_b[i]

    sorted_keypointes = sorted(keypoints_pairs.items(), key=lambda kv: kv[1])
    print("number of matching = ", count)
    top_ten = sorted_keypointes[0:9]
    print(top_ten)

    result_img1 = cv2.drawKeypoints(img1, keypoint1, outImage=None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    result_img2 = cv2.drawKeypoints(img2, keypoint2, outImage=None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite("sample1_keypoints_final_color.jpg", result_img1)
    cv2.imwrite("sample2_keypoints_final_color.jpg", result_img2)

    # height_1, width_1, rgb_1 = img1.shape
    # temp_1 = img1.copy()
    #
    # for row in range(height_1):
    #     for list in range(width_1):
    #         for c in range(rgb_1):
    #             pv = img1[row, list, c]
    #             temp_1[row, list, c] = 255 - pv
    #
    # height_2, width_2, rgb_2 = img2.shape
    # temp_2 = img2.copy()
    #
    # for row in range(height_2):
    #     for list in range(width_2):
    #         for c in range(rgb_2):
    #             pv = img1[row, list, c]
    #             temp_2[row, list, c] = 255 - pv

    show_matching(img1, keypoint1, img2, keypoint2)

    return top_ten

def generate_top_ten_color(image1, image2, top_ten):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    keypoint1 = []
    keypoint2 = []

    for item in top_ten:
        keypoint1.append(item[0][0])
        keypoint2.append(item[0][1])

    show_matching(img1, keypoint1, img2, keypoint2)

if __name__ == "__main__":

    img_bee = cv2.imread("./bee.jpg")
    img_building = cv2.imread("./building.jpg")

    rows, cols, rgb = img_building.shape
    rotated_building = cv2.getRotationMatrix2D((cols / 2, rows / 2), 60, 1)
    dst = cv2.warpAffine(img_building, rotated_building, (cols, rows))


    # q1a1 = OneDimLinearInterpolation(img_bee, 4, 0)
    # cv2.imwrite("./q1a1.jpg", q1a1)
    #
    # q1a2 = OneDimLinearInterpolation(img_bee, 4, 1)
    # cv2.imwrite("./q1a2.jpg", q1a2)
    #
    # q1a = OneDimLinearInterpolation(q1a1, 4, 1)
    # cv2.imwrite("./q1a.jpg", q1a)
    #
    # q1b = TwoDimLinearInterpolation(img_bee, 4)
    # cv2.imwrite("./q1b.jpg", q1b)

    # q1b2 = TwoDimLinearInterpolation(img_bee, 3)
    # cv2.imwrite("./q1b2.jpg", q1b2)




    # q2a_harris = harris(img_building, 0.05, 0.01)
    # q2a_harris2 = harris2(img_building, 0.05, 0.01)

    # q2a_brown = brown(img_building)
    # q2a_brown2 = brown2(img_building)

    # q2a_harris_suppression = harris(img_building, 0.05, 0.01, 1)
    # q2a_brown_suppression = brown(img_building, 5)

    # q2a_harris_rotated = harris(dst, 0.05, 0.01, 1)

    LOG(img_building,levels=5,initial_sigma=1.6,scale=np.sqrt(2),threshold=5)




    # sift_extract("./sample1.jpg")
    # sift_extract("./sample2.jpg")

    # sift_extract("./sample1_noise.jpg")
    # sift_extract("./sample2_noise.jpg")

    # top_ten = sift_matching("./sample1.jpg", "./sample2.jpg", 0.8, 1)
    # generate_top_ten("./sample1.jpg", "./sample2.jpg", top_ten)

    # sample1_noise = AddGaussianNoise("./sample1.jpg")
    # cv2.imwrite("./sample1_noise.jpg", sample1_noise)
    # sample2_noise = AddGaussianNoise("./sample2.jpg")
    # cv2.imwrite("./sample2_noise.jpg", sample2_noise)

    # top_ten = sift_matching("./sample1_noise.jpg", "./sample2_noise.jpg", 0.8, 2)
    # generate_top_ten("./sample1_noise.jpg", "./sample2_noise.jpg", top_ten)

    # top_ten_color = sift_matching_color("./colourTemplate.png", "./colourSearch.png", 0.8)
    # generate_top_ten_color("./colourTemplate.png", "./colourSearch.png", top_ten_color)


