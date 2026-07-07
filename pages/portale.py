import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide")

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    annunci = supabase.table("annunci").select("*").execute().data
    
    col1, col2 = st.columns(2)
    s_ruolo = col1.selectbox("Qualifica", ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci]))))
    s_citta = col2.selectbox("Sede", ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci]))))

    filtrati = [a for a in annunci if (s_ruolo == "Tutti i Ruoli" or a["posizione"] == s_ruolo) and (s_citta == "Tutte le Sedi" or a["sede"] == s_citta)]

    for i in range(0, len(filtrati), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(filtrati):
                a = filtrati[i + j]
                with row[j]:
                    # Usiamo il comando nativo di Streamlit per l'immagine
                    st.image(a.get("immagine"), use_container_width=True)
                    st.subheader(a.get("posizione"))
                    st.markdown(f"📍 {a.get('sede')} | 💼 {a.get('inquadramento')} | 💸 {a.get('importo')}€")
                    st.write(a.get("note", ""))
                    if st.button("CANDIDATI ORA ↗️", key=f"btn_{a['id']}"):
                        st.query_params["job"] = a['id']
                        st.rerun()

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_vetrina()
