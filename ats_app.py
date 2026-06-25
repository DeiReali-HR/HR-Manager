import streamlit as st
import pandas as pd
import json
import random
import os
from datetime import datetime

# 1. Configurazione della pagina e palette colori (Bianco, Azzurro tenue, Scritte Blu)
st.set_page_config(page_title="Dei Reali ATS", page_icon="💼", layout="wide")

st.markdown("""
    <style>
    /* Sfondo generale bianco e scritte blu scuro */
    .stApp {
        background-color: #FFFFFF;
        color: #0A2540;
    }
    /* Sidebar azzurro tenue */
    [data-testid="stSidebar"] {
        background-color: #EBF3FC !important;
        color: #0A2540 !important;
    }
    /* Testi principali e titoli in blu */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #0A2540 !important;
    }
    /* Bottoni della Dashboard a tasti (Azzurro tenue con testo blu) */
    .stButton>button {
        background-color: #D3E5F9 !important;
        color: #0A2540 !important;
        border: 1px solid #B4D3F5 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #B4D3F5 !important;
        border-color: #0A2540 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione dello Stato della Sessione
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'candidates' not in st.session_state:
    st.session_state.candidates = [
        {"id": "CAND-001", "nome": "Marco Rossi", "competenze": "Python, Django, PostgreSQL", "formazione": "Laurea Informatica", "punteggio": 9, "stato": "Nuovo"},
        {"id": "CAND-002", "nome": "Giulia Bianchi", "competenze": "React, TypeScript, CSS", "formazione": "Master Front-End", "punteggio": 7, "stato": "Nuovo"},
    ]
if 'clients' not in st.session_state:
    st.session_state.clients = [{"id": "CLI-001", "nome": "TechCorp S.r.l.", "settore": "IT", "referente": "Ing. Riva"}]
if 'interviews' not in st.session_state:
    st.session_state.interviews = []
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "📢 Annunci"

# --- SIDEBAR (MENU DI SINISTRA) ---
with st.sidebar:
    # Inserimento Logo Dei Reali (Cerca l'immagine caricata nella stessa cartella)
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.subheader("👑 DEI REALI")
        st.caption("Corporate Consulting")
    
    st.divider()
    st.caption("🔹 MONITORAGGIO APPLICATIVO")
    st.markdown("*Utenti attivi:* 1/10\n\n*CV in Database:* 2/10000")
    st.divider()
    st.info("🤖 AI Gemini pronta per l'integrazione a consumo.")

# --- DASHBOARD A TASTI (TONI AZZURRO E BLU) ---
st.title("💼 Sistema di Gestione & Selezione Personale")
st.markdown("### 🎛️ Dashboard Operativa")

# Griglia di pulsanti per la navigazione
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1:
    if st.button("📢\nAnnunci"): st.session_state.current_menu = "📢 Annunci"
with c2:
    if st.button("📥\nScreening CV"): st.session_state.current_menu = "📥 Screening CV"
with c3:
    if st.button("🤝\nColloqui AI"): st.session_state.current_menu = "🤝 Colloqui AI"
with c4:
    if st.button("🎉\nAssunzioni"): st.session_state.current_menu = "🎉 Assunzioni"
with c5:
    if st.button("📊\nReport"): st.session_state.current_menu = "📊 Report"
with c6:
    if st.button("🏢\nClienti"): st.session_state.current_menu = "🏢 Clienti"
with c7:
    if st.button("👥\nCandidati"): st.session_state.current_menu = "👥 Candidati"

st.divider()

# --- GESTIONE DELLE AREE ---

# AREA 1: MODULO ANNUNCI (AGGIORNATO)
if st.session_state.current_menu == "📢 Annunci":
    st.header("📢 Creazione e Pubblicazione Annunci")
    
    col_sx, col_dx = st.columns(2)
    
    with col_sx:
        st.subheader("📝 Dati dell'Annuncio")
        uploaded_img = st.file_uploader("🖼️ Foto caricabile da locale", type=["png", "jpg", "jpeg"])
        titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. Senior Project Manager")
        
        # Blocco Importi/Costi
        st.markdown("*💰 Specifica Economica*")
        tipo_importo = Skinner = st.radio("Tipo di tariffa", ["RAL (Annua)", "Importo Lordo", "Costo Orario"], horizontal=True)
        valore_importo = st.text_input("Valore economico (€)", placeholder="es. 40.000 o 45/ora")
        
        indirizzo_job = st.text_input("🏢 Indirizzo / Sede di lavoro", placeholder="es. Via Condotti, Roma")
        
        st.markdown("*📞 Dati di Contatto*")
        cellulare_job = st.text_input("Cellulare", placeholder="es. +39 333 1234567")
        mail_job = st.text_input("E-mail di contatto", placeholder="es. hr@deireali.com")

    with col_dx:
        st.subheader("🤖 Assistente di Scrittura IA")
        info_basiche = st.text_area("Inserisci le info basiche dell'annuncio per l'editing IA", placeholder="es. Cerchiamo un esperto di consulenza aziendale per la sede di Roma, offriamo welfare...")
        tono = st.selectbox("Tono dell'editing", ["Professionale", "Istituzionale", "Moderno"])
        
        if st.button("Ottimizza Annuncio con IA ✨"):
            if titolo_job and info_basiche:
                st.session_state['gen_text'] = f"### Offerta di Lavoro: {titolo_job}\n\n*Sede:* {indirizzo_job}\n*Budget/Compenso:* {valore_importo} ({tipo_importo})\n\n*Descrizione Posizione:\n{info_basiche}\n\nContatti:*\n✉️ {mail_job} | 📞 {cellulare_job}"
            else:
                st.error("Inserisci almeno il Titolo e le Info Basiche!")

    if 'gen_text' in st.session_state:
        st.divider()
        st.subheader("🌐 Verifica ed Esporta Pagina Web Annuncio")
        testo_definitivo = st.text_area("Modifica il testo finale", value=st.session_state['gen_text'], height=200)
        
        if st.button("Conferma e Pubblica Annuncio 🌐"):
            slug = titolo_job.lower().replace(" ", "-")
            link_generato = f"https://deireali-hr.streamlit.app/jobs/{slug}"
            st.session_state.jobs.append({"titolo": titolo_job, "tipo": tipo_importo, "valore": valore_importo, "link": link_generato})
            st.success("🎉 Pagina Web dell'annuncio creata!")
            st.code(link_generato)

    if st.session_state.jobs:
        st.divider()
        st.subheader("📋 Storico Annunci Pubblicati")
        st.dataframe(pd.DataFrame(st.session_state.jobs), use_container_width=True)

# AREA 2: SCREENING CV
elif st.session_state.current_menu == "📥 Screening CV":
    st.header("📥 Screening CV & Catalogazione AI")
    up_cv = st.file_uploader("Trascina qui i CV dei candidati", accept_multiple_files=True)
    if up_cv:
        st.success("CV importati nel database! Gemini assegnerà i punteggi reali (1-10) non appena collegata l'API key.")
    st.dataframe(pd.DataFrame(st.session_state.candidates), use_container_width=True)

# AREA 3: COLLOQUI AI
elif st.session_state.current_menu == "🤝 Colloqui AI":
    st.header("🤝 Sala Colloqui Virtuale con Assistente Silente")
    cand = st.selectbox("Seleziona Candidato", [c["nome"] for c in st.session_state.candidates])
    st.info(f"Pannello per avviare la conferenza online. L'IA registrerà la conversazione producendo lo skill summary finale.")

# AREA 4: ASSUNZIONI
elif st.session_state.current_menu == "🎉 Assunzioni":
    st.header("🎉 Conferma Assunzione Risorse")
    st.write("Modulo per la chiusura della risorsa e l'assegnazione finale al cliente di riferimento.")

# Altre aree (Semplificate per la struttura)
else:
    st.header(f"{st.session_state.current_menu}")
    st.write("Dati anagrafici e reportistica pronti per l'alimentazione del database.")
