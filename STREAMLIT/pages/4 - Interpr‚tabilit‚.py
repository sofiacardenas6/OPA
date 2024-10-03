import streamlit as st
import pandas as pd
import numpy as np


col1, col2, col3 = st.columns([2.5, 5, 2.5])

with col2:
    st.title("Interprétabilité")

    st.write(" ")
    st.write("Nous portons une attention particulière aux modèles Random Forest Regressor et Logistic Regression, qui semblent être les plus performants parmi tous les modèles de régression et de classification, respectivement.")
    st.write(" ")
    st.write("Avec bibliothèque SHAP de Python, nous sommes en mesure d'évaluer si notre modèle est influencé de manière biaisée par certaines variables. Un graphique SHAP montre l'impact de chaque caractéristique sur les prédictions d'un modèle. La position des points indique le poids de chaque feature, tandis que la couleur représente la valeur de cette caractéristique.")
    st.write(" ")
    st.write("Random Forest Regressor")
    st.image("images/RandomForestRegressor.png", width=600)

    st.write("Logistic Regression")
    st.image("images/LogisticRegression.png", width=620)

    st.write("La majorité des variables identifiées sont d'ordre financier et pourraient raisonnablement affecter la performance boursière d'une entreprise. Nous n'observons pas d'impact suffisamment significatif pour conclure que ces modèles présentent un biais.")
