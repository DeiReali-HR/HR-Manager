import streamlit as st
import pandas as pd
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    
    # Recupero annunci
    try:
        res = supabase.table("annunci").select("*").execute()
        annunci = res.data if res.data else []
    except Exception as e:
        st.error(f"Errore caricamento database: {e}")
        return

    # Filtri
    col_f1, col_f2 = st.columns(2)
    ruoli = ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci if a.get("posizione")])))
    citta = ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci if a.get("sede")])))
    
    search_ruolo = col_f1.selectbox("🔍 Qualifica", ruoli)
    search_citta = col_f2.selectbox("📍 Sede", citta)

    # Logica filtro
    filtrati = [a for a in annunci if (search_ruolo == "Tutti i Ruoli" or a.get("posizione") == search_ruolo) and 
                                     (search_citta == "Tutte le Sedi" or a.get("sede") == search_citta)]

    if not filtrati:
        st.info("Nessun annuncio trovato.")
        return

    # Griglia dinamica a 2 colonne (Metodo nativo Streamlit)
    for i in range(0, len(filtrati), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(filtrati):
                a = filtrati[i + j]
                with row[j]:
                    with st.container(border=True):
                        # Immagine
                        img_url = a.get("immagine") or "https://via.placeholder.com/600x300?text=Dei+Reali"
                        st.image(img_url, use_container_width=True)
                        
                        # Info
                        st.subheader(a.get('posizione', 'Senza titolo'))
                        st.markdown(f"**📍 Sede:** {a.get('sede', 'N/D')} | **💸 Compenso:** {a.get('importo', '0')} €")
                        st.markdown(f"**💼 Inquadramento:** {a.get('inquadramento', 'N/D')}")
                        
                        # Descrizione limitata
                        note = a.get('note', '')
                        st.write(note[:200] + "..." if len(note) > 200 else note)
                        
                        # Bottone
                        if st.button("CANDIDATI ORA ↗️", key=f"btn_{a['id']}"):
                            st.query_params["job"] = a['id']
                            st.rerun()

# --- LOGICA NAVIGAZIONE ---
if "job" in st.query_params:
    st.write("Redirect in corso...")
    st.rerun() # In un'app reale qui richiameresti la funzione mostra_dettaglio
else:
    mostra_vetrina()
