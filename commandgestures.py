import cv2
import mediapipe as mp
import pyautogui
import time

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

last_action_time = 0
cooldown = 2

while True:
    success, frame = camera.read()

    if not success:
        print("Camera not working.")
        break

    frame = cv2.flip(frame, 1)

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

            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]

            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)

            distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5

            pinch = distance < 40

            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 0, 255), -1)
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 0), 3)

            current_time = time.time()

            if pinch and current_time - last_action_time > cooldown:
                pyautogui.hotkey("ctrl", "t")
                last_action_time = current_time

                cv2.putText(frame, "NEW TAB OPENED", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)

            if pinch:
                status = "PINCH"
            else:
                status = "NO PINCH"

            cv2.putText(frame, status, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)

    cv2.imshow("Gesture Controller", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()