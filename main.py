import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Function to count fingers
def count_fingers(hand_landmarks):
    fingers = []

    # Tip ids for fingers
    tips = [4, 8, 12, 16, 20]

    # Thumb
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

# Start webcam
cap = cv2.VideoCapture(0)

print("Gesture Music Control Started...")
print("1 Finger = Play | 2 = Pause | 3 = Next | 4 = Previous")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Convert to RGB
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(handLms)

            if fingers == 1:
                cv2.putText(img, "PLAY", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            elif fingers == 2:
                cv2.putText(img, "PAUSE", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

            elif fingers == 3:
                cv2.putText(img, "NEXT", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            elif fingers == 4:
                cv2.putText(img, "PREVIOUS", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Gesture Music Control", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
