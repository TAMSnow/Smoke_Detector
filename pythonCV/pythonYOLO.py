from ultralytics import YOLO
import cv2
import datetime
import pandas as pd
model = YOLO("..\\modelo_YOLO_cigarroV6\\best.pt") #estou utilizando o pytorch
#futuramente deve-se melhorar essa passagem de caminho do modelo, pois assim só funciona no windows.

#   para realizar registro
registros = [] # essa lista será futuramente usada p registro em planilha via pandas
ultimo_registro = None
alerta = False
cont_registro = 0
cooldown = 10

#   codigo abaixo é para abrir a webcam e rodar o modelo nela
#webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # esse cap_dshow é só pra windows, se trata do video source
#webcam.set(3,640)
#   abrir video e rodar o modelo nele:
capVideo = cv2.VideoCapture("fumantes_video.avi")
while(capVideo.isOpened()):
    dataHoraAtual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ret, frame = capVideo.read()
    if not ret:
        break
    # reseta todas as detecções a cada frame
    pessoa_detectada = False
    cigarro_detectado = False
    fumando_detectado = False

    # procura pessoas, cigarros e fumantes em cada frame do vídeo:
    resultados = model.predict(frame, conf=0.6, iou= 0.3, verbose=False)

    # Analisa TODAS as detecções do frame
    for resultado in resultados:
        for caixa in resultado.boxes:
            classe = model.names[int(caixa.cls[0])]
            if classe == "Pessoa":
                pessoa_detectada = True
            elif classe == "Cigarro":
                cigarro_detectado = True
            elif classe == "Fumando":
                fumando_detectado = True

    # Só considera "fumante" se tiver os 3 elementos:
    fumante_detectado = (pessoa_detectada and cigarro_detectado and fumando_detectado)

    # .plot() rotula as coisas no vídeo para visualização
    frameAnotado = resultados[0].plot()

    # se tem fumante, salva o frame em jpg na pasta fumantes, mas verifica umas coisas antes
    if(fumante_detectado):
        agora = datetime.datetime.now()
        # se é o primeiro alerta, salvar sem checagem de cooldown
        if (not alerta):
            ultimo_registro = agora
            cv2.imwrite(f'fumantes\\fumante_{cont_registro}.jpg', frameAnotado)
            cont_registro+=1
            alerta = True
        # nao é o primeiro alerta
        else:
            print((agora - ultimo_registro).total_seconds())
            if((agora - ultimo_registro).total_seconds() > cooldown):
                cv2.imwrite(f'fumantes\\fumante_{cont_registro}.jpg', frameAnotado)
                ultimo_registro = agora
                cont_registro+=1

    cv2.putText(frameAnotado, dataHoraAtual, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 250, 250), 2, cv2.LINE_AA)
    cv2.imshow('VideoShow', frameAnotado)


    if (cv2.waitKey(1) & 0xFF == ord('q')): # pressionar q para fechar a janela
        break

capVideo.release()
cv2.destroyAllWindows()