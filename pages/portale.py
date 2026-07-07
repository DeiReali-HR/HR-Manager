import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS per il layout a due colonne con card fissa
st.markdown("""
<style>
    .card-orizzontale {
        display: flex;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        height: 380px;
        margin-bottom: 20px;
        overflow: hidden;
        background: white;
    }
    .img-lato { width: 40%; background-size: cover; background-position: center; border-right: 1px solid #E2E8F0; }
    .testo-lato { width: 60%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
    .btn-black { background: #0F172A; color: white !important; padding: 12px; border-radius: 6px; text-align: center; text-decoration: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    annunci = supabase.table("annunci").select("*").execute().data or []
    
    col1, col2 = st.columns(2)
    s_r = col1.selectbox("Qualifica", ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci]))))
    s_s = col2.selectbox("Sede", ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci]))))

    filtrati = [a for a in annunci if (s_r == "Tutti i Ruoli" or a["posizione"] == s_r) and (s_s == "Tutte le Sedi" or a["sede"] == s_s)]

    # Ciclo a due a due per le colonne
    for i in range(0, len(filtrati), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(filtrati):
                a = filtrati[i + j]
                with row[j]:
                    st.markdown(f"""
                    <div class="card-orizzontale">
                        <div class="img-lato" style="background-image: url('{a.get('immagine')}');"></div>
                        <div class="testo-lato">
                            <div>
                                <h3>{a.get('posizione')}</h3>
                                <p style="font-size:13px; color: #64748B;">📍 {a.get('sede')} | 💼 {a.get('inquadramento')} | 💸 {a.get('importo')}€</p>
                                <div style="font-size:13px; height: 150px; overflow-y: auto;">{a.get('note')}</div>
                            </div>
                            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗️</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_vetrina()
