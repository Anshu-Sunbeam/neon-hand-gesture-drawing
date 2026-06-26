import cv2
import mediapipe as mp

camera = cv2.VideoCapture(0)#Use camera number 0.

mp_hands = mp.solutions.hands#gives us the hand detection system.
mp_draw = mp.solutions.drawing_utils#gives us helper functions to draw the dots and lines.

hands = mp_hands.Hands(
    max_num_hands=1,#Only track one hand.
    min_detection_confidence=0.7,#Only accept a hand if MediaPipe is at least fairly confident.
    min_tracking_confidence=0.7#Only keep tracking if it is fairly confident frame-to-frame.
)
#Lower values detect more easily but can be messy. Higher values are stricter but may lose hand hand position
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
            h, w, c = frame.shape#height,width,colour ∝ image

            index_tip = hand_landmarks.landmark[8]

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            cv2.circle(frame, (x, y), 12, (0, 255, 0), -1)#frame,centre,radius,colour,thickness

    cv2.imshow("Hand Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):#This checks if you pressed q.
        break

camera.release()#stop using webcam
cv2.destroyAllWindows()# close OpenCV windows