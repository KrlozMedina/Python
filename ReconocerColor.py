import cv2
import numpy as np

def dibujar(mask, color, c1, c2, cord):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[c1:c2]
    
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if (M["m00"] == 0) : M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            if cord is None:
                cord = (x, y)
            cv2.circle(frame, (x, y), 5, color, -1)
            #cv2.putText(frame, '{}, {}'.format(x, y), (x+10, y), font, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
            #cv2.putText(frame, str(cord), (x+10, y), font, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
            #if color != (0, 0, 0):
                #cv2.drawContours(frame, [nuevoContorno], 0,  color, 3)
    return cord
            
            
def linea(frame, imAux, mask, color, x1, y1):
    if imAux is None:
        imAux = np.zeros(frame.shape, dtype = np.uint8)
        
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.medianBlur(mask, 13)    
    
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
    
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(c)
            x2 = x + round(w/2)
            y2 = y + round(h/2)
            if x1 is not None:
                imAux = cv2.line(imAux, (x1, y1), (x2, y2), color, 3)
            x1 = x2
            y1 = y2
            
    imAuxGray = cv2.cvtColor(imAux, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(imAuxGray, 10, 255, cv2.THRESH_BINARY)
    thInv = cv2.bitwise_not(th)
    frame = cv2.bitwise_and(frame, frame, mask = thInv)
    frame2 = cv2.add(frame, imAux)
    
    return (frame2, imAux, x1, y1)

cap = cv2.VideoCapture(0)

naranjaBajo = np.array([0, 100, 190], np.uint8)
naranjaAlto = np.array([20, 255, 255], np.uint8)

azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

amarilloBajo = np.array([15, 100, 20], np.uint8)
amarilloAlto = np.array([45, 255, 255], np.uint8)

verdeBajo = np.array([55, 20, 20], np.uint8)
verdeAlto = np.array([65, 255, 255], np.uint8)

laserBajo = np.array([150, 20, 20], np.uint8)
laserAlto = np.array([179, 255, 155], np.uint8)

redBajo1 = np.array([0, 10, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)

redBajo2 = np.array([170, 10, 20], np.uint8)
redAlto2 = np.array([179, 100, 255], np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX

x1 = None
y1 = None
imAux = None
cordNaranja = None
cordAzul = None
cordAmarillo = None
cordVerde = None

while True:
    ret, frame = cap.read()
    
    if ret == True:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        maskNaranja = cv2.inRange(frameHSV, naranjaBajo, naranjaAlto)
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
        maskVerde = cv2.inRange(frameHSV, verdeBajo, verdeAlto)
        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
        maskRed = cv2.add(maskRed1, maskRed2)
        maskLaser = cv2.inRange(frame, laserBajo, laserAlto)
        
        cordNaranja = dibujar(maskNaranja, (0, 128, 255), 1, 4, cordNaranja)
        cordAzul = dibujar(maskAzul, (255, 0, 0), 0, 2, cordAzul)
        cordAmarillo = dibujar(maskAmarillo, (0, 255, 255), 0, 2, cordAmarillo)
        cordVerde = dibujar(maskVerde, (0, 255, 0), 0, 2, cordVerde)
        
        frame, imAux, x1, y1 = linea(frame, imAux, maskRed2, (0, 0, 255), x1, y1)
        
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
        
cap.release()
cv2.destroyAllWindows()