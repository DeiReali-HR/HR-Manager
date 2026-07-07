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
    .testo-lato { width: 60%; padding: 20px; display: flex; flex-direction: column; }
    /* Questo assicura che il contenuto prenda tutto lo spazio e il bottone resti in basso */
    .contenuto-scroll { flex-grow: 1; overflow-y: auto; margin-bottom: 15px; }
    .btn-black { background: #0F172A; color: white !important; padding: 12px; border-radius: 6px; text-align: center; text-decoration: none; font-weight: bold; width: 100%; margin-top: auto; }
</style>
""", unsafe_allow_html=True)

# ... (dentro il ciclo della funzione mostra_vetrina) ...
                    st.markdown(f"""
                    <div class="card-orizzontale">
                        <div class="img-lato" style="background-image: url('{a.get('immagine')}');"></div>
                        <div class="testo-lato">
                            <div class="contenuto-scroll">
                                <h3>{a.get('posizione')}</h3>
                                <p style="font-size:12px; color: #64748B;">📍 {a.get('sede')} | 💼 {a.get('inquadramento')} | 💸 {a.get('importo')}€</p>
                                <div style="font-size:13px;">{a.get('note')}</div>
                            </div>
                            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗️</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_vetrina()
