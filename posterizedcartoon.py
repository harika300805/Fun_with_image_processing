import numpy as np
import matplotlib.pyplot as plt
import cv2

path="face.jpg"
image=cv2.imread(path)
imco=image.copy()
image_RGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
image_blur=cv2.medianBlur(imco,3)
cv2.imshow("Output",image)
cv2.imshow("Output",image_RGB)
cv2.imshow("Output",image_blur)
cv2.waitKey()
cv2.destroyAllWindows()

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_blur)
plt.title("Blurred Image")
plt.axis("off")

plt.show()

n = 8  # Number of discrete levels
lookup_table = np.linspace(0, 255, n, dtype=np.uint8)
full_lut = np.interp(np.arange(256), np.linspace(0, 255, n), lookup_table).astype(np.uint8)

# Apply the LUT transformation
quantized_image = cv2.LUT(image_RGB, full_lut)

# Display the LUT transformed image
plt.figure(figsize=(5, 5))
plt.imshow(quantized_image)
plt.title("LUT Transformed Image")
plt.axis("off")
plt.show()