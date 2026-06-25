import streamlit as st
import pandas as pd
import os

# Configurazione della pagina con layout largo e titolo personalizzato
st.set_page_config(page_title="Dei Reali - Dashboard", page_icon="👑", layout="wide")

# CSS Avanzato per replicare l'interfaccia esatta del mockup (Mockup 1000376179.png)
st.markdown("""
    <style>
    /* Sfondo generale grigio chiarissimo per dare profondità alle card bianche */
    .stApp {
        background-color: #F8FAFC;
        color: #0A2540;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Configurazione Sidebar Bianca Minimal */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 20px;
    }
    
    /* Titoli principali */
    .main-title {
        color: #031B4E !important;
        font-weight: 800 !important;
        font-size: 28px !important;
        margin-bottom: 2px !important;
    }
    .sub-title {
        color: #64748B !important;
        font-size: 14px !important;
        margin-bottom: 25px !important;
    }
    
    /* Stile per i pulsanti della barra di navigazione superiore */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #334155 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease;
        width: 100%;
        min-height: 55px;
    }
    div.stButton > button:hover {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
        background-color: #F0F7FF !important;
    }
    
    /* Stile per il pulsante attivo di navigazione */
    .active-nav button {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
        background-color: #F0F7FF !important;
    }

    /* Card bianche rialzate per i moduli */
    .custom-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0px 4px 6px -1px rgba(0, 0, 0, 0.05), 0px 2px 4px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
        height: 100%;
    }
    
    .card-header {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #031B4E !important;
        margin-bottom: 20px !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Simulatore Box di caricamento trascina-e-rilascia */
    .upload-box-sim {
        border: 2px dashed #CBD5E1;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        background-color: #F8FAFC;
        cursor: pointer;
        margin-bottom: 15px;
    }
    
    /* Pulsante principale di Azione Blu (Pubblica Annuncio) */
    .stButton .pub-btn-container button {
        background-color: #0052CC !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
    }
    .stButton .pub-btn-container button:hover {
        background-color: #0043A4 !important;
    }
    
    /* Badge monitoraggio laterali */
    .monitor-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        font-size: 13px;
        color: #475569;
    }
    .monitor-badge {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione dello Stato della Navigazione
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Annunci"
if 'jobs' not in st.session_state:
    st.session_state.jobs = []

# --- MENU LATERALE SINISTRO (SIDEBAR) ---
with st.sidebar:
    # Esposizione del Logo centrato
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h2 style='text-align:center; color:#031B4E;'>DEI REALI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748B; font-size:12px;'>Corporate Consulting</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Voci del menu laterale decorative (Stile elenco del mockup)
    st.markdown("""
        <div style='padding-left: 10px;'>
            <p style='color: #3B82F6; font-weight: 600; font-size: 14px; margin-bottom:18px;'>📊 Dashboard</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:18px;'>📢 Annunci</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:18px;'>🔍 Screening CV</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:18px;'>🤖 Colloqui AI</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:18px;'>👥 Assunzioni</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:18px;'>📈 Report</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:18px;'>🏢 Clienti</p>
            <p style='color: #475569; font-size: 14px; margin-bottom:18px;'>👤 Candidati</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Monitoraggio Applicativo in Basso (Incluso i badge numerici del mockup)
    st.markdown("<p style='font-size:11px; font-weight:700; color:#94A3B8; letter-spacing:0.5px;'>MONITORAGGIO APPLICATIVO</p>", unsafe_allow_html=True)
    st.markdown('<div class="monitor-row">👥 Utenti attivi <span class="monitor-badge">1/10</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="monitor-row">📄 CV in Database <span class="monitor-badge">2/10000</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="monitor-row"><span>⚡ AI Gemini</span> <span style="color:#22C55E; font-size:12px;">● pronta</span></div>', unsafe_allow_html=True)

# --- CONTENUTO PRINCIPALE ---
st.markdown('<p class="main-title">Sistema di Gestione & Selezione Personale</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Dashboard Operativa</p>', unsafe_allow_html=True)

# --- BARRA DI NAVIGAZIONE SUPERIORE A TASTI ---
nav_cols = st.columns(7)
menu_items = [
    ("📢 Annunci", "Annunci"), 
    ("📄 Screening CV", "Screening"), 
    ("🤖 Colloqui AI", "Colloqui"), 
    ("👥 Assunzioni", "Assunzioni"), 
    ("📊 Report", "Report"), 
    ("🏢 Clienti", "Clienti"), 
    ("👤 Candidati", "Candidati")
]

for idx, (label, key) in enumerate(menu_items):
    with nav_cols[idx]:
        # Applica classe CSS attiva se selezionato
        if st.session_state.current_menu == key:
            st.markdown('<div class="active-nav">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}"):
            st.session_state.current_menu = key
        if st.session_state.current_menu == key:
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- AREA DI LAVORO SELEZIONATA ---
if st.session_state.current_menu == "Annunci":
    
    col_sx, col_dx = st.columns(2)
    
    # CARD 1: DATI DELL'ANNUNCIO (A SINISTRA)
    with col_sx:
        st.markdown("""
            <div class="custom-card">
                <div class="card-header">📢 Creazione e Pubblicazione Annunci</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Elementi interni alla card sinistra
        st.markdown("*📋 Dati dell'Annuncio*")
        uploaded_img = st.file_uploader("Foto caricabile da locale", type=["png", "jpg", "jpeg"])
        
        titolo_job = st.text_input("Titolo della posizione", placeholder="Es. Senior Project Manager")
        
        st.markdown("*💰 Inquadramento Economico*")
        tipo_costo = st.selectbox("Seleziona la tipologia di costo", ["RAL (Annuale)", "Importo Lordo", "Costo Orario"])
        valore_costo = st.text_input("Valore economico (€)", placeholder="Es. 45.000 o 50/ora")
        
        indirizzo_job = st.text_input("📍 Indirizzo / Sede di lavoro", placeholder="Es. Via Condotti, Roma")
        
        st.markdown("*📞 Dati di Contatto*")
        c_tel, c_mail = st.columns(2)
        with c_tel:
            cellulare_job = st.text_input("Cellulare", placeholder="Es. +39 333 1234567")
        with c_mail:
            mail_job = st.text_input("E-mail di contatto", placeholder="Es. hr@deireali.com")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="pub-btn-container">', unsafe_allow_html=True)
        btn_pubblica = st.button("🚀 Pubblica annuncio")
        st.markdown('</div>', unsafe_allow_html=True)

    # CARD 2: ASSISTENTE AI (A DESTRA)
    with col_dx:
        st.markdown("""
            <div class="custom-card">
                <div class="card-header">✨ Assistente di Scrittura IA</div>
            </div>
        """, unsafe_allow_html=True)
        
        info_basiche = st.text_area("Inserisci le info base dell'annuncio per l'editing IA", placeholder="Es. Cerchiamo un esperto di consulenza aziendale per la sede di Roma...", height=150)
        tono = st.selectbox("Tono dell'editing", ["Professionale", "Istituzionale", "Moderno"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Ottimizza Annuncio con IA 🤖"):
            if titolo_job and info_basiche:
                st.session_state['preview_text'] = f"### {titolo_job}\n\n*Sede:* {indirizzo_job}\n*Compenso:* {valore_costo} ({tipo_costo})\n\n*Descrizione:\n{info_basiche}\n\nContatti:*\n✉️ {mail_job} | 📞 {cellulare_job}"
            else:
                st.error("Inserisci prima il titolo della posizione e le info base!")

        if 'preview_text' in st.session_state:
            st.markdown("<br><hr><b>🌐 Anteprima Pagina Web Generata:</b>", unsafe_allow_html=True)
            st.info(st.session_state['preview_text'])
            slug = titolo_job.lower().replace(" ", "-")
            st.code(f"https://deireali-hr.streamlit.app/jobs/{slug}")

else:
    # Sfondo o aree temporanee per gli altri menu della navigazione
    st.markdown(f"""
        <div class="custom-card">
            <div class="card-header">📬 Sezione {st.session_state.current_menu} in attesa di caricamento</div>
            <p style='color:#64748B;'>I moduli grafici per questa sezione seguiranno le linee guida del design prescelto.</p>
        </div>
    """, unsafe_allow_html=True)
