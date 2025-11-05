# collect_data.py

import cv2
import os
import numpy as np
import mediapipe as mp

# Settings
DATA_PATH = 'MP_Data'
actions = np.array(['swipeLeft', 'swipeRight'])
no_sequences = 30
sequence_length = 30

# Create folders
for action in actions:
    for sequence in range(no_sequences):
        os.makedirs(os.path.join(DATA_PATH, action, str(sequence)), exist_ok=True)

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


# Extract hand keypoints
def extract_keypoints(results):
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
    return np.zeros(21 * 3)

# Star capture
cap = cv2.VideoCapture(0)
for action in actions:
    for sequence in range(no_sequences):
        for frame_num in range(sequence_length):
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Show instructions
            if frame_num == 0:
                cv2.putText(image, f'STARTING {action} SEQ {sequence}', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Recording', image)
                cv2.waitKey(2000)
            else:
                cv2.putText(image, f'{action} Seq {sequence} Frame {frame_num}', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            keypoints = extract_keypoints(results)
            np.save(os.path.join(DATA_PATH, action, str(sequence), str(frame_num)), keypoints)

            cv2.imshow('Recording', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()


