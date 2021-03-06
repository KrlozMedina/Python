import cv2
import numpy as np

cap = cv2.VideoCapture(1) #, cv2.CAP_DSHOW)

redBajo = np.array([170, 30, 60], np.uint8)
redAlto = np.array([179, 100, 255], np.uint8)

colorCeleste = (255, 133, 82)
colorAmarillo = (89, 222, 255)
colorRosa = (128, 0, 255)
colorVerde = (0, 255, 36)
colorLimpiarPantalla = (29, 112, 246)

grosorCeleste = 6
grosorAmarillo = 2
grosorRosa = 2
grosorVerde = 2

grosorPeque = 6
grosorMedio = 1
grosorGrande = 1

color = colorCeleste
grosor = 3

x1 = None
y1 = None
imAux = None

while True:
    ret, frame = cap.read()
    if ret == False: break

    #frame = cv2.flip(frame, 1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if imAux is None:
        imAux = np.zeros(frame.shape, dtype = np.uint8)
    
    cv2.rectangle(frame, (0, 0), (50, 50), colorAmarillo, grosorAmarillo)
    cv2.rectangle(frame, (50, 0), (100, 50), colorRosa, grosorRosa)
    cv2.rectangle(frame, (100, 0), (150, 50), colorVerde, grosorVerde)
    cv2.rectangle(frame, (150, 0), (200, 50), colorCeleste, grosorCeleste)

    cv2.rectangle(frame, (300, 0), (400, 50), colorLimpiarPantalla, 1)
    cv2.putText(frame, 'Limpiar', (320, 20), 6, 0.6, colorLimpiarPantalla, 1, cv2.LINE_AA)
    cv2.putText(frame, 'pantalla', (320, 40), 6, 0.6, colorLimpiarPantalla, 1, cv2.LINE_AA)
    
    cv2.rectangle(frame, (490, 0), (540, 50), (0, 0, 0), grosorPeque)
    cv2.circle(frame, (515, 25), 3, (0, 0, 0), -1)
    cv2.rectangle(frame, (540, 0), (590, 50), (0, 0, 0), grosorMedio)
    cv2.circle(frame, (565, 25), 7, (0, 0, 0), -1)
    cv2.rectangle(frame, (590, 0), (640, 50), (0, 0, 0), grosorGrande)
    cv2.circle(frame, (615, 25), 11, (0, 0, 0), -1)
    
    maskRed = cv2.inRange(frameHSV, redBajo, redAlto)
    maskRed = cv2.erode(maskRed, None, iterations=1)
    maskRed = cv2.dilate(maskRed, None, iterations=2)
    maskRed = cv2.medianBlur(maskRed, 13)
    
    cnts, _ = cv2.findContours(maskRed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
    
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 1000:
            x, y2, w, h = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x, y2), (x+w, y2+h), (0, 255, 0), 2)
            x2 = x + w//2
            if x1 is not None:
                if 0 < x2 < 50 and 0 < y2 < 50:
                    color = colorAmarillo
                    grosorAmarillo = 6
                    grosorRosa = 2
                    grosorVerde = 2
                    grosorCeleste = 2
                if 50 < x2 < 100 and 0 < y2 < 50:
                    color = colorRosa
                    grosorAmarillo = 2
                    grosorRosa = 6
                    grosorVerde = 2
                    grosorCeleste = 2
                if 100 < x2 < 150 and 0 < y2 < 50:
                    color = colorVerde
                    grosorAmarillo = 2
                    grosorRosa = 2
                    grosorVerde = 6
                    grosorCeleste = 2
                if 150 < x2 < 200 and 0 < y2 < 50:
                    color = colorCeleste
                    grosorAmarillo = 2
                    grosorRosa = 2
                    grosorVerde = 2
                    grosorCeleste = 6
                if 490 < x2 < 540 and 0 < y2 < 50:
                    grosor = 3
                    grosorPeque = 6
                    grosorMedio = 1
                    GrosorGrande = 1
                if 540 < x2 < 590 and 0 < y2 < 50:
                    grosor = 7
                    grosorPeque = 1
                    grosorMedio = 6
                    GrosorGrande = 1
                if 590 < x2 < 640 and 0 < y2 < 50:
                    grosor = 11
                    grosorPeque = 1
                    grosorMedio = 1
                    GrosorGrande = 6
                if 300 < x2 < 400 and 0 < y2 < 50:
                    cv2.rectangle(frame, (300, 0), (400, 50), colorLimpiarPantalla, 2)
                    cv2.putText(frame, 'Limpiar', (320, 20), 6, 0.6, colorLimpiarPantalla, 2, cv2.LINE_AA)
                    cv2.putText(frame, 'pantalla', (320, 40), 6, 0.6, colorLimpiarPantalla, 2, cv2.LINE_AA)
                    imAux = np.zeros(frame.shape, dtype=np.uint8)
                if 0 < y2 < 60 or 0 < y1 < 60:
                    imAux = imAux
                else:
                    imAux = cv2.line(imAux, (x1, y1), (x2, y2), color, grosor)
            cv2.circle(frame, (x2, y2), grosor, color, 3)
            x1 = x2
            y1 = y2
        else:
            x1 = None
            y1 = None
            
    imAuxGray = cv2.cvtColor(imAux, cv2.COLOR_BGR2GRAY)
    _ , th = cv2.threshold(imAuxGray, 10, 255, cv2.THRESH_BINARY)
    thInv = cv2.bitwise_not(th)
    frame = cv2.bitwise_and(frame, frame, mask = thInv)
    frame = cv2.add(frame, imAux)
    
    cv2.imshow('frame', frame)
    cv2.imshow('imAux', imAux)
    cv2.imshow('th', th)
    cv2.imshow('thInv', thInv)
    cv2.imshow('markRed', maskRed)
    
    k = cv2.waitKey(1)
    if k == 27: break

cap.release()
cv2.destroyAllWindows()