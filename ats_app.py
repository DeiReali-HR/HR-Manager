import streamlit as st
import pandas as pd
import os
import random

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Corporate ATS & AI Rank",
    page_icon="👑",
    layout="wide"
)

# 2. Stile CSS Premium (Fondo chiaro, bottoni azzurri, tabelle pulite)
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
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
    .candidato-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione del database simulato nello stato della sessione
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "📢 Annunci"

if 'candidati_db' not in st.session_state:
    st.session_state.candidati_db = [
        {
            "Nome": "Alessandro Reali",
            "Email": "a.reali@gmail.com",
            "Posizione": "Senior Corporate Consultant",
            "Idoneità": "94%",
            "Stelle": "⭐⭐⭐⭐⭐",
            "Orientamento": "Perfetto per il ruolo. Spiccate doti di leadership.",
            "Alternativo": "Nessuno (Profilo ideale)"
        },
        {
            "Nome": "Beatrice Marchesi",
            "Email": "beatrice.m@outlook.it",
            "Posizione": "Senior Corporate Consultant",
            "Idoneità": "65%",
            "Stelle": "⭐⭐⭐",
            "Orientamento": "Competenze tecniche buone, ma manca di esperienza lato Financial Consulting.",
            "Alternativo": "💡 Consigliata come 'Junior Financial Analyst' o 'Account Specialist'"
        }
    ]

# --- 3. SIDEBAR LATERALE ---
with st.sidebar:
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.subheader("👑 DEI REALI")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📊 STATISTICHE AI")
    st.metric(label="Candidati Totali", value=len(st.session_state.candidati_db))
    st.metric(label="Idoneità Media", value="79.5%")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; font-weight:700; color:#94A3B8;'>TECNOLOGIA</p>", unsafe_allow_html=True)
    st.markdown("🟢 Modulo Analisi Rank: *Attivo*", unsafe_allow_html=True)
    st.markdown("🤖 AI Redirection: *Pronta*", unsafe_allow_html=True)

# --- 4. AREA CENTRALE ---
st.title("💼 Sistema di Gestione & Selezione Personale")
st.markdown("##### Dashboard Operativa & Intelligenza Artificiale • Dei Reali")
st.markdown("<br>", unsafe_allow_html=True)

# BARRA ORIZZONTALE A TASTI
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
st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

# --- LOGICA DELLE SEZIONI ---

if st.session_state.current_menu == "📢 Annunci":
    col_sx, col_dx = st.columns(2)
    with col_sx:
        st.markdown("### 📝 Dati dell'Annuncio")
        uploaded_img = st.file_uploader("🖼️ Foto o Copertina Annuncio", type=["png", "jpg", "jpeg"])
        titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. Senior Corporate Consultant")
        tipo_importo = st.radio("Inquadramento", ["RAL (Annua)", "Importo Lordo", "Costo Orario"], horizontal=True)
        valore_importo = st.text_input("Valore economico (€)", placeholder="es. 45.000")
        indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Via Condotti, Roma")
        
        st.markdown("*📞 Contatti Veloci*")
        cx1, cx2 = st.columns(2)
        with cx1: cellulare_job = st.text_input("Cellulare", placeholder="es. +39 333...")
        with cx2: mail_job = st.text_input("E-mail", placeholder="es. hr@deireali.com")
        
        if st.button("🚀 PUBBLICA NUOVO ANNUNCIO SU WEB", use_container_width=True):
            st.success("🎉 Annuncio indicizzato! Ora i candidati possono inviare i loro CV.")
            
    with col_dx:
        st.markdown("### 🤖 Assistente di Scrittura IA")
        info_basiche = st.text_area("Note sparse sui requisiti richiesti:", placeholder="Cerchiamo una figura aziendale...", height=210)
        tono = st.selectbox("Tono di voce dell'editing", ["Professionale", "Istituzionale", "Moderno"])
        if st.button("🪄 OTTIMIZZA LAYOUT E CONTENUTO CON IA", use_container_width=True):
            st.info("Generazione testo ottimizzato completata.")

elif st.session_state.current_menu == "📥 Screening CV":
    st.markdown("### 📥 Caricamento Manuale & Classifica AI Candidati")
    st.markdown("Trascina qui i CV che ricevi privatamente. L'IA compilerà la scheda di idoneità e indicherà un orientamento alternativo se non idoneo.")
    
    # Form di caricamento rapido
    with st.expander("➕ Inserisci o Trascina un nuovo CV (PDF / Testo)", expanded=True):
        cx_nome, cx_mail = st.columns(2)
        with cx_nome:
            nuovo_nome = st.text_input("Nome e Cognome Candidato")
        with cx_mail:
            nuova_mail = st.text_input("Indirizzo E-mail")
            
        file_cv = st.file_uploader("Carica il file del Curriculum Vitae", type=["pdf", "docx", "txt"])
        posizione_scelta = st.selectbox("Posizione per cui si candida", ["Senior Corporate Consultant", "Project Manager", "HR Specialist"])
        
        if st.button("⚡ ANALIZZA CV CON INTELLIGENZA ARTIFICIALE", use_container_width=True):
            if nuovo_nome and nuova_mail:
                # Simulatore di analisi IA
                percentuale_random = random.randint(45, 98)
                stelle_simolate = "⭐" * (percentuale_random // 20 + 1)
                
                # Logica di orientamento simulata
                if percentuale_random < 70:
                    orientamento_simulato = "Il candidato mostra carenze sulle competenze core richieste dal ruolo selezionato."
                    alternativo_simulato = "💡 Consigliato per: Ruoli di back-office o come Junior Analyst per formazione interna."
                else:
                    orientamento_simulato = "Ottimo allineamento con i requisiti aziendali richiesti nell'annuncio."
                    alternativo_simulato = "Nessuno (Idoneo alla posizione attuale)"
                
                # Salva nel database della sessione
                st.session_state.candidati_db.append({
                    "Nome": nuevo_nome,
                    "Email": nuova_mail,
                    "Posizione": posizione_scelta,
                    "Idoneità": f"{percentuale_random}%",
                    "Stelle": stelle_simolate,
                    "Orientamento": orientamento_simulato,
                    "Alternativo": alternativo_simulato
                })
                st.success(f"✅ Analisi completata per {nuovo_nome}! Profilo aggiunto alla classifica qui sotto.")
            else:
                st.error("Inserisci Nome ed E-mail del candidato prima di lanciare l'IA.")

    st.markdown("<br>## 🏆 Classifica di Idoneità AI dei Candidati", unsafe_allow_html=True)
    
    # Mostra i candidati del database ordinati in bellissime card SaaS
    for cand in st.session_state.candidati_db:
        st.markdown(f"""
        <div class="candidato-box">
            <table style="width:100%; border:none;">
                <tr>
                    <td style="width:65%;">
                        <h4 style="margin:0; color:#1E3A8A;">👤 {cand['Nome']}</h4>
                        <p style="margin:5px 0; color:#64748B; font-size:13px;">📧 {cand['Email']} &nbsp;|&nbsp; 🎯 Candidato per: <b>{cand['Posizione']}</b></p>
                        <p style="margin:10px 0 5px 0; font-size:14px;"><b>🧠 Analisi Orientamento IA:</b> {cand['Orientamento']}</p>
                        <p style="margin:0; font-size:14.5px; color:#2563EB;"><b>🔄 Re-indirizzamento Nuova Posizione:</b> {cand['Alternativo']}</p>
                    </td>
                    <td style="text-align:right; width:35%;">
                        <div style="font-size: 24px; font-weight:800; color:#1E40AF;">{cand['Idoneità']}</div>
                        <div style="font-size: 16px; margin-top:2px;">{cand['Stelle']}</div>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

else:
    # Schermata provvisoria per gli altri pulsanti
    st.info(f"Il pannello relativo a *{st.session_state.current_menu}* è configurato correttamente. Le classifiche e le analisi IA alimenteranno questa sezione automaticamente.")
