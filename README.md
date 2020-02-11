# Lane Detection using OpenCV
This script detects lane in a video using OpenCV. The scripts shows a simple way to detect the lanes on a road using the change in pixel value of the road when there is a lane. The script was developed using the 'test_image.jpg'.
- The image was converted to gray scale and blurred
- Canny function was used and the edges were drawn using trial and error to get the best possible edges
- A region of interest was defined to select the lanes
- Draw the average of the lines to determine the left and the right lane
- Open the video and repeat the procedure frame by frame
