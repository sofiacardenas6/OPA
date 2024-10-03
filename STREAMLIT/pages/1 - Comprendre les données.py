import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv("./data/20240423_PEA_stocks_info.csv")
choix = ["Pays", "Secteur", "Industrie", "Taille de l'entreprise", "Chiffre d'affaires"]
    

col1, col2, col3 = st.columns([2.5, 5, 2.5])
with col2:
    st.title("Comprendre les données")

    st.markdown("""
        <div style="font-size: 22px;">
        Analyser les données en fonction des variables <br>
        </div>
        """, unsafe_allow_html=True)

    #création de la liste déroutante
    option = st.selectbox("", choix)

    st.markdown(f"""
    <div style="font-size: 25px;text-align:center;">
    Répartition par 
        {option}<br>
    </div>
    """, unsafe_allow_html=True)

    #récupération des données en fonction de l'information demandée
    if option == choix[0]:
        data = df["country"].value_counts().sort_values(ascending=False)[0:10]
        labels = df["country"].value_counts().sort_values(ascending=False)[0:10].index
    elif option == choix[1]:
        data = df["sector"].value_counts().sort_values(ascending=False)[0:10]
        labels = df["sector"].value_counts().sort_values(ascending=False)[0:10].index
    elif option == choix[2]:
        data = df["industry"].value_counts().sort_values(ascending=False)[0:10]
        labels = df["industry"].value_counts().sort_values(ascending=False)[0:10].index
    elif option == choix[3]:
        df['fte_category'] = pd.cut(x = df['fullTimeEmployees'], bins = [1,20,250,5001,1000000], labels = ['TPE', 'PME', 'ETI', 'GE'], include_lowest = True)
        labels = list(df['fte_category'].value_counts().index)
        labels.append('not available')
        data = list(df['fte_category'].value_counts())
        data.append(df.shape[0] - df['fte_category'].value_counts().sum())

    #affichage des camenberts
    if option != choix[4]:
        fig = plt.figure()
        colors = sns.color_palette("pastel", len(labels))
        explode = [0.1 for i in range (0,len(labels))]
        plt.pie(data, labels=labels, colors=colors, autopct="%0.0f%%", explode = explode, labeldistance = 1.2)
        #text des graphiques en blanc
        for text in plt.gca().texts:
            text.set_color('black')
        st.pyplot(fig, transparent=True)

    #affichage du diagramme en bar
    if option == choix[4]:
        fig = plt.figure()
        MCbySector = df["marketCap"].groupby(df["sector"]).mean()
        ax = sns.barplot(x = MCbySector, y = MCbySector.index, palette = "pastel")
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        ax.set_xlabel('Capitalisation Boursière', color='black')
        ax.set_ylabel('Secteur', fontsize=14, color='black')
        st.pyplot(fig, transparent=True)


#affichage textes expliquatifs
text = ["Majorité des entreprises font partie de l'Europe",
"Principaux secteurs : la technologie, la santé et l'industrie.",
"Principales industries : la biotechnologie, les services immobiliers et les logiciels/applications.",
"Plupart sont des entreprises de tailles intermédiaires.",
"Secteurs rentables : énergie, des services financiers et des biens de consommations cycliques.",
]

st.markdown(f"""
    <div style="font-size: 25px;text-align:center;margin-top:1%">
        {text[choix.index(option)]}<br>
    </div>
    """, unsafe_allow_html=True)

