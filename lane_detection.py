import cv2
import numpy as np


# Canny Function to differentiate the change in pixel value
def canny(img):
    copy_img = np.copy(img)
    gray_img = cv2.cvtColor(copy_img, cv2.COLOR_RGB2GRAY)
    blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    res = cv2.Canny(blur_img, 50, 150)
    return res

# Define a area of interest based on the frame
# It assumes the view from a dashcam

def region_of_interest(img):
    y = img.shape[0]
    tri_draw = np.array([[(180, y), (1050, y), (600, 250)]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, tri_draw, 255)
    mask_img = cv2.bitwise_and(img, mask)
    return mask_img


def make_coordinates(img, line_parameters):
    m, c = line_parameters
    y1 = img.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1- c)/(m))
    x2 = int((y2-c)/m)
    return np.array([x1, y1, x2, y2])

# function to calculate the correct line and calculate the slope of the lane line
def slope_intercept(img, dis_lines):
    left_fit = []
    right_fit = []
    for line in dis_lines:
        x1, y1, x2, y2 = line.reshape(4)
        coordinates = np.polyfit((x1, x2), (y1, y2), 1)
        m = coordinates[0]
        intercept = coordinates[1]
        if m < 0:
            left_fit.append((m, intercept))
        else:
            right_fit.append((m, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_lane = make_coordinates(img, left_fit_average)
    right_lane = make_coordinates(img, right_fit_average)
    return np.array([left_lane, right_lane])

# Function to draw the lane line on the frame
def display_line(img, dis_lines):
    line_image = np.zeros_like(img)
    if dis_lines is not None:
        for line in dis_lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


cap = cv2.VideoCapture('test_video.mp4')
while cap.isOpened():
    _, frame = cap.read()
    canny_1 = canny(frame)
    cropped_img = region_of_interest(canny_1)
    lines = cv2.HoughLinesP(cropped_img, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    average_slope = slope_intercept(frame, lines)
    line_img = display_line(frame, average_slope)
    combo_img = cv2.addWeighted(frame, 0.8, line_img, 1, 1)
    cv2.imshow("result", combo_img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()