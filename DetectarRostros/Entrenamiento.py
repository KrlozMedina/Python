import cv2
import os
import numpy as np

#dataPath = 'C:/Users/krlozmedina/Documents/Proyectos/Python/DataFacial'    #MAC
# dataPath = 'C:/Users/camedina/Documents/Proyectos/Python/DataFacial'   #DELL
dataPath = 'C:/Users/charl/OneDrive/Documents/Proyectos/Python/DetectarRostros/DataFacial' #ASUS
peopleList = os.listdir(dataPath)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir

    for fileName in os.listdir(personPath):
        labels.append(label)
        facesData.append(cv2.imread(personPath + '/' + fileName, 0))
        image = cv2.imread(personPath + '/' + fileName, 0)
        #cv2.imshow('image', image)
        #cv2.waitKey(10)
    label = label + 1

#print('labels= ', labels)
#print('Numero de etiquetas 0: ', np.count_nonzero(np.array(labels)==0))

#cv2.destroyAllWindows

face_recognizer = cv2.face.LBPHFaceRecognizer_create() #pip install opencv-contrib-python
print("Entrenando...")
face_recognizer.train(facesData, np.array(labels))

face_recognizer.write('DetectarRostros/modelo.xml')
print("Modelo almacenado...")