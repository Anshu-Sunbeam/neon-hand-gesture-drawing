import cv2
import mediapipe as mp
import numpy as np

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

prev_x, prev_y = None, None
canvas = None
glow_canvas = None

# Neon colors in OpenCV BGR format
glow_color = (255, 0, 255)   # pink/magenta glow
core_color = (255, 255, 255) # white center line

while True:
    success, frame = camera.read()

    if not success:
        print("Camera not working.")
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)
        glow_canvas = np.zeros_like(frame)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, c = frame.shape

            index_tip = hand_landmarks.landmark[8]
            index_middle = hand_landmarks.landmark[6]
            thumb_tip = hand_landmarks.landmark[4]

            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)

            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            # Distance between thumb and index finger
            distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5
            pinch = distance < 40

            # Index finger is up if tip is above middle joint
            index_is_up = index_tip.y < index_middle.y

            if pinch:
                prev_x, prev_y = None, None

                cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)
                cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 0, 255), -1)
                cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (0, 0, 255), 2)

                cv2.putText(frame, "PINCH - NOT DRAWING", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            elif index_is_up:
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)

                if prev_x is not None and prev_y is not None:
                    # Thick glow strokes
                    cv2.line(glow_canvas, (prev_x, prev_y), (index_x, index_y), glow_color, 24)
                    cv2.line(glow_canvas, (prev_x, prev_y), (index_x, index_y), glow_color, 12)

                    # Bright sharp center
                    cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), core_color, 4)

                prev_x, prev_y = index_x, index_y

                cv2.putText(frame, "DRAWING", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            else:
                prev_x, prev_y = None, None

                cv2.putText(frame, "NOT DRAWING", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    else:
        prev_x, prev_y = None, None

    # Blur the glow layer to make it neon-like
    blurred_glow = cv2.GaussianBlur(glow_canvas, (21, 21), 0)

    # Merge webcam + glow + sharp lines
    output = cv2.addWeighted(frame, 1.0, blurred_glow, 0.8, 0)
    output = cv2.addWeighted(output, 1.0, canvas, 1.0, 0)

    cv2.imshow("Neon Hand Drawing", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):
        canvas = np.zeros_like(frame)
        glow_canvas = np.zeros_like(frame)
        prev_x, prev_y = None, None

    elif key == ord("1"):
        glow_color = (255, 0, 255)   # pink

    elif key == ord("2"):
        glow_color = (255, 255, 0)   # cyan

    elif key == ord("3"):
        glow_color = (0, 255, 0)     # green

    elif key == ord("4"):
        glow_color = (0, 165, 255)   # orange

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()