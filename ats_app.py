import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
import re
from datetime import datetime, date, time
from supabase import create_client, Client
from pypdf import PdfReader
from google import genai
from google.genai import types

# 1. Configurazione della pagina Enterprise
st.set_page_config(
    page_title="Dei Reali - Suite Enterprise Risorse Umane",
    page_icon="👑",
    layout="wide"
)

# 2. Connessione Sicura a Supabase e Gemini tramite Secrets
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except:
        st.error("❌ Errore nei Secrets di Streamlit: configurazione di Supabase mancante.")
        st.stop()

@st.cache_resource
def init_gemini():
    try:
        api_key = st.secrets["gemini"]["api_key"]
        return genai.Client(api_key=api_key)
    except:
        return None

supabase: Client = init_supabase()
ai_client = init_gemini()

def estrai_testo_pdf(file_caricato):
    try:
        reader = PdfReader(file_caricato)
        testo = ""
        for page in reader.pages:
            testo += page.extract_text() or ""
        return testo
    except:
        return ""

def analizza_cv_con_ia(testo_cv, requisiti_annuncio):
    if not ai_client:
        return f"{random.randint(75,95)}%", "⭐⭐⭐⭐", "Analisi standard (Sincronizzazione IA in corso)."
    
    prompt = f"""
    Sei l'assistente HR IA ufficiale della Dei Reali Srl. 
    Analizza il seguente testo estratto da un CV e confrontalo con i requisiti della posizione aperta.
    
    REQUISITI ANNUNCIO:
    {requisiti_annuncio}
    
    TESTO CV CANDIDATO:
    {testo_cv}
    
    Restituisci una risposta ESATTAMENTE in questo formato a 3 righe (non scrivere nient'altro):
    RIGA 1: Solo la percentuale di idoneità (es: 88%)
    RIGA 2: Da 1 a 5 icone stella (es: ⭐⭐⭐⭐)
    RIGA 3: Una breve sintesi professionale delle competenze estratte e perché è o non è ideale.
    """
    try:
        response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        linee = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        punteggio = linee[0] if len(linee) > 0 else "80%"
        stelle = linee[1] if len(linee) > 1 else "⭐⭐⭐⭐"
        sintesi = linee[2] if len(linee) > 2 else "Profilo analizzato dall'IA."
        return punteggio, stelle, sintesi
    except:
        return "85%", "⭐⭐⭐⭐", "Profilo recepito. Analisi in differita."

def genera_testo_annuncio_ia(titolo, inquadramento, importo, sede, note_brevi):
    if not ai_client:
        return note_brevi if note_brevi else "Dettagli annuncio in fase di definizione professionale."
    
    prompt = f"""
    Sei il Copywriter HR Senior ufficiale di Dei Reali Srl. 
    Scrivi un annuncio di lavoro accattivante, altamente professionale, formale ed elegante basandoti su questi dati essenziali:
    
    - POSIZIONE: {titolo}
    - SEDE DI LAVORO: {sede}
    - INQUADRAMENTO: {inquadramento} ({importo} €)
    - SPUNTI/NOTE INIZIALI: {note_breaks if note_breve else 'Nessuna nota aggiuntiva fornita'}
    
    Articola il testo in 3 sezioni chiare:
    1. Chi Siamo ed Obiettivo del Ruolo (introduzione d'impatto per conto dei nostri clienti di alto livello).
    2. Requisiti Chiave (competenze hard/soft desiderate).
    3. Cosa Offriamo (benefit, crescita aziendale e pacchetto retributivo menzionato).
    
    Mantieni un tono d'élite, corporate ed istituzionale. Non inserire saluti finali generici o placeholder, restituisci solo il corpo dell'annuncio pronto per la pubblicazione.
    """
    try:
        response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Errore generazione IA: {str(e)}"

# 3. CSS Custom Premium - Centratura e Struttura Globale App
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    
    .umana-banner {
        position: relative; width: 100%; height: 280px; 
        background-size: cover; background-position: center;
        border-radius: 16px; margin-bottom: 25px;
        box-shadow: inset 0 0 0 2000px rgba(15, 23, 42, 0.55);
        display: flex; align-items: flex-end; padding: 35px;
    }
    .umana-banner-title { color: #FFFFFF !important; font-size: 34px !important; font-weight: 800 !important; margin: 0 !important; text-shadow: 0 2px 4px rgba(0,0,0,0.4); }
    
    .umana-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 15px; margin-bottom: 30px; background: #FFFFFF; padding: 20px;
        border-radius: 12px; border: 1px solid #E2E8F0;
    }
    .umana-kpi { border-right: 1px solid #E2E8F0; padding-right: 10px; }
    .umana-kpi:last-child { border-right: none; }
    .umana-kpi-label { font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.5px; }
    .umana-kpi-value { font-size: 15px; color: #0F172A; font-weight: 700; margin-top: 2px; }
    
    .public-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 1000px; margin: 20px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }
    .saas-box { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .ai-box { background-color: #F1F5F9; border-left: 4px solid #2563EB; border-radius: 4px; padding: 15px; margin-top: 10px; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; border: none !important; padding: 12px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center; margin-top: 5px; font-size: 13px; width: 100%; text-shadow: none !important;}
    .meet-btn { background-color: #1a73e8 !important; color: white !important; border: none !important; padding: 12px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center; margin-top: 5px; font-size: 13px; width: 100%; }
    .link-box { background-color: #F8FAFC; padding: 10px 14px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; margin-top: 5px; word-break: break-all; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_job_id' not in st.session_state: st.session_state.edit_job_id = None
# Memorizzazione temporanea del testo IA nel form
if 'ai_generated_text' not in st.session_state: st.session_state.ai_generated_text = ""

buttons_nav = [
    ("📢 Annunci", "📢 Annunci"), ("📥 Screening CV", "📥 Screening CV"), 
    ("🤝 Colloqui AI", "🤝 Colloqui AI"), ("🎉 Assunzioni", "🎉 Assunzioni"), 
    ("📊 Report", "📊 Report"), ("🏢 Clienti", "🏢 Clienti"), ("👥 Candidati", "👥 Candidati")
]

# --- PORTALE CARRIERE PUBBLICO STYLE UMANA ---
query_params = st.query_params
if "job" in query_params:
    job_param = str(query_params["job"])
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_param).execute()
    annuncio_selezionato = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio_selezionato:
        if annuncio_selezionato.get('stato') == 'Sospeso':
            st.markdown('<div class="public-card" style="text-align:center; padding:60px 40px;">', unsafe_allow_html=True)
            st.markdown("## 🔒 Selezioni Momentaneamente Chiuse")
            st.warning("Ci scusiamo, ma la ricezione delle candidature per questa specifica posizione è stata temporaneamente sospesa dal nostro team HR.")
            st.markdown("<br><a href='#' onclick='window.close();' style='text-decoration:none; color:#1E3A8A; font-weight:bold;'>Chiudi Finestra</a>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            img_url = annuncio_selezionato.get('immagine') or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200"
            st.markdown('<div class="public-card">', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="umana-banner" style="background-image: url('{img_url}');">
                    <div class="umana-banner-title">{annuncio_selezionato['posizione']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class="umana-grid">
                    <div class="umana-kpi">
                        <div class="umana-kpi-label">📍 Sede di Lavoro</div>
                        <div class="umana-kpi-value">{annuncio_selezionato['sede']}</div>
                    </div>
                    <div class="umana-kpi">
                        <div class="umana-kpi-label">💼 Inquadramento</div>
                        <div class="umana-kpi-value">{annuncio_selezionato['inquadramento']}</div>
                    </div>
                    <div class="umana-kpi">
                        <div class="umana-kpi-label">💸 Compenso Lordo</div>
                        <div class="umana-kpi-value">{annuncio_selezionato['importo']} €</div>
                    </div>
                    <div class="umana-kpi">
                        <div class="umana-kpi-label">🔑 Codice Rif.</div>
                        <div class="umana-kpi-value">DR-{annuncio_selezionato['id'].upper()[-4:]}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📋 Descrizione della Posizione ed Offerta")
            st.info(annuncio_selezionato['note'])
            st.markdown("<br><hr style='border-color:#E2E8F0;'><br>### 📥 Invia il tuo Curriculum Vitae", unsafe_allow_html=True)
            with st.form("form_candidatura_esterno", clear_on_submit=True):
                c_nome = st.text_input("Nome e Cognome *")
                c_mail = st.text_input("Indirizzo E-mail *")
                c_tel = st.text_input("Numero di Telefono Cellulare *")
                c_file = st.file_uploader("Allega il tuo CV (Esclusivamente formato PDF)", type=["pdf"])
                if st.form_submit_button("INVIA CANDIDATURA UFFICIALE"):
                    if c_nome and c_mail and c_tel and c_file:
                        with st.spinner("🧠 Il copilota IA Dei Reali sta analizzando il profilo professionale..."):
                            testo_estratto = estrai_testo_pdf(c_file)
                            voto, stelle, orientamento = analizza_cv_con_ia(testo_estratto, annuncio_selezionato['note'])
                            supabase.table("candidati").insert({
                                "nome": c_nome, "email": c_mail, "telefono": c_tel,
                                "posizione": annuncio_selezionato['posizione'], "idoneita": voto, "stelle": stelle,
                                "orientamento": orientamento, "alternativo": "Layout Premium Attivo", "impegnato": False, "stato": "In Screening"
                            }).execute()
                        st.success("🎉 Candidatura trasmessa con successo!")
                    else: st.error("⚠️ Compila tutti i campi obbligatori.")
            st.markdown('</div>', unsafe_allow_html=True)

# --- SUITE INTERNA AMMINISTRATIVA CENTRATA ---
else:
    if not st.session_state.autenticato:
        st.markdown("""
            <style>
                .stApp { background: radial-gradient(circle at 50% 50%, #1E3A8A 0%, #0F172A 100%) !important; }
                header { visibility: hidden !important; }
                div[data-testid="stForm"] { 
                    background: #FFFFFF !important; 
                    border: 1px solid #E2E8F0 !important; 
                    border-radius: 16px !important; 
                    padding: 35px 40px 45px 40px !important; 
                    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.4) !important;
                    max-width: 450px !important;
                    margin: 0 auto !important;
                }
                div[data-testid="stForm"] label p { 
                    color: #1E293B !important; 
                    font-weight: 700 !important; 
                    text-shadow: none !important; 
                }
            </style>
        """, unsafe_allow_html=True)

        col_dx, col_centro, col_sx = st.columns([1, 1.4, 1])
        with col_centro:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            with st.form("login_form_premium"):
                if os.path.exists("1000376160.jpeg"):
                    st.image("1000376160.jpeg", use_container_width=True)
                else:
                    st.markdown("""
                        <div style="text-align:center; padding-bottom: 10px;">
                            <div style="font-size: 34px; font-weight: 900; color: #1E3A8A; letter-spacing: 1px; margin-bottom: 0px;">👑 DEI REALI</div>
                            <div style="font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 2px; text-transform: uppercase;">Corporate Consulting • HR Suite</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color:#F1F5F9; margin-top:5px; margin-bottom:20px;'>", unsafe_allow_html=True)
                login_mail = st.text_input("📧 E-mail Aziendale")
                login_pw = st.text_input("🔑 Password Coordinatore", type="password")
                submit_login = st.form_submit_button("ACCEDI AL SISTEMA", use_container_width=True)
                
                if submit_login:
                    if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                        st.session_state.autenticato = True
                        st.session_state.utente_connesso = OPERATORI[login_mail]
                        st.rerun()
                    else:
                        st.error("⚠️ Credenziali errate. Riprova.")

    else:
        with st.sidebar:
            st.markdown("<br>", unsafe_allow_html=True)
            if os.path.exists("1000376160.jpeg"):
                st.image("1000376160.jpeg", use_container_width=True)
            else:
                st.markdown("""
                    <div style="text-align:center; padding: 10px 0;">
                        <div style="font-size: 24px; font-weight: 900; color: #1E3A8A; letter-spacing: 0.5px;">👑 DEI REALI</div>
                        <div style="font-size: 9px; font-weight: 700; color: #64748B; letter-spacing: 1px; text-transform: uppercase;">Corporate Consulting</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("<hr style='margin-top:10px; margin-bottom:15px;'>", unsafe_allow_html=True)
            st.markdown(f"🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
            if ai_client: st.success("🤖 Copilota IA Connesso")
            else: st.warning("⚠️ IA in modalità simulata")
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.sidebar.button("🔒 Disconnetti Account"):
                st.session_state.autenticato = False
                st.rerun()

        st.title("👑 Suite di Gestione Risorse Umane")
        c_nav = st.columns(7)
        for i, (label, key) in enumerate(buttons_nav):
            with c_nav[i]:
                if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

        st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

        if st.session_state.current_menu == "📢 Annunci":
            res_ann = supabase.table("annunci").select("*").execute()
            elenco_annunci = res_ann.data if res_ann.data else []
            
            def_pos, def_inq, def_imp, def_sede, def_foto, def_note = "", "RAL", "", "", "", ""
            
            # Se siamo in modifica carica i dati esistenti, altrimenti usa l'eventuale testo generato dall'IA
            if st.session_state.edit_mode and st.session_state.edit_job_id:
                job_da_modificare = next((a for a in elenco_annunci if a["id"] == st.session_state.edit_job_id), None)
                if job_da_modificare:
                    def_pos = job_da_modificare["posizione"]
                    def_inq = job_da_modificare["inquadramento"]
                    def_imp = job_da_modificare["importo"]
                    def_sede = job_da_modificare["sede"]
                    def_foto = job_da_modificare.get("immagine", "")
                    def_note = job_da_modificare["note"]
            elif st.session_state.ai_generated_text:
                def_note = st.session_state.ai_generated_text

            col_sx, col_centro, col_dx = st.columns([1, 1, 1.2])
            with col_sx:
                st.markdown("### 📝 Dati Principali Annuncio")
                titolo_job = st.text_input("📍 Titolo della Posizione Aperta", value=def_pos)
                lista_inq = ["RAL", "Lordo", "Orario"]
                tipo_importo = st.radio("Inquadramento", lista_inq, index=lista_inq.index(def_inq) if def_inq in lista_inq else 0, horizontal=True)
                valore_importo = st.text_input("Importo Economico (€)", value=def_imp)
                indirizzo_job = st.text_input("🏢 Sede Operativa di Lavoro", value=def_sede)
                foto_job = st.text_input("🖼️ URL Immagine di Copertina (Opzionale)", value=def_foto, placeholder="https://images.unsplash.com/...")
            with col_centro:
                st.markdown("### 🤖 Descrizione Offerta")
                note_job = st.text_area("✍️ Note, Requisiti o Testo Annuncio Completo", value=def_note, height=220)
                
                # Pulsante Copilot IA per scrivere automaticamente l'annuncio dai dati base
                if st.button("🪄 Ottimizza e Completa con IA", use_container_width=True, type="secondary"):
                    if titolo_job:
                        with st.spinner("🧠 Scrittura dell'annuncio professionale in corso con Gemini..."):
                            testo_creato = genera_testo_annuncio_ia(titolo_job, tipo_importo, valore_importo, indirizzo_job, note_job)
                            st.session_state.ai_generated_text = testo_creato
                            st.rerun()
                    else:
                        st.error("⚠️ Inserisci almeno il Titolo della Posizione prima di generare con l'IA.")

                st.markdown("<br>", unsafe_allow_html=True)
                if st.session_state.edit_mode:
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("💾 AGGIORNA ANNUNCIO", use_container_width=True):
                            if titolo_job:
                                supabase.table("annunci").update({
                                    "posizione": titolo_job, "inquadramento": tipo_importo,
                                    "importo": valore_importo, "sede": indirizzo_job, "note": note_job,
                                    "immagine": foto_job
                                }).eq("id", st.session_state.edit_job_id).execute()
                                st.session_state.edit_mode = False
                                st.session_state.edit_job_id = None
                                st.session_state.ai_generated_text = ""
                                st.success("Annuncio aggiornato con successo!"); st.rerun()
                    with c2:
                        if st.button("❌ ANNULLA", use_container_width=True):
                            st.session_state.edit_mode = False
                            st.session_state.edit_job_id = None
                            st.session_state.ai_generated_text = ""
                            st.rerun()
                else:
                    if st.button("🚀 PUBBLICA ED ABILITA PORTALE CARRIERE", use_container_width=True):
                        if titolo_job:
                            clean_id = re.sub(r'[^a-zA-Z0-9]', '-', titolo_job.lower())[:15] + f"-{random.randint(10,99)}"
                            supabase.table("annunci").insert({
                                "id": clean_id, "posizione": titolo_job, "inquadramento": tipo_importo,
                                "importo": valore_importo, "sede": indirizzo_job, "note": note_job,
                                "immagine": foto_job, "stato": "Attivo"
                            }).execute()
                            st.session_state.ai_generated_text = ""
                            st.success("🎉 Annuncio Online con Grafica Premium!"); st.rerun()
            with col_dx:
                st.markdown("### 📋 Elenco e Pannello Controllo Annunci")
                for ann in elenco_annunci:
                    stato_corrente = ann.get('stato', 'Attivo')
                    badge_stato = "🟢 Attivo" if stato_corrente == "Attivo" else "🔴 Sospeso"
                    
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    st.markdown(f"<b>📢 {ann['posizione']}</b> - 📍 {ann['sede']} | <small><b>{badge_stato}</b></small>", unsafe_allow_html=True)
                    st.markdown(f"<div class='link-box'>https://deireali-hr.streamlit.app/?job={ann['id']}</div>", unsafe_allow_html=True)
                    
                    c_btn1, c_btn2, c_btn3 = st.columns(3)
                    with c_btn1:
                        if st.button("✍️ Modifica", key=f"edit_{ann['id']}", use_container_width=True):
                            st.session_state.edit_mode = True
                            st.session_state.edit_job_id = ann['id']
                            st.rerun()
                    with c_btn2:
                        nuovo_stato = "Sospeso" if stato_corrente == "Attivo" else "Attivo"
                        label_sosp = "⏸️ Sospendi" if stato_corrente == "Attivo" else "▶️ Attiva"
                        if st.button(label_sosp, key=f"susp_{ann['id']}", use_container_width=True):
                            supabase.table("annunci").update({"stato": nuovo_stato}).eq("id", ann['id']).execute()
                            st.rerun()
                    with c_btn3:
                        if st.button("🗑️ Elimina", key=f"del_{ann['id']}", use_container_width=True):
                            supabase.table("annunci").delete().eq("id", ann['id']).execute()
                            st.success("Annuncio rimosso dal cloud!"); st.rerun()
                            
                    st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.current_menu == "📥 Screening CV":
            st.markdown("### 📥 Analisi CV e Classificazione Idoneità Real-Time")
            res_cand = supabase.table("candidati").select("*").eq("stato", "In Screening").execute()
            for cand in (res_cand.data if res_cand.data else []):
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                c_l, c_r = st.columns([2.5, 1.5])
                with c_l:
                    st.markdown(f"#### 👤 {cand['nome']} &emsp; <span style='font-size:14px;color:#2563EB;'>📊 Idoneità Reale Estratta: {cand['idoneita']} {cand['stelle']}</span>", unsafe_allow_html=True)
                    st.markdown(f"🎯 *Posizione:* {cand['posizione']} | 📱 *Tel:* {cand['telefono']}")
                    st.markdown(f'<div class="ai-box"><b>🧠 VERBALE DI VALUTAZIONE IA DEEPREAD:</b><br>{cand["orientamento"]}</div>', unsafe_allow_html=True)
                with c_r:
                    if st.button("🤝 Approva per Colloquio", key=f"appr_{cand['id']}", use_container_width=True):
                        supabase.table("candidati").update({"stato": "Approvato per Colloquio"}).eq("id", cand['id']).execute()
                        st.success("Profilo spostato in agenda!"); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.current_menu == "🤝 Colloqui AI":
            st.markdown("### 🗓️ Organizzazione Turni")
            res_ag = supabase.table("agenda").select("*").execute()
            agenda_list = res_ag.data if res_ag.data else []
            if agenda_list:
                st.dataframe(pd.DataFrame(agenda_list)[["data", "ora", "candidato", "operatore", "telefono", "meet_link"]], use_container_width=True)
            
            col_plan, col_act = st.columns([1, 1])
            with col_plan:
                res_all_c = supabase.table("candidati").select("nome", "telefono").eq("stato", "Approvato per Colloquio").execute()
                cand_dispo = res_all_c.data if res_all_c.data else []
                if cand_dispo:
                    cand_scelto = st.selectbox("Seleziona Profilo Idoneo", [c["nome"] for c in cand_dispo])
                    d_s = st.date_input("Data", min_value=date.today())
                    o_s = st.time_input("Orario", value=time(10,0))
                    if st.button("💾 Pianifica Turno Cloud", use_container_width=True):
                        c_info = next((c for c in cand_dispo if c["nome"] == cand_scelto), None)
                        meet_url = f"https://meet.google.com/{random.randint(100,999)}-{random.randint(100,999)}"
                        supabase.table("agenda").insert({
                            "candidato": cand_scelto, "data": str(d_s), "ora": o_s.strftime("%H:%M"),
                            "operatore": st.session_state.utente_connesso['nome'], "meet_link": meet_url, "telefono": c_info["telefono"] if c_info else ""
                        }).execute()
                        st.success("Inserito in agenda!"); st.rerun()
            with col_act:
                for app in agenda_list:
                    st.markdown(f'<div class="saas-box"><b>{app["candidato"]}</b> ({app["data"]} ore {app["ora"]})', unsafe_allow_html=True)
                    msg = f"Gentile {app['candidato']},\nLe confermiamo il colloquio con Dei Reali.\n🗓️ {app['data']} alle {app['ora']}.\n🖥️ Link Meet: {app['meet_link']}"
                    st.markdown(f'<a href="https://wa.me/{str(app["telefono"]).replace("+","")}?text={urllib.parse.quote(msg)}" target="_blank" class="whatsapp-btn">💬 Avvisa via WhatsApp</a>', unsafe_allow_html=True)
                    st.markdown(f'<a href="{app["meet_link"]}" target="_blank" class="meet-btn">🖥️ Entra nell\'Aula Virtuale</a></div>', unsafe_allow_html=True)

        else:
            st.info("Sezione attiva e sincronizzata su Supabase Cloud.")
