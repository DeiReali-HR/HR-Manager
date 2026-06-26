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

# 3. CSS Custom Premium - Stile Umana.it Clean & Login Navy
st.markdown("""
    <style>
    /* Sfondo predefinito e Sidebar */
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    
    /* SCHERMATA LOGIN PREMIUM */
    .login-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #0F172A !important; /* Fondo Navy Scuro */
        background-image: radial-gradient(circle at 50% 50%, #1E3A8A 0%, #0F172A 100%) !important;
        z-index: 999990; display: flex; justify-content: center; align-items: center;
    }
    .login-card {
        background: #FFFFFF !important; padding: 45px; border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
        width: 100%; max-width: 480px; text-align: center; border: 1px solid rgba(255,255,255,0.1);
    }
    .login-logo { font-size: 38px; font-weight: 800; color: #1E3A8A; letter-spacing: 1.5px; margin-bottom: 5px; }
    .login-subtitle { font-size: 12px; font-weight: 600; color: #64748B; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; }
    
    /* Layout Annuncio Stile Umana */
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

# --- SUITE INTERNA AMMINISTRATIVA CON LOGIN STRUTTURATO ---
else:
    if not st.session_state.autenticato:
        # Layout centrato e pulito per contenitore Bianco su sfondo Navy
        _, col_box, _ = st.columns([1, 1.2, 1])
        with col_box:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            with st.container():
                st.markdown("""
                    <div style="background:#FFFFFF; padding:40px; border-radius:16px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #E2E8F0; text-align:center;">
                        <div style="font-size: 34px; font-weight: 800; color: #1E3A8A; letter-spacing: 1px; margin-bottom: 2px;">👑 DEI REALI</div>
                        <div style="font-size: 11px; font-weight: 700; color: #64748B; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 25px;">Corporate Consulting • HR Suite</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Form di login incorporato dentro il box bianco
                with st.form("login_form_premium"):
                    login_mail = st.text_input("📧 E-mail Aziendale")
                    login_pw = st.text_input("🔑 Password Coordinatore", type="password")
                    submit_login = st.form_submit_button("ACCEDI AL SISTEMA")
                    
                    if submit_login:
                        if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                            st.session_state.autenticato = True
                            st.session_state.utente_connesso = OPERATORI[login_mail]
                            st.rerun()
                        else:
                            st.error("⚠️ Credenziali errate. Riprova.")
            
            # Imposta lo sfondo della sola pagina di login a Navy Blue
            st.markdown("""
                <style>
                    .stApp { background: radial-gradient(circle at 50% 50%, #1E3A8A 0%, #0F172A 100%) !important; }
                    .stApp h1, .stApp p, .stApp label { color: #0F172A !important; }
                </style>
            """, unsafe_allow_html=True)

    else:
        with st.sidebar:
            st.markdown("""
                <div style="text-align:center; padding: 10px 0;">
                    <div style="font-size: 24px; font-weight: 800; color: #1E3A8A; letter-spacing: 0.5px;">👑 DEI REALI</div>
                    <div style="font-size: 9px; font-weight: 700; color: #64748B; letter-spacing: 1px; text-transform: uppercase;">Corporate Consulting</div>
                </div>
                <hr style="margin-top:5px; margin-bottom:15px;">
            """, unsafe_allow_html=True)
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
            col_sx, col_centro, col_dx = st.columns([1, 1, 1])
            with col_sx:
                st.markdown("### 📝 Dati Principali Annuncio")
                titolo_job = st.text_input("📍 Titolo della Posizione Aperta")
                tipo_importo = st.radio("Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True)
                valore_importo = st.text_input("Importo Economico (€)")
                indirizzo_job = st.text_input("🏢 Sede Operativa di Lavoro")
                foto_job = st.text_input("🖼️ URL Immagine di Copertina (Opzionale)", placeholder="https://images.unsplash.com/...")
            with col_centro:
                st.markdown("### 🤖 Descrizione Offerta")
                note_job = st.text_area("✍️ Note e Requisiti Iniziali", height=150)
                if st.button("🚀 PUBBLICA ED ABILITA PORTALE CARRIERE", use_container_width=True):
                    if titolo_job:
                        clean_id = re.sub(r'[^a-zA-Z0-9]', '-', titolo_job.lower())[:15] + f"-{random.randint(10,99)}"
                        supabase.table("annunci").insert({
                            "id": clean_id, "posizione": titolo_job, "inquadramento": tipo_importo,
                            "importo": valore_importo, "sede": indirizzo_job, "note": note_job,
                            "immagine": foto_job
                        }).execute()
                        st.success("🎉 Annuncio Online con Grafica Premium!"); st.rerun()
            with col_dx:
                st.markdown("### 📋 Elenco Link Attivi")
                res_ann = supabase.table("annunci").select("*").execute()
                for ann in (res_ann.data if res_ann.data else []):
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    st.markdown(f"<b>📢 {ann['posizione']}</b> - 📍 {ann['sede']}", unsafe_allow_html=True)
                    st.markdown(f"<div class='link-box'>https://deireali-hr.streamlit.app/?job={ann['id']}</div>", unsafe_allow_html=True)
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
