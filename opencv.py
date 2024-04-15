import cv2
import time

def draw_point(frame, center_x, center_y, color):
    # Draw a point on the specified coordinates with the given color
    cv2.circle(frame, (center_x, center_y), 5, color, -1)

def calculate_shift(frame, prev_frame, initial_center_x, initial_center_y):
    # Convert frames to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Calculate the absolute difference between the frames
    diff = cv2.absdiff(gray_frame, gray_prev_frame)

    # Threshold the difference image
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate shift based on the centroid of the largest contour
    shift_left_right = 0
    shift_up_down = 0
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            shift_left_right = cx - initial_center_x
            shift_up_down = cy - initial_center_y

    return shift_left_right, shift_up_down

def capture_screenshot():
    # Set the index to 0 for the default camera (usually the built-in one)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    # Create a window to display the live video
    cv2.namedWindow('Live Video', cv2.WINDOW_NORMAL)

    # Initialize previous frame and initial center coordinates
    _, prev_frame = cap.read()
    initial_center_x = prev_frame.shape[1] // 2
    initial_center_y = prev_frame.shape[0] // 2

    # Start time for the countdown
    start_time = time.time()

    # Continuously capture and display live video
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame is read correctly
        if not ret:
            print("Error: Unable to capture frame.")
            break

        # Draw countdown timer in the upper left corner
        elapsed_time = time.time() - start_time
        remaining_time = max(1 - elapsed_time, 0)
        cv2.putText(frame, f"Countdown: {remaining_time:.1f} sec", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Calculate shift after 1 second
        if elapsed_time > 1:
            shift_left_right, shift_up_down = calculate_shift(frame, prev_frame, initial_center_x, initial_center_y)
            red_point_x = initial_center_x
            red_point_y = initial_center_y
            draw_point(frame, red_point_x, red_point_y, (0, 0, 255))  # Draw red point

            # Calculate blue point coordinates based on the shift direction
            blue_point_x = initial_center_x - shift_left_right
            blue_point_y = initial_center_y - shift_up_down
            draw_point(frame, blue_point_x, blue_point_y, (255, 0, 0))  # Draw blue point

        # Display the frame
        cv2.imshow('Live Video', frame)

        # Update previous frame
        prev_frame = frame.copy()

        # Check for key press to exit (press 'q' to quit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_screenshot()
