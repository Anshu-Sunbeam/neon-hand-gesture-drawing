# Neon Hand Gesture Drawing

A beginner-friendly Python computer vision project that uses OpenCV and MediaPipe to track hand movement and draw neon trails in real time.

## What it does

- Tracks your hand using a webcam
- Detects your index finger
- Draws neon trails when your index finger is up
- Uses pinch gesture to stop drawing
- Lets you clear the screen and change neon colors

## Tech used

- Python
- OpenCV
- MediaPipe
- NumPy

## Files


main.py        # Main neon drawing app
skeleton.py    # Commented hand skeleton learning file
command.py     # Pinch gesture command experiment
controls.md    # Controls and shortcuts




```markdown
# Controls

## main.py

```text
Index finger up = Draw
Pinch thumb + index finger = Stop drawing
C = Clear screen
Q = Quit
1 = Pink neon
2 = Cyan neon
3 = Green neon
4 = Orange neon
