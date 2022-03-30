import cv2
import numpy as np

def dibujando(event, x, y, flags, param):
    if event == 1:
        print('--------------------')
        print('event= ', event)
        print('x= ', x)
        print('y= ', y)
        print('flags= ', flags)
        print('param= ', param)

cap = cv2.VideoCapture(0)
#imagen = np.zeros((480, 640, 3), np.uint8)
cv2.namedWindow("Imagen")
cv2.setMouseCallback("Imagen", dibujando)

while True:
    ret, frame = cap.read()
    if ret == False: break

    cv2.imshow("Imagen", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27: break