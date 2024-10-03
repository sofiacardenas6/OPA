import streamlit as st
import pandas as pd
import numpy as np



info = pd.read_csv("./data/20240423_PEA_stocks_info.csv")

historical = pd.read_csv("./data/AN8068571086_historical_market_data.csv")

cash_flow = pd.read_csv("./data/AN8068571086_cash_flow_data.csv")

balance_sheet = pd.read_csv("./data/AN8068571086_balance_sheet_data.csv")

financials = pd.read_csv("./data/AN8068571086_financials_data.csv")

new_df=pd.read_csv("./data/complete_processed_df_v4.csv")

col1, col2, col3 = st.columns([2.5, 5, 2.5])

with col2:
    st.title("Traitement des données")
    st.write(" ")
    st.write("Parmi les attributs disponibles pour chaque action, nous trouvons info, historical, cash_flow, balance_sheet et financials.")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("Données info")
    st.dataframe(info)
    st.markdown(" ")
    st.markdown("Exemple d'un fichier 'historical'")
    st.dataframe(historical)
    st.markdown(" ")
    st.markdown("Exemple d'un fichier 'cash_flow'")
    st.dataframe(cash_flow)
    st.markdown(" ")
    st.markdown("Exemple d'un fichier 'balance_sheet'")
    st.dataframe(balance_sheet)
    st.markdown(" ")
    st.markdown("Exemple d'un fichier 'financials'")
    st.dataframe(financials)
    st.markdown(" ")


    st.write("L’enjeu initial était de réunir les plus de 19 000 fichiers différents en un seul. Pour ce faire, nous avons utilisé différentes boucles et méthodes de concatenation.")
    st.write(" ")
    st.write("Étant donné l’objectif du projet, nous nous intéressons particulièrement au rendement annuel des actions. Cette quantité est donnée par")
    st.latex(r"\frac{valeur.finale + dividendes - valeur.initiale}{valeur.initiale}")
    st.write("Nous avons calculé ce rendement pour chaque entreprise pour les années 2020, 2021, 2022 et 2023.")
            
    st.write("Après un rigoureux nettoyage des données , nous avons obtenu le Data Frame suivant.")


    st.markdown("Data Frame Final")
    st.dataframe(new_df)

    st.write(" ")
    if st.checkbox("Afficher la dimension du Data Frame"):
        st.write(new_df.shape)




