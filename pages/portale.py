import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS Professionale per allineamento perfetto
st.markdown("""
<style>
    .card-orizzontale {
        display: flex;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        height: 380px;
        margin-bottom: 25px;
        overflow: hidden;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .img-lato { 
        width: 40%; 
        background-size: cover; 
        background-position: center; 
        border-right: 1px solid #E2E8F0; 
        background-color: #f0f0f0;
    }
    .testo-lato { 
        width: 60%; 
        padding: 20px; 
        display: flex; 
        flex-direction: column; 
    }
    .contenuto-scroll { 
        flex-grow: 1; 
        overflow-y: auto; 
        margin-bottom: 15px; 
    }
    .btn-black { 
        background: #0F172A; 
        color: white !important; 
        padding: 12px; 
        border-radius: 6px; 
        text-align: center; 
        text-decoration: none; 
        font-weight: bold; 
        width: 100%; 
        display: block;
    }
    .btn-black:hover { background: #1E293B; }
</style>
""", unsafe_allow_html=True)

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    
    # Recupero dati
    try:
        annunci = supabase.table("annunci").select("*").execute().data or []
    except:
        annunci = []

    # Filtri
    col1, col2 = st.columns(2)
    ruoli = ["Tutti i Ruoli"] + sorted(list(set([a.get("posizione") for a in annunci if a.get("posizione")])))
    citta = ["Tutte le Sedi"] + sorted(list(set([a.get("sede") for a in annunci if a.get("sede")])))
    
    s_r = col1.selectbox("Qualifica", ruoli)
    s_s = col2.selectbox("Sede", citta)

    filtrati = [a for a in annunci if (s_r == "Tutti i Ruoli" or a.get("posizione") == s_r) and (s_s == "Tutte le Sedi" or a.get("sede") == s_s)]

    # Griglia annunci
    for i in range(0, len(filtrati), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(filtrati):
                a = filtrati[i + j]
                with row[j]:
                    img_url = a.get('immagine', '')
                    st.markdown(f"""
                    <div class="card-orizzontale">
                        <div class="img-lato" style="background-image: url('{img_url}');"></div>
                        <div class="testo-lato">
                            <div class="contenuto-scroll">
                                <h3>{a.get('posizione', 'Posizione')}</h3>
                                <p style="font-size:12px; color: #64748B;">📍 {a.get('sede', 'N/D')} | 💼 {a.get('inquadramento', 'N/D')} | 💸 {a.get('importo', '0')}€</p>
                                <div style="font-size:13px; line-height: 1.4;">{a.get('note', '')}</div>
                            </div>
                            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗️</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Gestione navigazione
if "job" in st.query_params:
    st.subheader("Procedura di candidatura")
    st.write("Stai completando la candidatura per l'annuncio selezionato.")
    if st.button("⬅️ Torna alla lista"):
        st.query_params.clear()
        st.rerun()
else:
    mostra_vetrina()
