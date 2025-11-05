import cv2

count = 0
video = cv2.VideoCapture(0)
face_detect = cv2.CascadeClassifier("Data\haarcascade_frontalface_default.xml")
id = float(input("Enter your id (id must be > " + str(count) + " ) : "))


while True:
    ret, frame = video.read()
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces= face_detect.detectMultiScale(gray_image, 1.3, 5)
    for (x,y,w,h) in faces:
        count += 1
        cv2.imwrite('Data/Valid_Users/User.' + str(id) + "." + str(count) + ".jpg", gray_image[y:y+h , x:x+w])
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
    cv2.imshow("Face Recognition", frame)
    
    k = cv2.waitKey(1)
    if count > 1000:
        break
    
video.release()
cv2.destroyAllWindows()
print("Dataset collected ......")
