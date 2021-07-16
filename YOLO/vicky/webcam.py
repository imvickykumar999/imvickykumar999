import numpy as np
import cv2, time

def save_car(para = 0):

    confidenceThreshold = 0.5
    NMSThreshold = 0.3

    modelConfiguration = 'files/yolov3.cfg'
    modelWeights = 'files/yolov3.weights'
    labelsPath = 'files/coco.names'

    labels = open(labelsPath).read().strip().split('\n')
    np.random.seed(10)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    outputLayer = net.getLayerNames()
    outputLayer = [outputLayer[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # video_capture = cv2.VideoCapture(0)
    video_capture = cv2.VideoCapture(para)
    (W, H) = (None, None)

    while True:
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        if W is None or H is None:
            (H,W) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB = True, crop = False)
        net.setInput(blob)
        layersOutputs = net.forward(outputLayer)

        boxes = []
        confidences = []
        classIDs = []

        for output in layersOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > confidenceThreshold:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY,  width, height) = box.astype('int')
                    x = int(centerX - (width/2))
                    y = int(centerY - (height/2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)
        if(len(detectionNMS) > 0):
            for i in detectionNMS.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                a,b,c,d = x,y,w,h
                detected = labels[classIDs[i]]
                try:
                    if detected == 'car':
                        a,b,c,d = x,y,w,h
                        if cv2.imwrite('input.jpg', frame[b:b+d, a:a+c]):
                            print('\nCropped Car Image Saved...')
                            return True
                except:
                    pass

                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow('Press Space to Exit...', frame)
        if(cv2.waitKey(1) & 0xFF == ord(' ')):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# para = 0
# para = 'http://192.168.1.114:8080/video'
# save_car(para)
