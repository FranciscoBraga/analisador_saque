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

file_name = "serve/01-24_1_1.mp4"
cap = cv2.VideoCapture(file_name)
fps = int(cap.get(cv2.CAP_PROP_FPS))
seconds = 4

frames = deque(maxlen=fps*4)
landmarks_frames = deque(maxlen=fps*seconds)
min_visibility = 0.9

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
        image.flags.writeable = False # Melhora performance
        
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

            landmarks = results.pose_landmarks.landmark
           # wrist_visible = pose[mp_pose.PoseLandmark.LEFT_WRIST] > min_visibility
            
           

        cv2.imshow("tela", image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()