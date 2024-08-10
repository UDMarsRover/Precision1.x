import cv2
import numpy as np
import glob
"""
img1 = "C:\\Users\\Paul\\MarsRoverWork\\Precision1.x\\src\\base_pkg\\gui\\elements\\captured_image_5.jpg"
img2 = "C:\\Users\\Paul\\MarsRoverWork\\Precision1.x\\src\\base_pkg\\gui\\elements\\captured_image_6.jpg"

# Load the images
image1 = cv2.imread(img1)
image2 = cv2.imread(img2)

images = [image1, image2]
num_images = len(images)

#cv2.imshow("IMG1", image1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
"""
"""plt.figure(figsize=[30,10])
num_cols = 3
num_rows = math.ceil(num_images / num_cols)
for i in range(0, num_images):
    plt.subplot(num_rows, num_cols, i+1)
    plt.axis('off')
    plt.imshow(images[i])"""

image_paths = glob.glob("src/base_pkg/gui/elements/*.jpg")
for thing in image_paths:
    print(thing)
#image_paths = ["C:\\Users\\Paul\\MarsRoverWork\\Precision1.x\\src\\base_pkg\\gui\\elements\\captured_image_13.jpg", "C:\\Users\\Paul\\MarsRoverWork\\Precision1.x\\src\\base_pkg\\gui\\elements\\captured_image_14.jpg", "C:\\Users\\Paul\\MarsRoverWork\\Precision1.x\\src\\base_pkg\\gui\\elements\\captured_image_15.jpg"]
images = []

for image in image_paths:
    img = cv2.imread(image)
    images.append(img)
    cv2.imshow("Image", img)
    cv2.waitKey(1000) #waitKey(0) does not work correctly on Linux from my experience
    cv2.destroyAllWindows()

print(images)

imageStitcher = cv2.Stitcher_create()

error, stitched_img = imageStitcher.stitch(images)

if error: 
    print("sad")
    print(error)

if not error:

    cv2.imwrite("stitchedOutput.png", stitched_img)
    cv2.imshow("Stitch", stitched_img)
    cv2.waitKey(0)

print("done")
"""
stitcher = cv2.Stitcher_create()
error, result = stitcher.stitch(images)

if error:

    cv2.imwrite("stichedOutput.jpg", result)
    cv2.imshow("Stiched", result)
    cv2.waitKey(0)

#if status == 0:
#    plt.figure(figsize=[30,10])
#    plt.imshow(result)

#check = error == 0
#print(check)
#cv2.imshow("result", result)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
"""
"""
img1 = "C:\\Users\\Paul\\MarsRoverWork\\Precision1.x\\src\\base_pkg\\gui\\elements\\captured_image_5.jpg"
img2 = "C:\\Users\\Paul\\MarsRoverWork\\Precision1.x\\src\\base_pkg\\gui\\elements\\captured_image_6.jpg"

# Load the images
image1 = cv2.imread(img1)
image2 = cv2.imread(img2)

images = [image1, image2]

num_images = len(images)

stitcher = cv2.Stitcher_create()
status, result = stitcher.stitch(images)
cv2.imshow("Result", result)
"""