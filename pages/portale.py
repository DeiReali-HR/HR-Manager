import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    annunci = supabase.table("annunci").select("*").execute().data
    
    if not annunci:
        st.info("Nessun annuncio disponibile al momento.")
        return

    col1, col2 = st.columns(2)
    s_ruolo = col1.selectbox("Qualifica", ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci if a.get("posizione")]))))
    s_citta = col2.selectbox("Sede", ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci if a.get("sede")]))))

    filtrati = [a for a in annunci if (s_ruolo == "Tutti i Ruoli" or a.get("posizione") == s_ruolo) and (s_citta == "Tutte le Sedi" or a.get("sede") == s_citta)]

    for i in range(0, len(filtrati), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(filtrati):
                a = filtrati[i + j]
                with row[j]:
                    # CONTROLLO SICUREZZA: Carica l'immagine solo se il link esiste
                    img_url = a.get("immagine")
                    if img_url:
                        st.image(img_url, use_container_width=True)
                    else:
                        st.warning("Immagine non disponibile")
                    
                    st.subheader(a.get("posizione", "Senza titolo"))
                    st.markdown(f"📍 {a.get('sede', 'N/D')} | 💼 {a.get('inquadramento', 'N/D')} | 💸 {a.get('importo', '0')}€")
                    st.write(a.get("note", "")[:200] + "...")
                    
                    if st.button("CANDIDATI ORA ↗️", key=f"btn_{a['id']}"):
                        st.query_params["job"] = a['id']
                        st.rerun()

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_vetrina()
