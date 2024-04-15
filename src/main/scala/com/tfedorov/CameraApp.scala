package com.tfedorov

import org.opencv.core.{Core, Mat, Point, Scalar}
import org.opencv.videoio.VideoCapture
import org.opencv.highgui.HighGui
import org.opencv.imgproc.Imgproc

object CameraApp {

  def detectLeftShift(currentFrame: Mat, previousFrame: Mat): Int = {
    // Your detection logic here...
    1
  }

  def main(args: Array[String]): Unit = {
    try {
      // Load OpenCV native library
      System.loadLibrary(Core.NATIVE_LIBRARY_NAME)
    } catch {
      case e: UnsatisfiedLinkError =>
        println("Error: Failed to load OpenCV native library.")
        e.printStackTrace()
        System.exit(1)
    }

    val camera = new VideoCapture(0)

    if (!camera.isOpened) {
      println("Error: Unable to open camera.")
      System.exit(1)
    }

    val windowName = "Live Video"
    HighGui.namedWindow(windowName, HighGui.WINDOW_NORMAL)

    var prevFrame = new Mat()

    // Loop until the Esc key is pressed or the window is closed
    var continueLoop = true
    while (continueLoop) {
      val frame = new Mat()
      camera.read(frame)

      if (!frame.empty()) {
        if (prevFrame.empty()) {
          // Store the first frame as the previous frame
          prevFrame = frame.clone()
        } else {
          // Detect left shift
          val leftShift = detectLeftShift(frame, prevFrame)
          println(s"Left shift detected: $leftShift pixels")

          // Draw a red line indicating the left shift
          val startPoint = new Point(0, leftShift)
          val endPoint = new Point(frame.cols(), leftShift)
          Imgproc.line(frame, startPoint, endPoint, new Scalar(0, 0, 255), 2)
        }

        // Display the frame
        HighGui.imshow(windowName, frame)
      }

      // Check for Esc key press or window closure
      val key = HighGui.waitKey(1)
      if (key == 27 || key == -1) {
        continueLoop = false
      }

      // Release the previous frame and update it
      prevFrame.release()
      prevFrame = frame.clone()
    }

    camera.release()
    HighGui.destroyAllWindows()
  }
}
