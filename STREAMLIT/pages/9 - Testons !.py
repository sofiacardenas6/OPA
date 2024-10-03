import streamlit as st
import pandas as pd
import datetime
import numpy as np

df_top10_filter = pd.read_csv("./data/dfInfo.csv")
df_top10_filter.set_index(df_top10_filter.iloc[:,0], inplace=True)
df_top10_filter.index = pd.to_datetime(df_top10_filter.index)
df_top10_filter = df_top10_filter.drop("Date", axis = 1)

predicList = pd.read_csv("./data/predict.csv")
predicList.set_index(predicList.iloc[:,0], inplace=True)
predicList.index = pd.to_datetime(predicList.index)
predicList = predicList.drop("Date", axis = 1)

col1, col2, col3 = st.columns([2.5, 5, 2.5])

moyPerf = 0
moyAlea = 0

coupleDate = []


choix = predicList.columns
choix = [mot[2:len(mot)-7] for mot in choix]

with col2:
    st.title("Testons")

    df=pd.read_csv("./data/20240423_PEA_stocks_info.csv")
    st.markdown("""
    <div style="font-size: 25px;">
    Le but est de savoir : <strong> Est-ce que notre modèle est plus
    intéressant que de l'hasard ? </strong> 
    <br>
    </div>
    """, unsafe_allow_html=True)

    entreprise_val = st.selectbox("Entrer le nom de l'entreprise:", choix)

    slider_value = st.slider("Choisir le nombre de transactions prises en compte",
    min_value=(0),  
    max_value=(30), 
    value=(10)  
    )
    st.write("La valeur sélectionnée est :", slider_value)

    
    col1_, col2_ = st.columns([5, 5])
    with col1_:


        #si on a bien rentré une valeur dans le champ de texte
        if (entreprise_val):
            #On récupere les informations de l'entreprise (rendement)
            entreprise = entreprise_val
            backTest = df_top10_filter.filter(regex = f"{entreprise}$")
            predReturn = predicList.filter(like = entreprise + "_return")
            backTest = pd.concat([backTest, predReturn], axis=1)

            quar3 = backTest.iloc[:, 3].describe().loc["75%"]
            quar1 = backTest.iloc[:, 3].describe().loc["25%"]

            #On récupère les dates avec le meilleur et le moins bon rendement
            high = backTest[backTest.iloc[:, 3] > quar3].sort_values(by=backTest.columns[3], ascending=False)
            low = backTest[backTest.iloc[:, 3] < quar1].sort_values(by=backTest.columns[3], ascending=True)

            #On prend les 50 meilleurs performances
            high = high[0:50]
            low = low[0:50]

            #fonction qui créee des couples de date pour creer une date d'achat et de vente
            def findDateBuySell(dataBuy, dataSell):
                for buy in dataBuy.index:
                    for sell in dataSell.index:
                        if buy < sell:
                            dateAchat = dataBuy.loc[str(buy)]
                            dateVente = dataSell.loc[str(sell)]
                            dateAchatI = pd.to_datetime(buy, format="%Y%m%d")
                            dateVenteI = pd.to_datetime(sell, format="%Y%m%d")
                            #st.write(dateAchat, dateVente, dateAchatI, dateVenteI)
                            break 
                    if buy < sell: 
                        return dateAchat, dateVente, dateAchatI, dateVenteI
                        break 
                    else:
                        return None, None, None, None

            #fonction qui calcule le rendement
            def getRendement(dataBuy, dataSell):
                rendement = ((dataSell[0] + dataBuy[2]) - dataBuy[0]) / dataBuy[0]
                return rendement
            #fonction qui fait la moyenne des moyennes avec tous les couples de date N
            def moyRendement(dataBuy, dataSell):
                rend = []
                coupleDate =  []
                for i in range (0, slider_value):
                    dateAchat, dateVente, dateAchatI, dateVenteI = findDateBuySell(dataBuy.sample(frac=1), dataSell.sample(frac=1))
                    if dateAchat is not None:
                        rend.append(getRendement(dateAchat, dateVente))
                        coupleDate.append([dateAchatI, dateVenteI])
                coupleDate = pd.DataFrame(coupleDate, columns=["Date d'Achat", "Date de Vente"])
                return np.mean(rend), coupleDate

            #get rendements moy en prenant en compte les meilleurs rendements prédits VS hasard
            moyPerf, coupleDatePerf = (moyRendement(high.sample(frac=1), low.sample(frac=1)))
            moyAlea, coupleDateAlea = (moyRendement(backTest.sample(frac=1), backTest.sample(frac=1)))

            st.dataframe((coupleDatePerf))
            with col2_:
                st.dataframe((coupleDateAlea))

    col1_, col2_ = st.columns([5, 5])
    with col1_:
            #affichage rendments moy avec les prédictions
            if pd.isna(moyPerf) == False :
                st.markdown("""
                <div style="font-size: 20px;text-align:center;"><strong>
                Moyenne du rendement pour les meilleurs performances en prenant en compte """ 
                + str(slider_value) + """ couples de dates: <strong>"""+ str(round((moyPerf),3))+""" </strong><br>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Pas assez de couples pour trouver une pair adéquate: Veillez augmenter son nombre")

            #affichage rendements moy hasard
            with col2_:
                if pd.isna(moyAlea) == False :
                    st.markdown("""
                    <div style="font-size: 20px;text-align:center;"><strong>
                    Moyenne du rendement avec le hasard en prenant en compte """ + str(slider_value) + 
                    """ couples de dates: <strong>"""+ str(round((moyAlea),3)) +""" </strong><br>
                    </div>
                    """, unsafe_allow_html=True)