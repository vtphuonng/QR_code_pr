import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import PIL

# Read image as grayscale, get dimensions
img = cv2.imread('image/qr3.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img.shape

# Binarize image to get rid of aliasing artifacts (gray-ish colors)
img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)[1]

# Morphological closing to get rid of artifacts
img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))

# Count white pixels per row and column to crop actual QR code
sum_x = np.sum(img_bin == 255, axis=1)
sum_y = np.sum(img_bin == 255, axis=0)
y1, y2 = np.argwhere(sum_x < w)[[0, -1], 0]
x1, x2 = np.argwhere(sum_y < h)[[0, -1], 0]
cropped = img_bin[y1:y2, x1:x2]

# Resize cropped part to actual QR code dimension (25, 25)
resized = cv2.resize(cropped, (100))

# Resize to destination size
dst_size = (700, 700)
resized_dst = cv2.resize(resized, dst_size, interpolation=cv2.INTER_NEAREST)

# Add white borders of desired size
m = 40
output = cv2.copyMakeBorder(resized_dst, m, m, m, m, cv2.BORDER_CONSTANT, value=255)

# save a image using extension

#cv2.imwrite('qr5.jpg', img)
# Just for visualization
plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray'), plt.title('Original image')
plt.subplot(2, 2, 2), plt.imshow(cropped, cmap='gray'), plt.title('Cropped part')
plt.subplot(2, 2, 3), plt.imshow(resized, cmap='gray'), plt.title('Resized to QR code dimensions')
plt.subplot(2, 2, 4), plt.imshow(output, cmap='gray'), plt.title('Final output')
plt.tight_layout(), plt.show()

