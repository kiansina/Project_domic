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
st.set_page_config(page_title="Domiciliatario", page_icon=img)

hide_menu_style= """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """

d = date.today()
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
df.set_index('id',inplace=True)

@st.cache_data
def get_data():
    return []

def to_excel3(df,index=False):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=index, sheet_name='Sheet1', startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    worksheet.set_column('A:ZZ', 25,cell_format)
    header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'vdistributed',
    'align' : 'center',
    'fg_color': '#A5F5B0'})#,
    for col_num, value in enumerate(df.reset_index().columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.set_column('A:ZZ', 25)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

sql = """select * from v_user where stato=1 order by id"""
cursor = conn.cursor()
cursor.execute(sql)
duser=pd.DataFrame(cursor.fetchall(),columns=['ID','User', 'nome',	'Team',	'Qualifica', 'Tariffa', 'stato', 'linkf'])

if "Confirm" not in st.session_state:
    st.session_state["Confirm"] = False

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

def sql_ins():
    st.session_state["Confirm"]=not st.session_state["Confirm"]
    if st.session_state["Confirm"]==True:
        dx=pd.DataFrame(e_df)
        dx=dx.dropna(subset=[st.session_state["username"].lower()])
        for i in dx.index:
            sql="""update domiciliatario
                set {}={}
                where id={}""".format(st.session_state["username"].lower(),dx[st.session_state["username"].lower()].loc[i],i)
            cursor = conn.cursor()
            cursor.execute(sql)
    st.session_state["Confirm"]=not st.session_state["Confirm"]

if check_password():
    kos,st.session_state["username"]=check_password()
    if st.session_state["username"] not in ['Marco_Troisi', 'Antonio_Schiavone', 'Sina_Kian', 'Stefano_Menghini']:
        st.session_state["aut"] = 'user'
    #else:
    #    st.session_state["aut"] = 'sup'
    DFST=get_data()
    dfs=duser[duser['User']==st.session_state["username"]][duser.columns[2:-4]]
    st.image(
    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
     width=150,
     )
    st.title(" :orange[Domiciliatario] 🏫")
    col1, col2 = st.columns(2)
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write(dfs)
    with col2:
        st.image(
        "{}".format(duser[duser['User']==st.session_state["username"]]['linkf'].iloc[0]),
         width=150,
         )
    
    option = st.selectbox(
    'What do you need?',
    ('Extracting Votes', 'Voting'))

    if option=='Voting':
        xx=['domiciliatario', 'rating_base']+[st.session_state["username"].lower()]
        e_df = st.experimental_data_editor(df[xx], num_rows="dynamic")
        if st.button('Confirm'):
            sql_ins()
    elif option=='Extracting Votes':
        if st.button('extract voto'):
            final_file = to_excel3(df,index=True)
            st.download_button(
            "Press to Download",
            final_file,
            "Pivot_UP_{}.xlsx".format(d.strftime("%m_%d_%y")),
            "text/csv",
            key='download-excel'
            )

    

