import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# Stile professionale pulito
st.markdown("""
<style>
    .main-card { border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; background: white; margin-bottom: 20px; transition: 0.3s; }
    .main-card:hover { box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .img-placeholder { width: 100%; height: 200px; background: #F8FAFC; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; }
    .btn-candidati { width: 100%; background: #0F172A; color: white; padding: 12px; border-radius: 6px; text-align: center; font-weight: bold; cursor: pointer; }
</style>
""", unsafe_allow_html=True)

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    annunci = supabase.table("annunci").select("*").execute().data or []

    # Filtri eleganti
    c1, c2 = st.columns(2)
    ruoli = ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci])))
    sede = ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci])))
    s_r = c1.selectbox("Qualifica", ruoli)
    s_s = c2.selectbox("Sede", sede)

    # Logica filtraggio
    f = [a for a in annunci if (s_r == "Tutti i Ruoli" or a["posizione"] == s_r) and (s_s == "Tutte le Sedi" or a["sede"] == s_s)]

    # Griglia a 2 colonne professionale
    for i in range(0, len(f), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(f):
                a = f[i + j]
                with row[j]:
                    with st.container(border=True):
                        if a.get("immagine"):
                            st.image(a["immagine"], use_container_width=True)
                        else:
                            st.markdown('<div class="img-placeholder">Anteprima non disponibile</div>', unsafe_allow_html=True)
                        
                        st.subheader(a.get("posizione"))
                        st.markdown(f"📍 {a.get('sede')} | 💼 {a.get('inquadramento')} | 💸 {a.get('importo')}€")
                        st.write(a.get("note", "")[:180] + "...")
                        
                        if st.button("CANDIDATI ORA ↗️", key=str(a['id'])):
                            st.query_params["job"] = a['id']
                            st.rerun()

if "job" in st.query_params:
    st.info("Visualizzazione candidatura selezionata...")
else:
    mostra_vetrina()
