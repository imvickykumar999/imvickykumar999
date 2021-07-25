import cv2, os
path = os.path.join('C:\\Users', os.getlogin(), 'Desktop', 'Camera Webcam IP')

cap, count = cv2.VideoCapture(0), 1
# cap, count = cv2.VideoCapture('http://192.168.0.65:8080/video'), 1

if not os.path.exists(path):
    os.mkdir(path)
if(cap.isOpened()):
    again = '1'
    while again is '1':
        again = input('Press 1 to CLICK photo : ')
        ret, face = cap.read()
        file_name_path = path + '/count' + str(count) + ' .jpg'
        cv2.imwrite(file_name_path, face)
        count += 1
else: print('\nWebCam is failed to use')
cap.release()
cv2.destroyAllWindows()
input('\nThanks 4 Using Camera... Press ENTER to EXIT')
