import cv2
import os

def area(event, x, y, flag, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cord[0] = (x, y)
        #print(cord)
    if event == cv2.EVENT_RBUTTONDOWN:
        cord[1] = (x, y)
        #print(cord)

dataPath = '/Users/krlozmedina/Documents/Proyectos/Python/DetectarRostros/DataFacial'    #MAC
# dataPath = 'C:/Users/camedina/Documents/Proyectos/Python/DataFacial'   #DELL
#dataPath = 'C:/Users/charl/OneDrive/Documents/Proyectos/Python/DetectarRostros/DataFacial' #ASUS
#dataPath = '/home/krlozmedina/Documentos/Proyectos/Python/DetectarRostros/DataFacial'   #Toshiba
imagePaths = os.listdir(dataPath)

face_recognizer = cv2.face.EigenFaceRecognizer_create()
face_recognizer.read('DetectarRostros/modelo.xml')
cap = cv2.VideoCapture(0)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cv2.namedWindow("frame")
cv2.setMouseCallback("frame", area)
cord = [(0, 0), (0, 0)]

while True:
    ret, frame = cap.read()
    if ret == False: break

    cv2.rectangle(frame, cord[0], cord[1], (255, 0, 0), 2)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()
    
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        if (cord[0] < (x, y) < cord[1]) and (cord[0] < (x+w, y+h) < cord[1]):
            rostro = auxFrame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame, '{}'.format(result), (x, y-5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

            if 0 < result[1] < 3500:
                cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.rectangle(frame, cord[0], cord[1], (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Desconocido', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.rectangle(frame, cord[0], cord[1], (0, 0, 255), 2)
            
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k==27: break

cap.release()
cv2.destroyAllWindows()