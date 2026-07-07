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

    # Ciclo per creare righe da 2 colonne
    for i in range(0, len(filtrati), 2):
        colonne = st.columns(2)
        # Primo annuncio della riga
        with colonne[0]:
            a = filtrati[i]
            st.markdown(f"### {a['posizione']}")
            st.markdown(f"📍 {a.get('sede', 'N/D')} | 💸 {a.get('importo', '0')}€")
            st.write(a.get('note', '')[:150] + "...")
            if st.button("CANDIDATI ORA", key=f"btn_{a['id']}"):
                st.query_params["job"] = a['id']
                st.rerun()
        
        # Secondo annuncio della riga (se esiste)
        if i + 1 < len(filtrati):
            with colonne[1]:
                a = filtrati[i+1]
                st.markdown(f"### {a['posizione']}")
                st.markdown(f"📍 {a.get('sede', 'N/D')} | 💸 {a.get('importo', '0')}€")
                st.write(a.get('note', '')[:150] + "...")
                if st.button("CANDIDATI ORA", key=f"btn_{a['id']}"):
                    st.query_params["job"] = a['id']
                    st.rerun()
