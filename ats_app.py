import streamlit as st
import pandas as pd
import os

# 1. Configurazione ad alto impatto (Layout largo)
st.set_page_config(
    page_title="Dei Reali - ATS Platform",
    page_icon="👑",
    layout="wide"
)

# 2. Forzatura CSS Professionale per rimuovere la dispersività e dare stacco visivo netto
st.markdown("""
    <style>
    /* Sfondo dell'app grigio-azzurro freddo per far risaltare i moduli bianchi */
    .stApp {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
    }
    
    /* Sidebar Bianca con bordo sottile ed elegante */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Pulizia dei titoli principali per renderli compatti e d'impatto */
    .main-title {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #031B4E !important;
        margin-top: -15px !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 13px !important;
        color: #64748B !important;
        margin-bottom: 20px !important;
    }
    
    /* Card Bianche con angoli arrotondati e ombreggiatura profonda stile SaaS Premium */
    .premium-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 15px !important;
    }
    
    /* Intestazioni delle aree interne alle card */
    .card-title {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #1E3A8A !important;
        margin-bottom: 15px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Etichette dei campi ridotte e scure per non disperdere l'occhio */
    label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #334155 !important;
    }
    
    /* Bottone Principale Sfumato ad alto impatto visivo */
    div.stButton > button {
        background: linear-gradient(135deg, #1E40AF 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.15) !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(30, 64, 175, 0.25) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione dello Stato della Navigazione
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "📢 Annunci"
if 'jobs' not in st.session_state:
    st.session_state.jobs = []

# --- MENU LATERALE (SIDEBAR) ---
with st.sidebar:
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h3 style='color:#031B4E; text-align:center;'>👑 DEI REALI</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:11px; font-weight:700; color:#94A3B8; letter-spacing:0.5px;'>MONITORAGGIO APPLICATIVO</p>", unsafe_allow_html=True)
    st.markdown("👥 Utenti attivi: <span style='color:#031B4E; font-weight:bold;'>1/10</span>", unsafe_allow_html=True)
    st.markdown("📄 CV nel Database: <span style='color:#031B4E; font-weight:bold;'>2/10000</span>", unsafe_allow_html=True)
    st.markdown("⚡ AI Gemini: <span style='color:#22C55E; font-weight:bold;'>● Pronta</span>", unsafe_allow_html=True)

# --- CORPO PRINCIPALE ---
st.markdown('<div class="main-title">Sistema di Gestione & Selezione Personale</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Dashboard
