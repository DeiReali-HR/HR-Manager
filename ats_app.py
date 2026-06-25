import streamlit as st
import pandas as pd
import os

# Configurazione della pagina ad alto impatto grafico
st.set_page_config(
    page_title="Dei Reali - Corporate Consulting",
    page_icon="👑",
    layout="wide"
)

# Configurazione del tema nativo pulito e moderno (Bianco, Azzurro e Blu)
st.markdown("""
    <style>
    /* Sfondo generale dell'applicazione (Grigio azzurrato molto chiaro e pulito) */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    
    /* Sidebar Bianca minimale ed elegante */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Nasconde i menu standard di Streamlit per un look 100% software proprietario */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Stile per i titoli */
    .main-title {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
        margin-bottom: 2px !important;
    }
    .sub-title {
        font-size: 14px !important;
        color: #64748B !important;
        margin-bottom: 25px !important;
    }
    
    /* Card personalizzate staccate dallo sfondo */
    .saas-container {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.02) !important;
        margin-bottom: 20px !important;
    }
    
    .card-header {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1E3A8A !important;
        margin-bottom: 15px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione dello Stato del Menu
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "📢 Annunci"
if 'jobs' not in st.session_state:
    st.session_state.jobs = []

# --- 1. MENU LATERALE (SIDEBAR) ---
with st.sidebar:
    # Mostra il logo se presente
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h2 style='text-align:center; color:#1E3A8A;'>👑 DEI REALI</h2>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Navigazione verticale pulita (stile SaaS) usando i radio nativi ma stilizzati
    st.markdown("<b>📌 NAVIGAZIONE</b>", unsafe_allow_html=True)
    scelta = st.radio(
        label="Menu",
        options=["📢 Annunci", "📥 Screening CV", "🤝 Colloqui AI", "🎉 Assunzioni", "📊 Report", "🏢 Clienti", "👥 Candidati"],
        label_visibility="collapsed"
    )
    st.session_state.current_menu = scelta
    
    st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; font-weight:700; color:#94A3B8; letter-spacing:0.5px;'>MONITORAGGIO SISTEMA</p>", unsafe_allow_html=True)
    st.markdown("👥 Utenti attivi: <span style='color:#1E3A8A; font-weight:bold;'>1/10</span>", unsafe_allow_html=True)
    st.markdown("📄 CV nel Database: <span style='color:#1E3A8A; font-weight:bold;'>2/10000</span>", unsafe_allow_html=True)
    st.markdown("⚡ AI Gemini: <span style='color:#22C55E; font-weight:bold;'>● Collegata</span>", unsafe_allow_html=True)

# --- 2. CONTENUTO PRINCIPALE ---
st.markdown(f'<div class="main-title">Dei Reali — Corporate Suite</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Gestione Risorse Umane & Selezione ATS • Area {st.session_state.current_menu}</div>', unsafe_allow_html=True)

# GESTIONE DEI MODULI
if st.session_state.current_menu == "📢 Annunci":
    
    col_sx, col_dx = st.columns(2)
    
    # Sezione di Sinistra: Input Dati
    with col_sx:
        st.markdown('<div class="saas-container">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📝 Creazione Nuovo Annuncio</div>', unsafe_allow_html=True)
        
        uploaded_img = st.file_uploader("🖼️ Foto o Copertina dell'Annuncio", type=["png", "jpg", "jpeg"])
        titolo_job = st.text_input("📍 Titolo della Posizione", placeholder="Es. Senior Corporate Consultant")
        
        st.markdown("<br><b>💰 Inquadramento Economico</b>", unsafe_allow_html=True)
        tipo_tariffa = st.selectbox("Tipologia di compenso", ["RAL (Annua)", "Importo Lordo", "Costo Orario"])
        valore_importo = st.text_input("Valore (€)", placeholder="Es. 45.000")
        
        indirizzo_job = st.text_input("🏢 Sede di Lavoro / Indirizzo", placeholder="Es. Via Condotti, Roma")
        
        st.markdown("<br><b>📞 Dati di Contatto Rapido</b>", unsafe_allow_html=True)
        c_tel, c_mail = st.columns(2)
        with c_tel:
            cellulare_job = st.text_input("Cellulare", placeholder="Es. +39 333 1234567")
        with c_mail:
            mail_job = st.text_input("E-mail", placeholder="Es. hr@deireali.com")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 PUBBLICA ANNUNCIO ONLINE", use_container_width=True):
            if titolo_job:
                slug = titolo_job.lower().replace(" ", "-")
                st.success(f"🎉 Annuncio pubblicato! Raggiungibile su: deireali-hr.streamlit.app/jobs/{slug}")
            else:
                st.error("Inserisci almeno il titolo della posizione!")
                
        st.markdown
