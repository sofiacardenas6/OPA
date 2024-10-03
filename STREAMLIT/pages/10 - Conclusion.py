import streamlit as st
import pandas as pd

col1, col2, col3 = st.columns([2, 5, 2])
with col2:
   st.title("Conclusion")

   st.markdown("""
   <div style="
                border: 5px solid  rgba(235, 159, 115, 0.5); 
                padding: 7%;
                margin-top: 10%;
                text-align:center;
                font-size: 32px">
   Rendement annuel 2023: Random Forest et Logistic Regression <br>
   Rendement journalier 2023: Regression Linéaire <br>
   Améliorations: Ajout de variables explicatives + modèles de classification pour le rendement journalier
   </div>
    """, unsafe_allow_html=True)