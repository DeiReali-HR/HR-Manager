import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

# --- CSS FORZATO ---
st.markdown("""
<style>
    /* Forza la griglia a due colonne */
    .stColumn { width: 48% !important; float: left; margin: 1%; }
    .card { border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; height: 400px; overflow: hidden; background: white; }
    .img-box { width: 100%; height: 150px; background-size: cover; background-position: center; border-radius: 8px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    res = supabase.table("annunci").select("*").execute()
    annunci = res.data

    # Barra filtri
    col_f1, col_f2 = st.columns(2)
    search_ruolo = col_f1.selectbox("Qualifica", ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci]))))
    search_citta = col_f2.selectbox("Sede", ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci]))))

    filtrati = [a for a in annunci if (search_ruolo == "Tutti i Ruoli" or a["posizione"] == search_ruolo) and 
                                     (search_citta == "Tutte le Sedi" or a["sede"] == search_citta)]

    # Griglia manuale a 2 colonne
    it = iter(filtrati)
    for coppia in zip(it, it): # Prende a due a due
        c1, c2 = st.columns(2)
        for col, a in zip([c1, c2], coppia):
            with col:
                st.markdown(f"""
                <div class="card">
                    <div class="img-box" style="background-image: url('{a.get('immagine')}');"></div>
                    <h3>{a['posizione']}</h3>
                    <p>📍 {a.get('sede')} | 💸 {a.get('importo', '0')}€</p>
                    <p style="height: 100px; overflow-y: auto;">{a.get('note', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"CANDIDATI ORA", key=f"btn_{a['id']}"):
                    st.query_params["job"] = a['id']
                    st.rerun()

# --- LOGICA NAVIGAZIONE ---
if "job" in st.query_params:
    # Qui richiameresti la funzione mostra_dettaglio che avevamo già
    st.write("Dettaglio in caricamento...") 
else:
    mostra_vetrina()
