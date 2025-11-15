from ultralytics import YOLO
import cv2
import datetime
from pathlib import Path
import registroPlanilha
import envioSeparado

# Devido o uso da biblioteca pathlib, agora o caminho para os arquivos funcionam em qualquer SO

#   para realizar registro
ultimo_registro = None
alerta = False
cont_registro = 0
cooldown = 60 # (segundos)
output_pasta = Path("fumantes") 
nome_csv = "registrosFumantes.csv"

output_pasta.mkdir(exist_ok=True) # se a pasta "fumantes" não existir, ela será criada 

model = YOLO((Path("modelo_YOLO_cigarroV6") / "best.pt")) #carrega o modelo, estou utilizando o pytorch

#capVideo = cv2.VideoCapture("fumantes_video.avi") #rodar a detecção no vídeo para testes

capVideo = cv2.VideoCapture(0, cv2.CAP_DSHOW) # rodar detecção na câmera conectada ao PC, caso tenha múltiplas câmeras e queira acessa-las, trocar 0 por 1, 2, 3...
#   ^^ esse cap_dshow é só pra windows, se trata do video source
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
    resultados = model.predict(frame, conf=0.55, iou= 0.2, verbose=False) # por meio de testes, esses parametros foram identificados como os melhores p esse modelo

    # Analisa TODAS as detecções do frame
    for resultado in resultados:
        for caixa in resultado.boxes:
            classe = model.names[int(caixa.cls[0])] # retorna pra variavel classe o que foi detectado no frame
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
            cv2.imwrite(output_pasta / f'fumante_{cont_registro}.jpg', frameAnotado)
            registroPlanilha.adicionar_registro(output_pasta / f'fumante_{cont_registro}.jpg', nome_csv, "cafeteria(placeholder)")
            envioSeparado.enviar_emails(dataHoraAtual, output_pasta / f'fumante_{cont_registro}.jpg')
            cont_registro+=1
            alerta = True

        # nao é o primeiro alerta, checar o cooldown e aí sim salvar 
        else:
            if((agora - ultimo_registro).total_seconds() > cooldown):
                cv2.imwrite(output_pasta / f'fumante_{cont_registro}.jpg', frameAnotado)
                registroPlanilha.adicionar_registro(output_pasta / f'fumante_{cont_registro}.jpg', nome_csv, "cafeteria(placeholder)")
                envioSeparado.enviar_emails(dataHoraAtual, output_pasta / f'fumante_{cont_registro}.jpg')
                ultimo_registro = agora
                cont_registro+=1


    # coloca data-hora por cima da exibição
    cv2.putText(frameAnotado, dataHoraAtual, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 250, 250), 2, cv2.LINE_AA)
    cv2.imshow('VideoShow', frameAnotado)


    if (cv2.waitKey(1) & 0xFF == ord('q')): # pressionar 'q' para fechar a janela, 0xFF padroniza a entrada da tecla digitada p/ todos SO e versões do openCV
        break

capVideo.release()
cv2.destroyAllWindows()