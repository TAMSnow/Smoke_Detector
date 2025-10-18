from ultralytics import YOLO
import cv2
import datetime

model = YOLO("..\\modelo_YOLO_cigarroV1\\best.pt") #estou utilizando o pytorch, mas tambem disponibilizei a versão em onnx na pasta modelo YOLO cigarro; 
#futuramente deve-se melhorar essa passagem de caminho do modelo, pois assim só funciona no windows.
#results = model.predict(source="0", show = True)

webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # esse cap_dshow é só pra windows, se trata do video source
webcam.set(3,640)
while(webcam.isOpened()):
    dataHoraAtual = str(datetime.datetime.now().replace(microsecond=0))
    ret, frame = webcam.read()
    if not ret:
        break

    resultados = model.predict(frame, conf=0.7, verbose=False)
    frameAnotado = resultados[0].plot()
    cv2.putText(frameAnotado, dataHoraAtual, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('camera', frameAnotado)


    if (cv2.waitKey(1) & 0xFF == ord('q')): # pressionar q para fechar a janela
        break

webcam.release()
cv2.destroyAllWindows()