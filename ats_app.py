import streamlit as st
import pandas as pd
import os

# Configurazione ad altissimo impatto
st.set_page_config(page_title="Dei Reali ATS", page_icon="👑", layout="wide")

# Iniezione di FontAwesome per le icone e CSS Custom per azzerare lo stile base di Streamlit
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
    /* Reset e Sfondo Generale Deep Web App */
    .stApp {
        background-color: #F1F5F9 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* SIDEBAR TOTAL WHITE PREMIUM */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* TITOLI AD ALTO IMPATTO */
    .main-header {
        color: #0F172A !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin-top: -20px;
    }
    .sub-header {
        color: #64748B !important;
        font-size: 15px !important;
        margin-bottom: 30px;
    }
    
    /* CARD CONTENITORI STILE SAAS MODERNO */
    .saas-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 25px;
    }
    
    .card-title {
        color: #1E3A8A !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        margin-bottom: 20px;
        border-bottom: 2px solid #EFF6FF;
        padding-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* BARRA DI NAVIGAZIONE SUPERIORE COPIATA DAL MOCKUP */
    .nav-container {
        display: flex;
        gap: 12px;
        margin-bottom: 25px;
        overflow-x: auto;
        padding-bottom: 5px;
    }
    
    /* FORZATURA DEGLI INPUT DI STREAMLIT PER RENDERLI CORRETTI */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #0F172A !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }
    
    /* PULSANTE BLUE CORPORATE */
    div.stButton > button {
        background: linear-gradient(135deg, #1E40AF 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.3) !important;
    }
    
    /* BADGE LATERALE */
    .badge-sys {
        background-color: #F0FDF4;
        color: #166534;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione menu
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Annunci"

# --- SIDEBAR (LOGICA MINIMAL TOTAL WHITE) ---
with st.sidebar:
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Lista Navigazione Laterale Pulita
    st.markdown("""
        <div style='padding: 0 5px;'>
            <p style='color: #2563EB; font-weight: 700; font-size: 14px; margin-bottom:20px;'><i class='fa-solid fa-chart-pie' style='margin-right:10px;'></i> Dashboard Operativa</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:20px;'><i class='fa-solid fa-bullhorn' style='margin-right:10px;'></i> Annunci</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:20px;'><i class='fa-solid fa-file-pdf' style='margin-right:10px;'></i> Screening CV</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:20px;'><i class='fa-solid fa-robot' style='margin-right:10px;'></i> Colloqui AI</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:20px;'><i class='fa-solid fa-user-check' style='margin-right:10px;'></i> Assunzioni</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; font-weight:700; color:#94A3B8; letter-spacing:0.5px;'>MONITORAGGIO</p>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; color:#475569; margin-bottom:8px;'>Utenti attivi: <b>1/10</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; color:#475569; margin-bottom:15px;'>CV totali: <b>2/10000</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='badge-sys'><i class='fa-solid fa-circle' style='font-size:7px;'></i> AI Gemini Connessa</div>", unsafe_allow_html=True)

# --- CORPO CENTRALE ---
st.markdown('<p class="main-header">Sistema di Gestione & Selezione Personale</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Dashboard Operativa • Agenzia Dei Reali</p>', unsafe_allow_html=True)

# NAVIGAZIONE ORIZZONTALE AD IMPATTO (Sostituisce i vecchi bottoni grigi)
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
buttons = [("📢 Annunci", "Annunci"), ("📥 Screening", "Screening"), ("🤝 Colloqui AI", "Colloqui"), 
           ("🎉 Assunzioni", "Assunzioni"), ("📊 Report", "Report"), ("🏢 Clienti", "Clienti"), ("👥 Candidati", "Candidati")]

for i, (label, key) in enumerate(buttons):
    with [c1, c2, c3, c4, c5, c6, c7][i]:
        if st.button(label, key=f"btn_{key}"):
            st.session_state.current_menu = key

st.markdown("<br>", unsafe_allow_html=True)

# SEZIONE CONTENUTO: CARD DOPPIA
if st.session_state.current_menu == "Annunci":
    col_sx, col_dx = st.columns(2)
    
    with col_sx:
        st.markdown('<div class="saas-card"><div class="card-title"><i class="fa-solid fa-pen-to-square"></i> Dati dell\'Annuncio</div>', unsafe_allow_html=True)
        uploaded_img = st.file_uploader("Immagine di copertina annuncio", type=["png", "jpg", "jpeg"])
        titolo_job = st.text_input("Titolo della posizione lavorativa", placeholder="Es. Senior Corporate Consultant")
        
        st.markdown("<p style='font-weight:600; margin-top:15px; font-size:14px;'>Budget & Costo</p>", unsafe_allow_html=True)
        tipo_costo = st.selectbox("Seleziona inquadramento", ["RAL (Annuale)", "Importo Lordo", "Costo Orario"])
        valore_costo = st.text_input("Valore economico (€)", placeholder="Es. 50.000")
        
        indirizzo_job = st.text_input("Sede lavorativa", placeholder="Es. Via Condotti, Roma")
        
        st.markdown("<p style='font-weight:600; margin-top:15px; font-size:14px;'>Contatti Diretti</p>", unsafe_allow_html=True)
        cx1, cx2 = st.columns(2)
        with cx1: cellulare_job = st.text_input("Telefono", placeholder="Es. +39 333...")
        with cx2: mail_job = st.text_input("Email", placeholder="Es. hr@deireali.com")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 PUBBLICA ANNUNCIO SU WEB"):
            st.success("Annuncio pubblicato nell'indice globale!")
        st.markdown('</div>', unsafe_allow_html=True) # Chiusura Card

    with col_dx:
        st.markdown('<div class="saas-card"><div class="card-title"><i class="fa-solid fa-wand-magic-sparkles"></i> Assistente di Scrittura IA</div>', unsafe_allow_html=True)
        info_basiche = st.text_area("Cosa stai cercando? Inserisci note sparse:", placeholder="Cerchiamo una figura junior da inserire nel team di Roma...", height=180)
        tono = st.selectbox("Seleziona il tono del copywriter", ["Professionale Istituzionale", "Moderno Accattivante"])
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("✨ OTTIMIZZA CON INTELLIGENZA ARTIFICIALE"):
            st.info("Generazione del testo ottimizzato SEO in corso...")
        st.markdown('</div>', unsafe_allow_html=True) # Chiusura Card
