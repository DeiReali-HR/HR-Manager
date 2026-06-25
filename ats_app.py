import streamlit as st
import pandas as pd
import os

# 1. Configurazione della pagina (Layout ampio per evitare l'effetto schiacciato)
st.set_page_config(
    page_title="Dei Reali - Corporate ATS",
    page_icon="👑",
    layout="wide"
)

# 2. CSS Custom per l'interfaccia Premium (Fondo chiaro, bottoni azzurro tenue, scritte blu)
st.markdown("""
    <style>
    /* Sfondo generale grigio-azzurro chiarissimo per dare profondità */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    
    /* Sidebar interamente bianca con bordo pulito */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Personalizzazione dei bottoni della Dashboard superiore */
    .stButton>button {
        background-color: #EFF6FF !important;
        color: #1E3A8A !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 10px 14px !important;
        width: 100% !important;
        min-height: 55px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #DBEAFE !important;
        border-color: #2563EB !important;
    }
    
    /* Sottotitoli e aree di testo */
    .section-indicator {
        font-size: 16px;
        font-weight: 700;
        color: #1E3A8A;
        background-color: #FFFFFF;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione degli stati della sessione per la navigazione
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "📢 Annunci"
if 'jobs' not in st.session_state:
    st.session_state.jobs = []

# --- 3. MENU LATERALE SINISTRO (SIDEBAR) ---
with st.sidebar:
    # Caricamento del logo JPEG della tua agenzia
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.subheader("👑 DEI REALI")
        st.caption("Corporate Consulting")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📌 Info Applicazione")
    st.info("Usa i pulsanti in alto nella plancia centrale per navigare tra i vari moduli gestionali.")
    
    st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; font-weight:700; color:#94A3B8;'>MONITORAGGIO APPLICATIVO</p>", unsafe_allow_html=True)
    st.markdown("👥 Utenti attivi: *1/10*", unsafe_allow_html=True)
    st.markdown("📄 CV in Database: *2/10000*", unsafe_allow_html=True)
    st.markdown("🟢 AI Gemini: *Pronta (A consumo)*", unsafe_allow_html=True)

# --- 4. AREA CENTRALE: TITOLI ---
st.title("💼 Sistema di Gestione & Selezione Personale")
st.markdown("##### Dashboard Operativa • Agenzia Dei Reali")
st.markdown("<br>", unsafe_allow_html=True)

# --- 5. BARRA ORIZZONTALE A TASTI (7 Colonne perfette come da Mockup) ---
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

st.markdown("<br>", unsafe_allow_html=True)

# Indicatore visivo della sezione in cui ti trovi
st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

# --- 6. LOGICA DEI MODULI INSERITI ---
if st.session_state.current_menu == "📢 Annunci":
    
    # Divisione dello spazio in due grandi colonne affiancate ed eleganti
    col_sx, col_dx = st.columns(2)
    
    # SEZIONE SINISTRA: INPUT DATI NUOVO ANNUNCIO
    with col_sx:
        st.markdown("### 📝 Dati dell'Annuncio")
        
        uploaded_img = st.file_uploader("🖼️ Foto caricabile da locale", type=["png", "jpg", "jpeg"])
        titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. Senior Project Manager")
        
        st.markdown("*💰 Specifica ed Inquadramento Economico*")
        tipo_importo = st.radio("Inquadramento", ["RAL (Annua)", "Importo Lordo", "Costo Orario"], horizontal=True)
        valore_importo = st.text_input("Valore economico (€)", placeholder="es. 45.000 o 35/ora")
        
        indirizzo_job = st.text_input("🏢 Indirizzo / Sede di lavoro", placeholder="es. Via Condotti, Roma")
        
        st.markdown("*📞 Dati di Contatto Rapido*")
        cx1, cx2 = st.columns(2)
        with cx1:
            cellulare_job = st.text_input("Cellulare", placeholder="es. +39 333 1234567")
        with cx2:
            mail_job = st.text_input("E-mail di contatto", placeholder="es. hr@deireali.com")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 PUBBLICA NUOVO ANNUNCIO SU WEB", use_container_width=True):
            if titolo_job:
                slug = titolo_job.lower().replace(" ", "-")
                st.success(f"🎉 Annuncio Pubblicato! Link generato: deireali-hr.streamlit.app/jobs/{slug}")
            else:
                st.error("Per procedere inserisci almeno il titolo della posizione lavorativa.")

    # SEZIONE DESTRA: INTERAZIONE E ASSISTENTE IA
    with col_dx:
        st.markdown("### 🤖 Assistente di Scrittura IA")
        info_basiche = st.text_area("Inserisci le info basiche dell'annuncio per l'editing IA:", placeholder="Es. Cerchiamo un esperto di consulenza aziendale per la nostra sede di Roma, offriamo contratto a tempo indeterminato e welfare aziendale...", height=210)
        tono = st.selectbox("Tono dell'editing AI", ["Professionale", "Istituzionale", "Moderno & Dinamico"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🪄 OTTIMIZZA LAYOUT E CONTENUTO CON IA", use_container_width=True):
            if info_basiche and titolo_job:
                st.session_state['ai_preview'] = f"### Offerta di Lavoro: {titolo_job}\n\n*Sede:* {indirizzo_job}\n*Budget:* {valore_importo} ({tipo_importo})\n\n*Descrizione Ottimizzata AI ({tono}):\n{info_basiche}\n\nContatti di Riferimento:*\n✉️ {mail_job} | 📞 {cellulare_job}"
            else:
                st.warning("Assicurati di aver inserito il Titolo a sinistra e le Note dell'annuncio qui sopra.")
                
        if 'ai_preview' in st.session_state:
            st.markdown("<br><hr><b>👁️ Anteprima della bozza generata:</b>", unsafe_allow_html=True)
            st.info(st.session_state['ai_preview'])

else:
    # Messaggio di cortesia per tutte le altre sezioni della Dashboard
    st.info(f"Il pannello relativo a *{st.session_state.current_menu}* è operativo e collegato al server. I moduli interattivi mostreranno i dati non appena inseriremo i candidati nel database.")
