import cv2
import time

def recognize_face():
    start_time = time.time()
    video = cv2.VideoCapture(0)
    face_detect = cv2.CascadeClassifier(r"Data\haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Data/Trainer.yml")
    namesList = ["", "Momina"]
    result = False
    id = -1 

    while True:
        ret, frame = video.read()
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detect.detectMultiScale(gray_image, 1.3, 5)

        for (x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray_image[y:y+h, x:x+w])
            if confidence < 50:
                name = namesList[id]
                result = True
            else:
                name = "Unknown"
                result = False

            cv2.putText(frame, name, (x, y-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) == ord("e"):
            break
        if time.time() - start_time > 20:
            break
        if result:
            break

    video.release()
    cv2.destroyAllWindows()
    
    print("User ID:", id)
    print("Recognition finished.")
    return result

# recognized = recognize_face()
# print("Face recognized ✅" if recognized else "Face not recognized ❌")
