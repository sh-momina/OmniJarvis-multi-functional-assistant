import cv2 
import numpy as np
import pyautogui
import mediapipe as mp
from keras.models import load_model
import time
import os
import random

def control():
    # --- OPEN RANDOM PRESENTATION ---
    presentation_paths = [
        r"D:\study\semester 6\Artifitial intellegence\content\2.1 Means End Analysis.pptx"
    ]
    
    # Pick a random presentation (you can replace with your own path)
    selected_presentation = random.choice(presentation_paths)
    os.startfile(selected_presentation)
    print(f"Opened presentation: {selected_presentation}")

    # --- LOAD MODEL AND SETUP ---
    model = load_model("gesture_model.h5")
    actions = np.array(['swipeLeft', 'swipeRight'])

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    def extract_keypoints(results):
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
        return np.zeros(21 * 3)

    sequence = []
    threshold = 0.5 
    cooldown_time = 2 
    last_action_time = 0

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for landmark in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, landmark, mp_hands.HAND_CONNECTIONS)

        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            prediction = actions[np.argmax(res)]
            confidence = res[np.argmax(res)]

            current_time = time.time()
            if confidence > threshold and (current_time - last_action_time) > cooldown_time:
                if prediction == 'swipeRight':
                    print("➡️ Next Slide")
                    pyautogui.press("right")
                    last_action_time = current_time
                elif prediction == 'swipeLeft':
                    print("⬅️ Previous Slide")
                    pyautogui.press("right")
                    last_action_time = current_time

        cv2.imshow("Gesture Slide Control", image)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start the control
control()
