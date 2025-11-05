# import mediapipe as mp
# import cv2
# import numpy as np
# import os
# import time
# from sklearn.model_selection import train_test_split
# from keras.utils import to_categorical
# from keras.models import Sequential
# from keras.layers import LSTM, Dense
# from keras.callbacks import TensorBoard


# # Initialize MediaPipe
# mp_holistic = mp.solutions.holistic
# mp_drawing = mp.solutions.drawing_utils
# mp_face_mesh = mp.solutions.face_mesh

# # Global variables
# DATA_PATH = os.path.join('MP_Data')
# actions = np.array(['hello', 'swipeLeft ', 'swipeRight'])
# no_sequences = 30
# sequence_length = 30
# label_map = {label: num for num, label in enumerate(actions)}
# model = None
# colors = [(245,117,16), (117,245,16), (16,117,245)]

# # ---------- Utility Functions ----------

# def mediapipe_detection(image, model):
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image.flags.writeable = False
#     results = model.process(image)
#     image.flags.writeable = True
#     return cv2.cvtColor(image, cv2.COLOR_RGB2BGR), results

# def draw_landmarks(image, results):
#     if results.face_landmarks:
#         mp_drawing.draw_landmarks(
#             image, results.face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
#             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
#             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
#         )
#     if results.pose_landmarks:
#         mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
#     if results.left_hand_landmarks:
#         mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
#     if results.right_hand_landmarks:
#         mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

# def extract_keypoints(results):
#     pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]) \
#         .flatten() if results.pose_landmarks else np.zeros(33 * 4)
#     face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]) \
#         .flatten() if results.face_landmarks else np.zeros(468 * 3)
#     lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]) \
#         .flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
#     rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]) \
#         .flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
#     return np.concatenate([pose, face, lh, rh])

# def prob_viz(res, actions, image, colors):
#     output = image.copy()
#     for num, prob in enumerate(res):
#         cv2.rectangle(output, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
#         cv2.putText(output, actions[num], (0, 85 + num * 40),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#     return output

# # ---------- Functional Steps ----------

# def collect_data():
#     for action in actions:
#         for sequence in range(no_sequences):
#             try:
#                 os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
#             except:
#                 pass

#     cap = cv2.VideoCapture(0)
#     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
#         for action in actions:
#             for sequence in range(no_sequences):
#                 for frame_num in range(sequence_length):
#                     ret, frame = cap.read()
#                     image, results = mediapipe_detection(frame, holistic)
#                     draw_landmarks(image, results)

#                     if frame_num == 0:
#                         cv2.putText(image, 'STARTING COLLECTION', (120, 200),
#                                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
#                         cv2.imshow('OpenCV Feed', image)
#                         cv2.waitKey(2000)
#                     else:
#                         cv2.putText(image, f'Collecting frames for {action} Video {sequence}', (15, 12),
#                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
#                         cv2.imshow('OpenCV Feed', image)

#                     keypoints = extract_keypoints(results)
#                     np.save(os.path.join(DATA_PATH, action, str(sequence), str(frame_num)), keypoints)

#                     if cv2.waitKey(10) & 0xFF == ord('q'):
#                         break
#     cap.release()
#     cv2.destroyAllWindows()

# def load_data():
#     sequences, labels = [], []
#     for action in actions:
#         for sequence in range(no_sequences):
#             window = []
#             for frame_num in range(sequence_length):
#                 res = np.load(os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy"))
#                 window.append(res)
#             sequences.append(window)
#             labels.append(label_map[action])
#     X = np.array(sequences)
#     y = to_categorical(labels).astype(int)
#     return train_test_split(X, y, test_size=0.05)

# def build_model():
#     global model
#     model = Sequential()
#     model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 1662)))
#     model.add(LSTM(128, return_sequences=True, activation='relu'))
#     model.add(LSTM(64, return_sequences=False, activation='relu'))
#     model.add(Dense(64, activation='relu'))
#     model.add(Dense(32, activation='relu'))
#     model.add(Dense(actions.shape[0], activation='softmax'))

#     model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# def train_model(X_train, y_train):
#     log_dir = os.path.join('Logs')
#     tb_callback = TensorBoard(log_dir=log_dir)
#     model.fit(X_train, y_train, epochs=200, callbacks=[tb_callback])

# def predict_live(threshold=0.8):
#     sequence = []
#     sentence = []
#     cap = cv2.VideoCapture(0)
#     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             image, results = mediapipe_detection(frame, holistic)
#             draw_landmarks(image, results)

#             keypoints = extract_keypoints(results)
#             sequence.append(keypoints)
#             sequence = sequence[-30:]

#             if len(sequence) == 30:
#                 res = model.predict(np.expand_dims(sequence, axis=0))[0]

#                 if res[np.argmax(res)] > threshold:
#                     if len(sentence) > 0:
#                         if actions[np.argmax(res)] != sentence[-1]:
#                             sentence.append(actions[np.argmax(res)])
#                     else:
#                         sentence.append(actions[np.argmax(res)])

#                 if len(sentence) > 5:
#                     sentence = sentence[-5:]

#                 image = prob_viz(res, actions, image, colors)

#             cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
#             cv2.putText(image, ' '.join(sentence), (3, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

#             cv2.imshow('OpenCV Feed', image)

#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 break
#     cap.release()
#     cv2.destroyAllWindows()


# collect_data()






























import cv2
import mediapipe as mp
import pyautogui
from time import sleep

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
gesture_triggered = False

def get_fingers_up(hand_landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    # Thumb: compare x of tip and preceding joint
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers: tip y lower than pip y means finger is up
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
            fingers = get_fingers_up(hand_landmark)

            # Gesture: index finger up => Next slide
            if fingers == [0,1,0,0,0] and not gesture_triggered:
                print("➡️ Next Slide")
                pyautogui.press("right")
                gesture_triggered = True

            # Gesture: pinky finger up => Previous slide
            elif fingers == [0,0,0,0,1] and not gesture_triggered:
                print("⬅️ Previous Slide")
                pyautogui.press("left")
                gesture_triggered = True
                
            # Reset trigger when no gesture
            elif fingers != [0,1,0,0,0] and fingers != [0,0,0,0,1]:
                gesture_triggered = False

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
