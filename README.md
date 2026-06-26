# Neon Hand Gesture Drawing

A beginner-friendly Python computer vision project that uses OpenCV and MediaPipe to track hand movement and draw neon trails in real time.

## What it does

- Tracks your hand using a webcam
- Detects your index finger
- Draws neon trails when your index finger is up
- Uses pinch gesture to stop drawing
- Lets you clear the screen and change neon colors
- Includes a pinch gesture command experiment

## Tech used

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

## Files

```text
main.py        # Main neon drawing app
skeleton.py    # Commented hand skeleton learning file
command.py     # Pinch gesture command experiment


Controls
main.py
Index finger up = Draw
Pinch thumb + index finger = Stop drawing
C = Clear screen
Q = Quit
1 = Pink neon
2 = Cyan neon
3 = Green neon
4 = Orange neon
command.py
Thumb + index pinch = Open new browser tab
Q = Quit
Tips
Click on the OpenCV camera window before pressing keyboard controls.
Use good lighting for better hand tracking.
Keep your hand clearly visible to the webcam.
If tracking feels unstable, move your hand slower and keep fingers apart.
Notes

This project was built as a learning experiment to understand hand tracking, finger landmarks, gesture detection, and simple visual effects using Python.

It works best in good lighting with a clear webcam view.
