import streamlit as st
import pandas as pd
import os
import random

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Corporate ATS & CRM",
    page_icon="👑",
    layout="wide"
)

# 2. CSS Custom per l'interfaccia Premium
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
    .saas-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione dei Database nella Sessione (se non già presenti)
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
            "Orientamento": "Perfetto per il ruolo. Spiccate doti di leadership aziendale.",
            "Alternativo": "Nessuno (Profilo ideale)"
        },
        {
            "Nome": "Beatrice Marchesi",
            "Email": "beatrice.m@outlook.it",
            "Posizione": "Senior Corporate Consultant",
            "Idoneità": "65%",
            "Stelle": "⭐⭐⭐",
            "Orientamento": "Buone competenze tecniche, ma mostra lacune lato Financial Modeling.",
            "Alternativo": "💡 Consigliata come 'Junior Financial Analyst'"
        }
    ]

if 'clienti_db' not in st.session_state:
    st.session_state.clienti_db = [
        {
            "Azienda": "Dei Reali Consulting",
            "Settore": "Consulenza Aziendale & HR",
            "Referente": "Direzione HR",
            "Email": "info@deireali.com",
            "Posizioni_Aperte": 2
        },
        {
            "Azienda": "Finanza & Sviluppo S.p.A.",
            "Settore": "Banking & Finance",
            "Referente": "Dott. Enrico Verdi",
            "Email": "e.verdi@finanzasviluppo.it",
            "Posizioni_Aperte": 1
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
    st.markdown("### 📊 STATISTICHE SUITE")
    st.metric(label="Candidati in Classifica", value=len(st.session_state.candidati_db))
    st.metric(label="Aziende Clienti Partner", value=len(st.session_state.clienti_db))
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; font-weight:700; color:#94A3B8;'>STATO SISTEMA</p>", unsafe_allow_html=True)
    st.markdown("🟢 Database Interno: *Attivo*", unsafe_allow_html=True)
    st.markdown("🤖 Screening Rank & Orientamento AI: *Pronti*", unsafe_allow_html=True)

# --- 4. AREA CENTRALE ---
st.title("💼 Sistema di Gestione & Selezione Personale")
st.markdown("##### Dashboard Operativa Integrata • Agenzia Dei Reali")
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

# --- 5. LOGICA DEI MODULI ---

# --- MODULO 1: ANNUNCI ---
if st.session_state.current_menu == "📢 Annunci":
    col_sx, col_dx = st.columns(2)
    with col_sx:
        st.markdown("### 📝 Dati dell'Annuncio")
        uploaded_img = st.file_uploader("🖼️ Foto o Copertina Annuncio", type=["png", "jpg", "jpeg"])
        titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. Senior Corporate Consultant")
        tipo_importo = st.radio("Inquadramento", ["RAL (Annua)", "Importo Lordo", "Costo Orario"], horizontal=True)
        valore_importo = st.text_input("Valore economico (€)", placeholder="es. 45.000")
        indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Via Condotti, Roma")
        
        st.markdown("*📞 Contatti*")
        cx1, cx2 = st.columns(2)
        with cx1: cellulare_job = st.text_input("Cellulare", placeholder="es. +39 333...")
        with cx2: mail_job = st.text_input("E-mail", placeholder="es. hr@deireali.com")
        
        if st.button("🚀 PUBBLICA NUOVO ANNUNCIO SU WEB", use_container_width=True):
            st.success("🎉 Annuncio indicizzato con successo nel sistema!")
            
    with col_dx:
        st.markdown("### 🤖 Assistente di Scrittura IA")
        info_basiche = st.text_area("Note e requisiti per il Copy dell'annuncio:", placeholder="Cerchiamo una figura...", height=210)
        tono = st.selectbox("Tono dell'editing", ["Professionale", "Istituzionale", "Moderno"])
        if st.button("🪄 OTTIMIZZA LAYOUT E CONTENUTO CON IA", use_container_width=True):
            st.info("Bozza ottimizzata generata correttamente.")

# --- MODULO 2: SCREENING CV & RANK IA ---
elif st.session_state.current_menu == "📥 Screening CV":
    st.markdown("### 📥 Caricamento CV & Analisi Predittiva Idoneità")
    st.markdown("Gestisci la classifica dei candidati, calcola l'affinità con l'annuncio e scopri il loro orientamento professionale alternativo consigliato dall'IA.")
    
    with st.expander("➕ Carica Manualmente un Nuovo Profilo / Curriculum", expanded=True):
        cx_nome, cx_mail = st.columns(2)
        with cx_nome: nuovo_nome = st.text_input("Nome e Cognome Candidato")
        with cx_mail: nuova_mail = st.text_input("Indirizzo E-mail")
        file_cv = st.file_uploader("Seleziona o trascina il file del CV (PDF / Word)", type=["pdf", "docx", "txt"])
        posizione_scelta = st.selectbox("Posizione desiderata", ["Senior Corporate Consultant", "Project Manager", "Financial Analyst"])
        
        if st.button("⚡ VALUTA COMPATIBILITÀ E ORIENTAMENTO CON IA", use_container_width=True):
            if nuovo_nome and nuova_mail:
                percentuale_random = random.randint(50, 97)
                stelle_simolate = "⭐" * (percentuale_random // 20 + 1)
                
                if percentuale_random < 70:
                    orientamento_simulato = "Il candidato mostra solide soft-skills ma competenze tecniche parziali per questo specifico annuncio."
                    alternativo_simulato = f"💡 Consigliato come: 'Junior Assistant' o ricollocamento in area Back-Office."
                else:
                    orientamento_simulato = "Ottimo bilanciamento tra background accademico ed esperienze sul campo."
                    alternativo_simulato = "Nessuno (Profilo perfettamente in linea con le richieste)"
                
                st.session_state.candidati_db.append({
                    "Nome": nuovo_nome,
                    "Email": nuova_mail,
                    "Posizione": posizione_scelta,
                    "Idoneità": f"{percentuale_random}%",
                    "Stelle": stelle_simolate,
                    "Orientamento": orientamento_simulato,
                    "Alternativo": alternativo_simulato
                })
                st.success(f"📊 Classificazione completata per {nuovo_nome}!")
            else:
                st.error("Inserisci Nome e Mail per processare il profilo.")

    st.markdown("<br>## 🏆 Graduatoria di Idoneità AI dei Candidati", unsafe_allow_html=True)
    for cand in st.session_state.candidati_db:
        st.markdown(f"""
        <div class="saas-box">
            <table style="width:100%; border:none; border-collapse: collapse;">
                <tr>
                    <td style="width:70%; vertical-align: top;">
                        <h4 style="margin:0; color:#1E3A8A;">👤 {cand['Nome']}</h4>
                        <p style="margin:5px 0; color:#64748B; font-size:13px;">📧 {cand['Email']} &nbsp;|&nbsp; 🎯 Candidato per: <b>{cand['Posizione']}</b></p>
                        <p style="margin:10px 0 5px 0; font-size:14px;"><b>🧠 Idoneità al Ruolo (IA):</b> {cand['Orientamento']}</p>
                        <p style="margin:0; font-size:14px; color:#2563EB;"><b>🔄 Orientamento Alternativo Sconsigliato/Consigliato:</b> {cand['Alternativo']}</p>
                    </td>
                    <td style="text-align:right; width:30%; vertical-align: middle;">
                        <div style="font-size: 26px; font-weight:800; color:#1E40AF;">{cand['Idoneità']}</div>
                        <div style="font-size: 16px; margin-top:2px;">{cand['Stelle']}</div>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

# --- MODULO 6: GESTIONE CLIENTI (CRM AZIENDE) ---
elif st.session_state.current_menu == "🏢 Clienti":
    st.markdown("### 🏢 Anagrafica Clienti & Aziende Partner")
    st.markdown("Monitora le aziende mandanti, i referenti interni e il numero di ricerche di personale attive per ciascun cliente.")
    
    with st.expander("➕ Registra una Nuova Azienda Cliente Partner", expanded=False):
        c_az, c_set = st.columns(2)
        with c_az: nome_azienda = st.text_input("Ragione Sociale / Nome Azienda")
        with c_set: settore_azienda = st.text_input("Settore Industriale", placeholder="es. Tech, Luxury, Finance")
        
        c_ref, c_m = st.columns(2)
        with c_ref: referente_azienda = st.text_input("Nome Referente / HR Manager")
        with c_m: mail_azienda = st.text_input("E-mail Referente")
        
        posizioni_attive = st.number_input("Numero di Annunci/Ricerche affidate a Dei Reali", min_value=0, value=1, step=1)
        
        if st.button("💾 SALVA AZIENDA NEL DATABASE", use_container_width=True):
            if nome_azienda and referente_azienda:
                st.session_state.clienti_db.append({
                    "Azienda": nome_azienda,
                    "Settore": settore_azienda,
                    "Referente": referente_azienda,
                    "Email": mail_azienda,
                    "Posizioni_Aperte": int(posizioni_attive)
                })
                st.success(f"🏢 Azienda '{nome_azienda}' registrata correttamente nei sistemi centrali!")
            else:
                st.error("Compila almeno il Nome Azienda e il Referente per salvare.")

    st.markdown("<br>## 📋 Elenco Aziende Partner Sincronizzate", unsafe_allow_html=True)
    for cli in st.session_state.clienti_db:
        st.markdown(f"""
        <div class="saas-box">
            <table style="width:100%; border:none; border-collapse: collapse;">
                <tr>
                    <td style="width:75%; vertical-align: top;">
                        <h4 style="margin:0; color:#0F172A;">🏢 {cli['Azienda']}</h4>
                        <p style="margin:4px 0; color:#64748B; font-size:13px;">💼 Settore: <b>{cli['Settore']}</b> &nbsp;|&nbsp; 📧 Contatto: {cli['Email']}</p>
                        <p style="margin:8px 0 0 0; font-size:14px; color:#334155;">👤 Referente Interno: <b>{cli['Referente']}</b></p>
                    </td>
                    <td style="text-align:right; width:25%; vertical-align: middle;">
                        <span style="background-color: #F1F5F9; border: 1px solid #CBD5E1; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; color: #1E3A8A;">
                            📂 {cli['Posizioni_Aperte']} Ricerche Attive
                        </span>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

else:
    # Schermata provvisoria per gli altri pulsanti
    st.info(f"Il pannello relativo a *{st.session_state.current_menu}* è operativo. I moduli interattivi si popoleranno automaticamente non appena integreremo le restanti tabelle dati.")
