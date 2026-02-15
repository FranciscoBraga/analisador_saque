import cv2
import numpy as np
import pickle
import os


filename = "serve/kyrgios_1.mp4"

intervalo_baixo = np.array([30,50,166])
intervalo_alto = np.array([40,200,255])

list_balls = []

if not os.path.exists(filename):
    print(f"Erro: Arquivo '{filename}' não encontrado|")
else:
    cap = cv2.VideoCapture(filename)
    #pega o FPS do vídeo original
    fps = cap.get(cv2.CAP_PROP_FPS)

    #CALCULA O ATRASO EM MILISEGUDOS (1000MS/FPS)
    #SE O FPS FOR 30, O DELAY SERÁ ~33MS
    delay = int(1000/fps) if fps > 0 else 30

    
    if not cap.isOpened():
        print("Erro ao abrir o arquivo de video.")
    else:
        while cap.isOpened():
            ret,frame =cap.read()

            if not ret:
                print("Fim do vídeo ou erro na leitura do frame.")
                break

            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            mascara = cv2.inRange(hsv,intervalo_baixo, intervalo_alto)
            contornos, _ = cv2.findContours(mascara,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            conts = []

            for contorno in contornos:
                (x,y), raio = cv2.minEnclosingCircle(contorno)
                centro = (int(x),int(y))
                raio = int(raio)

                if raio > 5 and y < 0.5 * frame.shape[0]:
                    cv2.circle(frame,centro, raio,(0,255,0),2)
                    conts += [centro]

            list_balls += [conts]


            cv2.imshow('Deteccao da Bolinha de Tenis',frame)  
           # cv2.imshow('Deteccoo da Bolinha de Tenis',frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()