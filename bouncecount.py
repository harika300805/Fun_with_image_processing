import cv2
import numpy as np
import csv
points = []

def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  
        points.append((x, y))
        print(f"Point captured: {x}, {y}")

video_path = "Input.mov"
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

if ret:
    cv2.imshow("Click on 4 Points", frame)
    cv2.setMouseCallback("Click on 4 Points", get_coordinates)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Captured Points:", points)
else:
    print("Error: Could not load video frame.")

cap.release()

def nothing(x):
    pass

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not load video frame.")
    exit()

# Convert frame to HSV
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("H Low", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("H High", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("S Low", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("S High", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("V Low", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("V High", "Trackbars", 255, 255, nothing)

while True:
    h_low = cv2.getTrackbarPos("H Low", "Trackbars")
    h_high = cv2.getTrackbarPos("H High", "Trackbars")
    s_low = cv2.getTrackbarPos("S Low", "Trackbars")
    s_high = cv2.getTrackbarPos("S High", "Trackbars")
    v_low = cv2.getTrackbarPos("V Low", "Trackbars")
    v_high = cv2.getTrackbarPos("V High", "Trackbars")

    # Create a mask
    lower_bound = np.array([h_low, s_low, v_low])
    upper_bound = np.array([h_high, s_high, v_high])
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Lower Bound:", lower_bound)
        print("Upper Bound:", upper_bound)
        break

cv2.destroyAllWindows()

cap = cv2.VideoCapture(video_path)

fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

grid_points = np.array([[100, 50], [500, 50], [500, 400], [100, 400]], dtype=np.float32)

dest_points = np.array([[0, 0], [400, 0], [400, 400], [0, 400]], dtype=np.float32)

M = cv2.getPerspectiveTransform(grid_points, dest_points)

lower_bound = np.array([30, 90, 90])  
upper_bound = np.array([80, 255, 255])

previous_y = None
bounces = 0
bounce_data = []

# CSV File Setup
csv_filename = "bounce_data.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp (s)", "Bounce Count", "Region"])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    warped_frame = cv2.warpPerspective(frame, M, (400, 400))

    hsv = cv2.cvtColor(warped_frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        ball_center = (x + w // 2, y + h // 2)

        if previous_y is not None and ball_center[1] > previous_y:
            bounces += 1
            timestamp = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)  
            region = "Left" if ball_center[0] < 200 else "Right"
            print(f"Bounce {bounces} at {timestamp}s in {region} region")

            with open(csv_filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, bounces, region])

        previous_y = ball_center[1]

        cv2.circle(warped_frame, ball_center, 10, (0, 255, 0), -1)

    for i in range(4):
        cv2.line(frame, tuple(grid_points[i]), tuple(grid_points[(i + 1) % 4]), (255, 0, 0), 2)

    cv2.imshow("Warped View", warped_frame)
    cv2.imshow("Original Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
