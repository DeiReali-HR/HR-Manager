import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

# CSS per il layout professionale a card orizzontale
st.markdown("""
<style>
.card-container { display: flex; border: 1px solid #E2E8F0; border-radius: 12px; height: 350px; margin-bottom: 20px; overflow: hidden; background: white; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
.card-img { width: 40%; height: 100%; background-size: cover; background-position: center; border-right: 1px solid #E2E8F0; }
.card-content { width: 60%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
.btn-candidati { background-color: #0F172A; color: white !important; padding: 12px; border-radius: 6px; text-align: center; text-decoration: none; font-weight: bold; font-size: 14px; }
.btn-candidati:hover { background-color: #1E293B; }
h3 { margin: 0 0 10px 0; font-size: 20px; }
p { margin: 5px 0; font-size: 14px; color: #475569; }
</style>
""", unsafe_allow_html=True)

def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    # Recupero dati dal database
    annunci = supabase.table("annunci").select("*").execute().data
    
    # Filtri
    col1, col2 = st.columns(2)
    ruoli = ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci])))
    citta = ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci])))
    s_ruolo = col1.selectbox("🔍 Qualifica", ruoli)
    s_citta = col2.selectbox("📍 Sede", citta)

    filtrati = [a for a in annunci if (s_ruolo == "Tutti i Ruoli" or a["posizione"] == s_ruolo) and (s_citta == "Tutte le Sedi" or a["sede"] == s_citta)]

    # Layout a 2 colonne dinamiche
    it = iter(filtrati)
    for coppia in zip(it, it):
        cols = st.columns(2)
        for i, a in enumerate(coppia):
            with cols[i]:
                st.markdown(f"""
                <div class="card-container">
                    <div class="card-img" style="background-image: url('{a.get('immagine')}');"></div>
                    <div class="card-content">
                        <div>
                            <h3>{a['posizione']}</h3>
                            <p>📍 {a.get('sede')} | 💼 {a.get('inquadramento')} | 💸 {a.get('importo')}€</p>
                            <p style="height: 120px; overflow-y: auto;">{a.get('note')}</p>
                        </div>
                        <a href="?job={a['id']}" class="btn-candidati">CANDIDATI ORA ↗️</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Gestione navigazione
if "job" in st.query_params:
    st.write("Redirect al form di candidatura...")
    st.rerun()
else:
    mostra_vetrina()
