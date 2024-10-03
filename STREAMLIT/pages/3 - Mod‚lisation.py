import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import shap
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import mean_absolute_error, confusion_matrix
from sklearn.linear_model import Lasso, Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


def prediction(modele):

    modele = joblib.load("./modèles/"+modele)
    
    return modele
  
st.title("Modélisation du Rendement Annuel")

new_df=pd.read_csv("./data/complete_processed_df_v4.csv")

isins = new_df['isin']
short_names = new_df['shortName']
returns = new_df['return']

new_df.drop(['isin','shortName'], axis = 1, inplace = True)

st.subheader(" ")

type_modele = st.selectbox('Type de modèle', ('Régression', 'Classification'))

if type_modele=='Régression':

    st.subheader("Modèles de Régression")
    st.write(" ")

    columns_to_scale = new_df.drop(columns=['year', 'return', 'sector', 'country', 'quoteType', 'recommendationKey']).columns
    columns_to_exclude = ['year', 'return', 'quoteType', 'recommendationKey']
    new_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    new_df.fillna(new_df.mean(), inplace=True)
    scaler = StandardScaler()
    data = new_df
    data[columns_to_scale] = scaler.fit_transform(new_df[columns_to_scale])
    X_train = data[data['year'] != 2023]
    y_train = X_train['return']
    X_train = X_train.drop(['year','return'], axis=1)
    X_test = data[data['year'] == 2023]
    y_test = X_test['return']
    X_test = X_test.drop(['year','return'], axis=1)


    st.markdown('**Sélection du modèle**')
    choix = ['Lasso', 'Ridge', 'Random Forest Regressor']
    option = st.radio('Choisissez un modèle', choix)

    


    modele = prediction(option)
    y_pred = modele.predict(X_test)
    st.write(" ")
    st.markdown("**Scores**")
    st.write('mae:', np.round(mean_absolute_error(y_test, y_pred),2))
    st.write('R2:', np.round(modele.score(X_test, y_test),2))
    
    st.write(" ")
    if st.checkbox("Afficher les hyperparamètres du modèle") :
        st.write(modele.get_params())
    
    st.write(" ")
    st.markdown('**Comparatif**')
    st.image("./images/Régression.png", width = 700)


    

    predictions = pd.DataFrame(modele.predict(X_test), columns = ['return prédit'])

    isins_test = isins[y_test.index]
    short_names_test = short_names[y_test.index]
    returns_test = returns[y_test.index]

    isins_test = pd.DataFrame(np.array(isins_test), columns = ['isin'])
    short_names_test = pd.DataFrame(np.array(short_names_test), columns = ['shortName'])
    returns_test = pd.DataFrame(np.array(returns_test), columns = ['return'])

    predictions = predictions.join(isins_test, how = 'right')
    predictions = predictions.join(short_names_test, how = 'right')
    predictions = predictions.join(pd.DataFrame(np.array(returns_test), columns = ['return']), how = 'right')
    
    st.write(" ")
    st.markdown('**Construissons un portefeuille à partir de ce modèle**')
    option = st.slider("Nombre d'entreprises composant le portefeuille", 1, 100)

    predictions1 = predictions.sort_values('return prédit', ascending = False).head(option)

    st.write("Rendement prédit (par rapport au marché:)", np.round(predictions1['return prédit'].mean()*100,2),"%")
    st.write("Rendement réel (par rapport au marché:)", np.round(predictions1['return'].mean()*100,2),"%")

    st.write(" ")
    st.write("Top", option, "entreprises sélectionées par le modèle")

    
    st.dataframe(predictions1.drop(['return prédit','return'],axis=1))




elif type_modele=='Classification':
    st.subheader("Modèles de Classification")
    st.write(" ")

    new_df['classification'] = new_df['return']
    bins = [-np.inf, 0, np.inf]
    labels = [0, 1] # 0 étant perte et 1 étant gain
    new_df['classification'] = pd.cut(new_df['classification'], bins=bins, labels=labels)
    columns_to_scale = new_df.drop(columns=['year', 'return', 'sector', 'country', 'classification']).columns
    new_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    scaler = StandardScaler()
    data = new_df
    data[columns_to_scale] = scaler.fit_transform(new_df[columns_to_scale])
    X_train = data[data['year'] != 2023]
    y_train = X_train['classification']
    X_train = X_train.drop(['year','return','classification'], axis=1)
    X_train.fillna(X_train.mean(), inplace=True)

    X_test = data[data['year'] == 2023]
    y_test = X_test['classification']
    X_test = X_test.drop(['year','return','classification'], axis=1)
    X_test.fillna(X_test.mean(), inplace=True)


    st.markdown('**Sélection du modèle**')
    choix_clf= ['Random Forest Classifier', 'SVC', 'KNN', 'Logistic Regression']
    option_clf = st.radio('Choisissez un modèle', choix_clf)

    modele = prediction(option_clf)
    y_pred = modele.predict(X_test)
    st.write(" ")
    st.markdown("**Métriques**")
    st.write('score:', np.round(modele.score(X_test, y_test),2))
    st.write('Matrice de Confusion:', confusion_matrix(y_test, y_pred))

    st.write("La classe 0 représente un rendement en-dessous du marché et la classe 1 représente un rendement au-dessus du marché")

    st.write(" ")
    if st.checkbox("Afficher les hyperparamètres du modèle") :
        st.write(modele.get_params())

    st.write(" ")
    st.markdown('**Comparatif**')
    st.image("Images/Classification.png", width = 800)


    st.write(" ")
    st.markdown('**Construissons un portefeuille à partir de ce modèle**')

    isins_test = isins[y_test.index]
    short_names_test = short_names[y_test.index]
    returns_test = returns[y_test.index]

    isins_test = pd.DataFrame(np.array(isins_test), columns = ['isin'])
    short_names_test = pd.DataFrame(np.array(short_names_test), columns = ['shortName'])
    returns_test = pd.DataFrame(np.array(returns_test), columns = ['return'])


    probas = modele.predict_proba(X_test)
    probas = pd.DataFrame(probas, columns = ['proba_perte', 'proba_gain'])
    probas = probas.join(isins_test, how = 'left')
    probas = probas.join(short_names_test, how = 'left')
    probas = probas.join(pd.DataFrame(np.array(y_test), columns = ['classeReelle']), how = 'left')
    probas = probas.join(pd.DataFrame(np.array(returns_test), columns = ['return']), how = 'left')

    option = st.slider("Nombre d'entreprises composant le portefeuille", 1, 100)

    predictions1 = probas.sort_values('proba_gain', ascending = False).head(option)


    st.write("Rendement réel (par rapport au marché:)", np.round(predictions1['return'].mean()*100,2),"%")

    st.write(" ")
    st.write("Top", option, "entreprises sélectionées par le modèle")

    st.dataframe(predictions1.drop(['proba_perte', 'proba_gain', 'classeReelle','return'],axis=1))


    

    










