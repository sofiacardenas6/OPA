import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose 
import statsmodels.api as sm

#récupération du dataset des données de rendement
df_top10_return=pd.read_csv("./data/dfInfo_return.csv")

#affichage des entreprises nom court
choix = df_top10_return.columns[1::]
choix = [mot[2:len(mot)-7] for mot in choix]

col1, col2, col3 = st.columns([1.5, 5, 1.5])
with col2:
    st.title("Analyser des données")
    st.markdown("""
    <div style="font-size: 30px;text-align:center;margin-top:15%;"> <br>
    </div>
    """, unsafe_allow_html=True)

    #explication sur l'analyse des données
    col1_, col2_, col3_ = st.columns([2, 13, 2])
    with col1_:
        st.markdown(
            """
            <style>
            .dataframe-table {
                margin-left: auto;
                margin-right: auto;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )
        st.write("<div class='dataframe-table'>", unsafe_allow_html=True)
        st.dataframe(choix)
        st.write("</div>", unsafe_allow_html=True)
    with col2_:
        st.image("./images/entrepriseV8.png", use_column_width=True) 

    with col3_:
        st.markdown("""
        <div style="font-size: 20px;text-align:center;border: 2px solid black;
        margin-left:auto;margin-right:auto;padding-left:5%;padding-right:5%;padding-bottom:40%;"> <br><br><br>
        Recherches externes font ressortir plusieurs points: <br><br>
        <strong>
        Majorité des entreprises les plus performantes sont des banques scandinaves
        </div>
        """, unsafe_allow_html=True)

    #explication de la création du dataframe
    st.markdown("""
    <div style="font-size: 25px;text-align:center;border: 2px solid white;margin-bottom:5%;margin-top:30%;"> <br>
    Récupérons les données suivantes pour les 10
    entreprises les plus performantes: <br><strong>
     Fermeture du cours <br>
     Ouverture du cours <br>
     Dividende du cours <br>
     </strong>
    Objectif : Calculer le rendement journalier <br><br>
    </div>
    """, unsafe_allow_html=True)
    st.image("./images/recupV4.png", use_column_width=True) 

    st.markdown("""
    <div style="font-size: 30px;text-align:center;margin-top:20%"> <br>
    Pour une analyse approfondie des données, nous pouvons effectuer
    une décomposition de la série. <br><br>
    Décompositon de la série pour les 10 entreprises:<br><br>
    </div>
    """, unsafe_allow_html=True)

    #partie sur la décomposition de la série
    option = st.selectbox("", choix)
    text = ["""Return oscillant de -10 à 10%. 
        Tendance qui chute en fin 2019 et en fin 2021.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -20 à 15%. 
        Tendance qui chute en fin 2019 et en fin 2021.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -10 à 18%. 
        Tendance qui chute en fin 2019 et en fin 2021.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -12 à 14%. 
        Tendance qui chute en fin 2019 et en début 2021.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -20 à 45%. 
        Tendance qui chute en fin 2019 et en début 2022.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -7 à 10%. 
        Tendance qui chute en fin 2019 et en fin 2021.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -10 à 10%. 
        Tendance qui chute en fin 2019 et en fin 2021.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -5 à 18%. 
        Tendance qui est stable de 2018 à 2022 et qui chute en fin 2022.
        6 périodes de 2018 à 2023.
        Peu de résidu""",

        """Return oscillant de -10 à 28%. 
        Tendance qui augmente de 2018 à 2021 et qui chute en début 2022.
        6 périodes de 2018 à 2023.
        Peu de résidu""",
        
        """Return oscillant de -7 à 12%. 
        Tendance qui augmente de 2018 à 2021 et qui chute en fin 2021.
        6 périodes de 2018 à 2023.
        Peu de résidu"""]
        
    #affichage des explications avec les graphiques
    col1_, col2_ = st.columns([5, 2])
    with col1_:
        if option == "BMW" :
            st.image("./images/C_BMW_return.jpg", width = 900) 
        else :
            name = df_top10_return.filter(like = option).columns[0]
            name = name.replace("/","")
            st.image("./images/"+ name +".jpg", width = 900) 

    with col2_:
        st.markdown("""
        <div style="font-size: 25px;text-align:center; border: 2px solid black; padding-left:5%; padding-right:5%; padding-top:48%; padding-bottom:48%"> 
        """+ text[choix.index(option)] +"""
        </div>
        """, unsafe_allow_html=True)
       


    