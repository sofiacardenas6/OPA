import streamlit as st
import pandas as pd
st.set_page_config(page_title="ONLINE PORTFOLIO ALLOCATION", layout="wide")

#séparation des colonnes pour centrer la photo
col1, col2, col3 = st.columns([0.01, 5, 0.01])
with col2:
   st.image("./images/financeV8.png", use_column_width=True) 

   st.markdown("""
   <div style="
                background-color: rgba(235, 159, 115, 0.2); 
                border: 3px solid black;
                padding: 40px;">
   <h1 style="color:black;text-align:center; 
   font-family: 'Times New Roman', Times, serif; 
   font-weight: normal;
   font-style: italic;">
   Projet effectué dans le cadre de la formation Data
   Scientist de DataScientist.com <br>
   Promotion novembre 2023 <br>
   Créatrices <br>
   Sofía Cárdenas <br>
   Faith Sholesi</h1>
   </div>
    """, unsafe_allow_html=True)

#mise au centre du titre 
col1, col2 = st.columns([5,5])
with col1: 
   st.markdown("""
      <div style="font-size: 50px;text-align:center;">
      <strong>Contexte</strong>
      </div>
      """, unsafe_allow_html=True)

#contenu centré vers la droite
col1, col2, col3 = st.columns([4,0.5,3])
with col1:
   st.markdown("""
      <div style="font-size: 30px;text-align:center;">
         <strong> Un marché financier </strong> : Lieu où plusieurs acteurs se rencontrent pour échanger des
         instruments financiers.
         <br>
         Les entreprises mettent en vente leur instruments financiers
         afin de continuer à se developper <br>
         pendant que les investiseurs
         les rachètent pour ainsi faire du profit.
         <br>
         <br>
         Cette action n'est pas sans risque pour les actionnaires
         (crises financières de 2008/1929).<br>
         <strong> But des actionnaires : d'investir dans des
         instruments fiables et performants. </strong>
      </div>
      """, unsafe_allow_html=True)

#image de finance centré vers la droite
with col3:
   st.image("./images/bourse.jpg",  width=400)

col1, col2 = st.columns([5,5])
with col1: 
   st.markdown("""
      <div style="font-size: 50px;text-align:center;margin-top:10%">
      <strong>Données</strong>
      </div>
      """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([4,0.5,3])
with col1:
   st.markdown("""
      <div style="font-size: 30px;text-align:center">
      Les données utilisées dans ce projet proviennent de l’API open-source yfinance, 
      qui permet d’accéder aux informations financières fournies par Yahoo Finance.<br>
      Les informations sur chaque action sont accessibles via un ticker, 
      c’est-à-dire un symbole identifiant l’action.
      </div>
      """, unsafe_allow_html=True)

with col3:
   st.image("./images/yahoo_finance.png",  width=300)
   

