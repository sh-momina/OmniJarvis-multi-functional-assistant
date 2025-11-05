import cv2
import numpy as np
from PIL import Image
import os

path = "Data/Valid_Users"
recognizer = cv2.face.LBPHFaceRecognizer_create()

def getImageId(path):
    Image_path = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for image in Image_path:
        face_image = Image.open(image).convert("L")
        faceNp = np.array(face_image) 
        id = (os.path.split(image)[-1].split(".")[1])
        faces.append(faceNp)
        ids.append(id)
        cv2.imshow("Training window ", faceNp)
        cv2.waitKey(1)
    return ids, faces

IDs, Faces = getImageId(path)
recognizer.update(Faces, np.array([int(i) for i in IDs]))
recognizer.save("Data/Trainer.yml")
cv2.destroyAllWindows()
print("Training complete ..... ")
