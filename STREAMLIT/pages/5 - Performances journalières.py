import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

col1, col2, col3 = st.columns([2.5, 5, 2.5])

with col2:
    st.title("Performances journalières")
    st.markdown("""
    <div style="font-size: 22px;">
    Analyser les performances journalières avec les times series.<br>
    Time series : Données chronologiques où
    chaque valeur est lié à une date.<br>
    Pour analyser les series temporelles, il faut "décomposer la série". <br> <br>
    La décomposer sépare la série en plusieurs composants: <br><br>
    </div>
    """, unsafe_allow_html=True)

    col1_, col2_ = st.columns([5, 5])
    with col1_:
        st.markdown("""
        <div style="font-size: 20px;text-align:center;">
        Série d'origine
        </div>
        """, unsafe_allow_html=True)
    with col2_:
        st.markdown("""
        <div style="font-size: 20px;text-align:center;">
        Orientation générale de la série, 
        l'évolution les données
        </div>
        """, unsafe_allow_html=True)

    st.image("./images/decomposition_series_temporielle.png", use_column_width=True) 

    col1_, col2_ = st.columns([5, 5])
    with col1_:
        st.markdown("""
        <div style="font-size: 20px;text-align:center;">
        Variations périodiques de la série. <br> Additive : valeurs constantes. <br>
        Multiplicative : valeurs qui augmentent au fil du temps
        </div>
        """, unsafe_allow_html=True)
    with col2_:
        st.markdown("""
        <div style="font-size: 20px;text-align:center;">
        Partie aléatoire de la série
        </div>
        """, unsafe_allow_html=True)