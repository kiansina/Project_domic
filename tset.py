import streamlit as st
import pandas as pd
import psycopg2
import time
import random
from PIL import Image
import datetime
from datetime import date
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import create_engine
import sqlalchemy
import numpy as np
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from urllib.parse import quote_plus
import altair as alt
import plotly.express as px
import locale
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
locale.setlocale(locale.LC_ALL, 'it_IT')
img=Image.open('lo.jfif')
st.set_page_config(page_title="Dashboard", page_icon=img)

hide_menu_style= """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """

engine = create_engine('postgresql+psycopg2://{}:%s@{}/{}'.format(st.secrets["postgres"]['user'],st.secrets["postgres"]['host'],st.secrets["postgres"]['dbname']) % quote_plus(st.secrets["postgres"]['password']))
st.markdown(hide_menu_style, unsafe_allow_html=True)
# Initialize connection.
# Uses st.experimental_singleton to only run once.
#@st.experimental_singleton
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

conn.autocommit = True

cols=['id', 'domiciliatario','alessandro_marcadelli', 'alice_giubbi', 'andrea_manduchi', 'andrea_siena', 'andrea_unfer', 'angela_romano', 'anna_pettenati', 'antonio_scalera', 'antonio_schiavone', 'antonio_toscano', 'barbara_zagaria', 'benedetta_cinti', 'benedetta_paniconi', 'chiara_butta', 'danilo_brandi', 'dario_mami', 'davide_sarina', 'diandra_sciarra', 'edoardo_salmaso', 'egzona_baxhak', 'eleonora_gioia', 'elisa_albanese', 'ester_famao', 'eva_baldassarre', 'federica_cirelli', 'federica_colombo', 'federica_de_carlo', 'federica_morandotti', 'filippo_maria_traina', 'filippo_porta', 'gaia_prudente', 'giangiacomo_ciceri', 'gianmarco_marani', 'ludovica_ferri', 'giancarlo_accardo', 'giulia_galati', 'giulia_piccolantonio', 'giuseppe_bava', 'giuseppe_maria_iannone', 'giuseppe_provinzano', 'giuseppina_pagano', 'greta_castiglionesi', 'ilenia_febbi', 'irene_micieli', 'irene_tomassi', 'lamberto_banfi', 'lorenzo_marchionni', 'lucia_tortoreti', 'manuela_consoli', 'marco_bruno', 'marco_innocenti', 'marco_troisi', 'margaret_scolaro', 'margherita_la_grotteria', 'maria_monaco', 'martina_fioravanti_paolucci', 'martina_pontiggia', 'matteo_rovarini', 'maurizio_cilione', 'michela_gentili', 'michele_pellicciari', 'nadia_crivellari', 'nikla_colella', 'pamela_barile', 'paolo_forti', 'roberta_pisano', 'roberto_rasoli', 'salvatore_tripodi', 'selenia_panebianco', 'silvia_poli', 'simone_tumino', 'sina_kian', 'stefania_carriero', 'stefano_menghini', 'stefano_riccardi', 'valentina_lange', 'valeria_canestri', 'valeria_sangalli', 'vanessa_de_martino', 'vittorio_petruzzi', 'flavia_lo_forte', 'rating_base']

sql="""select * from domiciliatario;"""
cursor = conn.cursor()
cursor.execute(sql)
#nind=cursor.fetchall()
df=pd.DataFrame(cursor.fetchall(),columns=cols)









def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            #del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True , st.session_state["username"]


if check_password():
    kos,st.session_state["username"]=check_password()
    if st.session_state["username"] not in ['Marco_Troisi', 'Antonio_Schiavone', 'Sina_Kian', 'Stefano_Menghini']:
        st.session_state["aut"] = 'user'
    #else:
    #    st.session_state["aut"] = 'sup'

    st.write(df)
    e_df = st.experimental_data_editor(df)
