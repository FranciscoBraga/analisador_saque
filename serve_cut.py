import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import os
import pickle

# Configuração do MediaPipe (API Clássica/Solutions)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
test_hands = mp.solutions.hands
out = None

file_name = "serve/kyrgios.mp4"
cap = cv2.VideoCapture(file_name)
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
seconds = 4

frames = deque(maxlen=fps*seconds)
landmarks_frames = deque(maxlen=fps*seconds)
min_visibility = 0.9
post_condition3_frames = 0
current_frame = 0
condition1_meet = condition2_meet = condition3_meet = False
saque_count = 0

# Inicializa o módulo de Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # O MediaPipe usa RGB, o OpenCV usa BGR. Precisamos converter.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = True # Melhora performance
        
        # --- A MÁGICA ACONTECE AQUI ---
        results = pose.process(image)
        # ------------------------------

        # Converte de volta para BGR para desenhar na tela
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Desenha os pontos (landmarks) se encontrou algo
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS
            )

            #liSTAS DE PONTOS
            landmarks = results.pose_landmarks.landmark
           # wrist_visible = pose[mp_pose.PoseLandmark.LEFT_WRIST] > min_visibility
            frames.append(image.copy())
            landmarks_frames.append(results.pose_landmarks)
           

            wrist_visible = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].visibility > min_visibility
            elbow_visible = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].visibility > min_visibility
            shoulder_visible = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].visibility > min_visibility

            #print(f"Pulso: {wrist_visible}, Cotovelo: {elbow_visible}, Ombro: {shoulder_visible}")
            if wrist_visible and landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y < landmarks[mp_pose.PoseLandmark.NOSE].y:
                condition1_meet = True
            
            if condition1_meet and elbow_visible and landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y < landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y:
                condition2_meet = True

            if condition2_meet and elbow_visible and landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y > landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y:
                condition3_meet = True

            if condition3_meet == True:
                post_condition3_frames +=1

            if condition1_meet and condition2_meet and condition3_meet and out is None:
                print("estou aqui")
                h, w, _ = image.shape
                saque_count += 1
                out = cv2.VideoWriter(f'{file_name.split(".")[0]}_{saque_count}.mp4',fourcc,fps,(w,h))

            if out is not None:
                if post_condition3_frames >=fps *2:

                    while not len(frames)==0:
                        out.write(frames.popleft())
                    
                    out.release()
                    out = None
                    print(f"Saque {saque_count} salvo")
                    condition1_meet = condition2_meet = condition3_meet = False
                    post_condition3_frames = 0

        cv2.imshow("tela", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()