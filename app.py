import cv2
import mediapipe as mp
import pyautogui
import time

webcam = cv2.VideoCapture(0)

my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Variables for smooth volume control
last_press = 0
cooldown = 0.2          # 200 ms between key presses
smooth_length = 0

while True:
    _, image = webcam.read()

    # Flip image for mirror view
    image = cv2.flip(image, 1)

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)

    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:

            drawing_utils.draw_landmarks(
                image,
                hand,
                mp.solutions.hands.HAND_CONNECTIONS
            )

            landmarks = hand.landmark

            thumb_x = thumb_y = 0
            index_x = index_y = 0

            for id, landmark in enumerate(landmarks):

                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])

                if id == 4:
                    thumb_x = x
                    thumb_y = y

                    cv2.circle(
                        image,
                        (x, y),
                        10,
                        (0, 255, 0),
                        cv2.FILLED
                    )

                if id == 8:
                    index_x = x
                    index_y = y

                    cv2.circle(
                        image,
                        (x, y),
                        10,
                        (0, 255, 0),
                        cv2.FILLED
                    )

            # Draw line between thumb and index finger
            cv2.line(
                image,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255, 0, 255),
                3
            )

            # Calculate distance
            length = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5

            # Smooth the distance
            smooth_length = 0.8 * smooth_length + 0.2 * length

            # Display distance
            cv2.putText(
                image,
                f"{int(smooth_length)}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

            current_time = time.time()

            # Volume control with cooldown
            if current_time - last_press > cooldown:

                if smooth_length < 40:
                    cv2.circle(
                        image,
                        (index_x, index_y),
                        10,
                        (0, 0, 255),
                        cv2.FILLED
                    )

                    pyautogui.press("volumedown")
                    last_press = current_time

                elif smooth_length > 120:
                    cv2.circle(
                        image,
                        (index_x, index_y),
                        10,
                        (0, 0, 255),
                        cv2.FILLED
                    )

                    pyautogui.press("volumeup")
                    last_press = current_time

    cv2.imshow("Hand Volume Control", image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

webcam.release()
cv2.destroyAllWindows()