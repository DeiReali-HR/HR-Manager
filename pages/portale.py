import streamlit as st
import pandas as pd
import re, random
from supabase import create_client
from pypdf import PdfReader

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

# --- CSS PROFESSIONALE ---
st.markdown("""
<style>
.showcase-grid-2columns { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; width: 100%; margin-top: 15px; }
.showcase-card-row { display: flex; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; height: 382px; overflow: hidden; }
.showcase-img-side { width: 40%; height: 100%; background-size: cover; background-position: center; }
.showcase-content-side { width: 60%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
.showcase-scrollable-body { overflow-y: auto; flex-grow: 1; margin-bottom: 10px; }
.showcase-btn { background-color: #0F172A; color: white !important; padding: 10px; border-radius: 6px; text-align: center; text-decoration: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- FUNZIONI UTILI ---
def estrai_testo_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages])

# --- LOGICA DETTAGLIO E CANDIDATURA ---
def mostra_dettaglio(job_id):
    res = supabase.table("annunci").select("*").eq("id", job_id).execute()
    annuncio = res.data[0] if res.data else None
    if not annuncio:
        st.error("Annuncio non trovato.")
        return

    st.markdown(f"## {annuncio['posizione']}")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(annuncio.get('immagine') or "https://via.placeholder.com/600", use_container_width=True)
        st.write(annuncio['note'])
    with col2:
        st.markdown("### 📩 Invia la tua candidatura")
        with st.form("candidatura"):
            nome = st.text_input("Nome e Cognome")
            mail = st.text_input("E-mail")
            tel = st.text_input("Telefono")
            file = st.file_uploader("Allega CV (PDF)", type=["pdf"])
            if st.form_submit_button("INVIA CANDIDATURA"):
                if nome and mail and tel and file:
                    testo = estrai_testo_pdf(file)
                    nome_file = f"{re.sub(r'[^a-zA-Z0-9]', '_', nome.lower())}_{random.randint(1000,9999)}.pdf"
                    file.seek(0)
                    supabase.storage.from_("curriculum").upload(nome_file, file.read())
                    supabase.table("candidati").insert({
                        "nome": nome, "email": mail, "telefono": tel, "posizione": annuncio['posizione'],
                        "stato": "In Screening", "immagine": supabase.storage.from_("curriculum").get_public_url(nome_file)
                    }).execute()
                    st.success("🎉 Candidatura inviata!")
                else:
                    st.error("Compila tutto!")

# --- LOGICA VETRINA ---
def mostra_vetrina():
    st.title("📋 Tutte le Posizioni Aperte")
    res = supabase.table("annunci").select("*").execute()
    annunci = res.data
    
    col1, col2 = st.columns(2)
    search_ruolo = col1.selectbox("Qualifica", ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci]))))
    search_citta = col2.selectbox("Sede", ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci]))))

    filtrati = [a for a in annunci if (search_ruolo == "Tutti i Ruoli" or a["posizione"] == search_ruolo) and 
                                     (search_citta == "Tutte le Sedi" or a["sede"] == search_citta)]

    st.markdown("<div class='showcase-grid-2columns'>", unsafe_allow_html=True)
    for a in filtrati:
        st.markdown(f"""
        <div class="showcase-card-row">
            <div class="showcase-img-side" style="background-image: url('{a.get('immagine')}');"></div>
            <div class="showcase-content-side">
                <div class="showcase-scrollable-body">
                    <h3>{a['posizione']}</h3>
                    <p>📍 {a.get('sede')} | 💸 {a.get('importo', '0')}€</p>
                    <p>{a.get('note', '')[:100]}...</p>
                </div>
                <a href="?job={a['id']}" class="showcase-btn">CANDIDATI ORA ↗️</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- NAVIGAZIONE ---
if "job" in st.query_params:
    mostra_dettaglio(st.query_params["job"])
else:
    mostra_vetrina()
