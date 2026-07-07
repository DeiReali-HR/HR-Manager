import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide")

# CSS per forzare il layout identico alla tua anteprima
st.markdown("""
<style>
.card { border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; background: white; margin-bottom: 20px; height: 500px; display: flex; flex-direction: column; }
.card img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; }
.card h3 { margin: 0 0 10px 0; font-size: 1.2rem; }
.btn-candidati { background-color: #0F172A; color: white !important; padding: 10px; text-align: center; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: auto; }
</style>
""", unsafe_allow_html=True)

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    annunci = supabase.table("annunci").select("*").execute().data
    
    col1, col2 = st.columns(2)
    s_ruolo = col1.selectbox("Qualifica", ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci]))))
    s_citta = col2.selectbox("Sede", ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci]))))

    filtrati = [a for a in annunci if (s_ruolo == "Tutti i Ruoli" or a["posizione"] == s_ruolo) and (s_citta == "Tutte le Sedi" or a["sede"] == s_citta)]

    # Griglia gestita con indice per evitare che il layout "si rompa"
    for i in range(0, len(filtrati), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(filtrati):
                a = filtrati[i + j]
                with row[j]:
                    st.markdown(f"""
                    <div class="card">
                        <img src="{a.get('immagine')}" onerror="this.src='https://via.placeholder.com/600x300'">
                        <h3>{a.get('posizione')}</h3>
                        <p>📍 {a.get('sede')} | 💼 {a.get('inquadramento')} | 💸 {a.get('importo')}€</p>
                        <p style="overflow-y: auto; flex-grow: 1;">{a.get('note', '')}</p>
                        <a href="?job={a['id']}" class="btn-candidati">CANDIDATI ORA ↗️</a>
                    </div>
                    """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.info(f"Stai visualizzando l'annuncio ID: {st.query_params['job']}. [Torna alla lista](?)" )
else:
    mostra_vetrina()
