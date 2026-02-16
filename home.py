import streamlit as st
import os
import cv2
import pickle
import mediapipe as mp
import numpy as np


st.set_page_config(layout="wide")

if "idx" in st.session_state:
    st.session_state.idx = 0
if "idx2" in st.session_state:
    st.session_state.idx2 = 0
if "is_playing" in st.session_state: 
    st.session_state.is_playing= False
 

def draw_sidebar(landmarks, landmarks2):
    expander_frame = st.sidebar.expander("🎛️ Frame Controller", True)
    slider_play =  expander_frame.empty()
    slider_play2 = expander_frame.empty()
    col1, col2 = expander_frame.columns(2)
    col3,col4 = st.sidebar.columns(2)


    if col1.button("-1"):
        st.session_state.idx = st.session_state.idx - 1 if st.session_state.idx > 0 else 0
    if col2.button("+1"):
        st.session_state.idx = st.session_state.idx + 1 if st.session_state.idx < len(landmarks) else st.session_state.idx
    if col1.button("-1 R"):
        st.session_state.idx2 = st.session_state.idx2 - 1 if st.session_state.idx2 > 0 else 0
    if col2.button("+1 R"):
        st.session_state.idx2 = st.session_state.idx2 + 1 if st.session_state.idx2 < len(landmarks2) else st.session_state.idx2
      
    if col1.button("⏪ Voltar"):
        st.session_state.is_playing = False
        st.session_state.idx = st.session_state.idx - 1 if st.session_state.idx > 0 else 0
        st.session_state,idx2 = st.session_state,idx2 -1 if st.session_state.idx2 > 0 else 0

    if col1.button("⏩ Avançar"):
        st.session_state.is_playing = False
        st.session_state.idx = st.session_state.idx + 1 if st.session_state.idx < len(landmarks) else st.session_state.idx
        st.session_state.idx2 = st.session_state.idx2 + 1 if st.session_state.idx2 < len(landmarks2) else st.session_state.idx2

    if col3.button("▶️ Play"):
        st.session_state.is_playing = True
    if col4.button("⏸️ Pause"):
        st.session_state.is_playing = False

    st.session_state.idx =  slider_play.slider("Video 1",0,len(landmarks)-1,st.session_state.idx)
    st.session_state.idx2 =  slider_play2.slider("Video 2",0,len(landmarks2)-1,st.session_state.idx2)


