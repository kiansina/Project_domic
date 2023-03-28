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
