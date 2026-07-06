import streamlit as st
import pandas as pd
from supabase import create_client

# Configurazione (copiala uguale a quella che hai in ats_app.py)
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# Imposta il layout
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

# Qui incolli il codice che abbiamo preparato insieme:
# 1. La logica per leggere da Supabase (quella che crea le card)
# 2. La logica del Form di candidatura
