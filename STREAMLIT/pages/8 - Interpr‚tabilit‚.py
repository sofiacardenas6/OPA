import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import statsmodels.api as sm
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
import shap
import io

#inport et traitement des df
df_top10_return=pd.read_csv("./data/dfInfo_return.csv")
df_top10_return.set_index(df_top10_return.iloc[:,0], inplace=True)
df_top10_return.index = pd.to_datetime(df_top10_return.index)
df_top10_return = df_top10_return.drop("Date", axis = 1)

y = df_top10_return
X = pd.read_csv("./data/X_RL.csv")
X.set_index(X.iloc[:,0], inplace=True)
X.index = pd.to_datetime(X.index)
X = X.drop("Date", axis = 1)


X = X.filter(like = "C_BMW_return")
y = y.filter(like = "C_BMW_return")


col1, col2, col3 = st.columns([2, 5, 2])
with col2:
    st.title("Interprétabilité")

    st.markdown("""
        <div style="font-size: 25px;margin-bottom:10%">
        </div>
            """, unsafe_allow_html=True)


    st.subheader("Exemple d'interprétabilité pour le modèle de regression linéaire:")

    model = LinearRegression()
    model.fit(X, y)
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    #shap.summary_plot(shap_values, X)
    fig =  plt.figure(figsize=(10, 6)) 
    shap.summary_plot(shap_values, X, show=False) 
    st.pyplot(fig, transparent=True)

col1, col2, col3 = st.columns([2, 5, 2])
with col2:
    st.markdown("""
        <div style="font-size: 25px;margin-top:5%;text-align:center">Moyenne mobile a plus d'impact 
        positif comme négatif sur la prédiction du rendement<br>
        Moyenne positve == rendement postif<br>
        Moyenne négative == rendement négatif
        </div>
            """, unsafe_allow_html=True)



