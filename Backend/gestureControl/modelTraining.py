# train_model.py
import numpy as np
import os
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

DATA_PATH = 'MP_Data'
actions = np.array(['swipeLeft', 'swipeRight'])
sequence_length = 30

label_map = {label: num for num, label in enumerate(actions)}

# Load data
sequences, labels = [], []
for action in actions:
    for seq in range(30):
        window = []
        for frame in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(seq), f"{frame}.npy"))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

X = np.array(sequences)
y = to_categorical(labels).astype(int)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

# Build model
model = Sequential()
model.add(LSTM(64, return_sequences=False, activation='relu', input_shape=(30, X.shape[2])))
model.add(Dense(len(actions), activation='softmax'))

# Use categorical crossentropy since labels are one-hot
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Save model
model.save("gesture_model.h5")
print("✅ Model saved as gesture_model.h5")
