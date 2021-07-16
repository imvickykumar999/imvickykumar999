
import cv2

# input_image = input("\nEnter Image name : ")
# img = cv2.imread(input_image)

def plate():
    img = cv2.imread('image/croped car.jpeg')
    face_cascade = cv2.CascadeClassifier('files/carplate.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    count=0
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # cv2.imshow('img', img)
        roi = img[y:y+h, x:x+w]
        # cv2.imshow('img1', roi)

        count+=1
        cv2.imwrite(f"image/plate{count}.png", roi)
        # cv2.waitKey(1000) # 1 sec = 1000 ms

    return len(faces)

    # Destroying present windows on screen
    # cv2.destroyAllWindows()
