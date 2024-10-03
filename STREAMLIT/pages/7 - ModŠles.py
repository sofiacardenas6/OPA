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

df_train = df_top10_return.loc['2018':'2022']
df_test = df_top10_return.loc['2023']

y = df_top10_return
X = pd.read_csv("./data/X_RL.csv")
X.set_index(X.iloc[:,0], inplace=True)
X.index = pd.to_datetime(X.index)
X = X.drop("Date", axis = 1)

predicList = pd.read_csv("./data/predict.csv")
predicList.set_index(predicList.iloc[:,0], inplace=True)
predicList.index = pd.to_datetime(predicList.index)
predicList = predicList.drop("Date", axis = 1)

choix = df_top10_return.columns
choix = [mot[2:len(mot)-7] for mot in choix]

#global predicts

#@st.cache_data
def runSarimax():
        entCpt = 0
        global predicts 
        predicts = []
        global courspred
        global date
        global courslog
        date = slider_value
        fig, axs = plt.subplots(taille, 2, figsize=(20,  taille * 5))
        for i in range(taille):
            for j in range(2):
                if entCpt < len(option) :
                    courslog = df_top10_return.filter(like = "C_"+ option[entCpt] + "_return")
                    courslog = courslog.loc[: (date - pd.DateOffset(days=1))]
                    affichage = df_top10_return.filter(like = "C_"+ option[entCpt]  + "_return")
                    model = sm.tsa.SARIMAX(courslog, order=(1, 1, 1), seasonal_order=(0, 1, 1, 12), freq='D')
                    sarima = model.fit()
                    pred = (sarima.predict(len(courslog), len(courslog) + 0))
                    pred_series = pd.DataFrame()
                    pred_series[courslog.columns[0]] = pred
                    courspred = pd.concat([affichage.loc[date - pd.DateOffset(months=1): date- pd.DateOffset(days=1)], pred_series])
                    predicts.append(pred)
                    if len(option)> 2 :
                        printSARIMAX(axs[i, j])
                        set_upModel(axs[i, j])
                    if len(option)< 3 :
                        printSARIMAX(axs[j])
                        set_upModel(axs[j])
                    entCpt += 1
                else :
                    if len(option)> 2 :
                        axs[i,j].set_visible(False)  
                    if len(option)< 3 :
                        axs[j].set_visible(False)  
        st.pyplot(fig, transparent=True)

#@st.cache_data
def runRL():
    fig, axs = plt.subplots(taille, 2, figsize=(20, taille * 5))
    cpt = 0
    global donnee
    global predictData
    for i in range(taille):
        for j in range(2):
            if cpt < len(option) :
                donnee = y.filter(like = "C_"+ option[cpt] + "_return")
                predictData = predicList.filter(like = "C_"+ option[cpt]  + "_return")
                if len(option)> 2 :
                    printRL(axs[i, j])
                    set_upModel(axs[i, j])
                if len(option)< 3 :
                    printRL(axs[j])
                    set_upModel(axs[j])
                cpt += 1 
            else :
                if len(option)> 2 :
                    axs[i,j].set_visible(False)  
                if len(option)< 3 :
                    axs[j].set_visible(False)  
    st.pyplot(fig, transparent=True)  

def set_upModel(axs):
    axs.tick_params(axis='both', colors='black')  
    axs.set_xlabel(axs.get_xlabel(), color='black')  
    axs.set_ylabel(axs.get_ylabel(), color='black')  
    axs.spines['bottom'].set_color('black')
    axs.spines['top'].set_color('black')
    axs.spines['right'].set_color('black')
    axs.spines['left'].set_color('black')

def printSARIMAX(axs):
    axs.plot(courspred) 
    axs.axvline(x=(date- pd.DateOffset(days=1)), color='red')
    axs.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    axs.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
    axs.set_xlim(pd.Timestamp(date - pd.DateOffset(months=1)), pd.Timestamp(date + pd.DateOffset(months=1)))
    axs.legend(['Observed', 'Predicted'])
    axs.set_title(courslog.columns[0], color='black')

def printRL(axs):
    axs.scatter(donnee.index, donnee, color='blue', label='Données')
    axs.plot(predictData.index, predictData, color='red', label='Régression linéaire')
    axs.legend(['Observed', 'Predicted'])
    axs.set_title(donnee.columns[0], color = 'black')


col1, col2, col3 = st.columns([1.5, 5, 1.5])
with col2:
    st.title("Modèles")
    st.markdown("""
        <div style="font-size: 25px;margin-bottom:5%">
        Nous allons maintenant appliquer nos modèles de prédictions: <strong>SARIMAX et Régression Linéaire</strong><br>
        </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 25px;">
    Choisissez une date à prédire avec le curseur :<br>
    </div>
    """, unsafe_allow_html=True)

    slider_value = st.slider("",
        min_value=datetime.date(2023, 1, 1),  
        max_value=datetime.date(2023, 12, 31), 
        value=datetime.date(2023, 1, 1)  
    )

    st.write("La valeur sélectionnée est :", slider_value)

    st.markdown("""
    <div style="font-size: 25px;">
    Choisissez une entreprise :<br>
    </div>
    """, unsafe_allow_html=True)
    option = st.multiselect("", choix)

    col1_, col2_ = st.columns([5, 5])
    with col2_:
    
        bouton = st.button('START')

    #si le bouton start a été appuyé
    if bouton :
        with st.spinner('Chargement en cours...'):
            col1_, col2_ = st.columns([5, 5])
            if len(option)%2 == 0:
                taille = int(len(option) / 2)
            else :
                taille = int((len(option) + 1) / 2)
            with col1_:
                #application du modèle SARIMAX
                st.markdown("""
                <div style="font-size: 22px;text-align:center">
                <strong>Modèle SARIMAX</strong> <br>
                </div>
                """, unsafe_allow_html=True)
                runSarimax()
            with col2_:
                #application du modèle de regression linéaire
                st.markdown("""
                <div style="font-size: 22px;text-align:center">
                <strong>Modèle de régression linéaire</strong> <br>
                </div>
                """, unsafe_allow_html=True)
                runRL()

            col1_, col2_ = st.columns([5, 5])
            with col1_:
                #affichage métrique pour le SARIMAX
                filtered_columns = [col for col in df_test.columns if any(keyword + "_return" in col for keyword in option)]
                df_filtered = df_test[filtered_columns]
                true_values = df_filtered.iloc[0:1].to_numpy().reshape(len(option), 1)
                maePred = round(mean_absolute_error(true_values, predicts), 3)
                r2Pred = round(r2_score(true_values, predicts),3)
                st.markdown("""
                <div style="font-size: 20px;text-align:center;"><strong>
                Mean Absolute Error:  """+ str(maePred)+""" <br>
                R2 score: """+ str(r2Pred) +""" </strong>
                </div>
                """, unsafe_allow_html=True)

            with col2_:
                filtered_columns = [col for col in y.columns if any(keyword + "_return" in col for keyword in option)]
                dataFilter = y[filtered_columns]
                predListFilter = predicList[filtered_columns]
                #affichage métrique pour la regression linéaire
                date = str(date)
                mae = round(mean_absolute_error(dataFilter.loc[date], predListFilter.loc[date]),3)
                r2 = round(r2_score(dataFilter.loc[date], predListFilter.loc[date]),3)

                st.markdown("""
                <div style="font-size: 20px;text-align:center;"><strong>
                Mean Absolute Error:  """+ str(mae)+""" <br>
                R2 score: """+ str(r2) +""" </strong>
                </div>
                """, unsafe_allow_html=True)
    


