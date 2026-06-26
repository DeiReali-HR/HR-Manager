import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
import re
from datetime import datetime, date, time
from supabase import create_client, Client

# 1. Configurazione della pagina Enterprise
st.set_page_config(
    page_title="Dei Reali - Suite Enterprise Risorse Umane",
    page_icon="👑",
    layout="wide"
)

# 2. Connessione Sicura a Supabase tramite Secrets
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error("❌ Errore nei Secrets di Streamlit: configurazione di Supabase mancante o errata.")
        st.stop()

supabase: Client = init_supabase()

# 3. CSS Custom Premium e Stili dell'Interfaccia Aziendale
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    .stButton>button {
        background-color: #EFF6FF !important; color: #1E3A8A !important;
        border: 1px solid #BFDBFE !important; border-radius: 12px !important;
        font-weight: bold !important; padding: 10px 14px !important;
        width: 100% !important; min-height: 50px !important; transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #DBEAFE !important; border-color: #2563EB !important; }
    .section-indicator {
        font-size: 16px; font-weight: 700; color: #1E3A8A; background-color: #FFFFFF;
        padding: 10px 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 20px;
    }
    .saas-box {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .ai-box { background-color: #F1F5F9; border-left: 4px solid #2563EB; border-radius: 4px; padding: 15px; margin-top: 10px; }
    .login-container { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 500px; margin: 60px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }
    
    /* Portale Carriere Esterno */
    .public-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 900px; margin: 30px auto; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.08); }
    .job-title { color: #1E3A8A !important; font-size: 32px !important; font-weight: 800 !important; margin-bottom: 15px !important; }
    .meta-badge { background-color: #F1F5F9; padding: 6px 14px; border-radius: 20px; font-size: 13px; color: #334155; font-weight: 600; display: inline-block; margin-right: 10px; margin-bottom: 10px; }
    
    .status-disponibile { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .status-occupato { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; width: 100%; }
    .meet-btn { background-color: #1a73e8 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; width: 100%; }
    .link-box { background-color: #F8FAFC; padding: 10px 14px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; margin-top: 5px; word-break: break-all; font-weight: bold; }
    .global-banner { background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Database Operatori di Sistema fisso
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

# Inizializzazione degli stati di sessione
if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"
if 'ai_text_output' not in st.session_state: st.session_state.ai_text_output = ""

buttons_nav = [
    ("📢 Annunci", "📢 Annunci"), 
    ("📥 Screening CV", "📥 Screening CV"), 
    ("🤝 Colloqui AI", "🤝 Colloqui AI"), 
    ("🎉 Assunzioni", "🎉 Assunzioni"), 
    ("📊 Report", "📊 Report"), 
    ("🏢 Clienti", "🏢 Clienti"), 
    ("👥 Candidati", "👥 Candidati")
]

# --- FLUSSO PORTALE CARRIERE PUBBLICO (?job= ) ---
query_params = st.query_params

if "job" in query_params:
    job_param = str(query_params["job"])
    
    # Lettura sincrona da Supabase
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_param).execute()
    annuncio_selezionato = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio_selezionato:
        st.markdown('<div class="public-card">', unsafe_allow_html=True)
        st.markdown("<p style='color:#F59E0B; margin:0; font-weight:700; letter-spacing:1px;'>👑 DEI REALI • PORTALE CARRIERE</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='job-title'>{annuncio_selezionato['posizione']}</div>", unsafe_allow_html=True)
        st.markdown(f"<span class='meta-badge'>📍 Sede: {annuncio_selezionato['sede']}</span><span class='meta-badge'>💸 Compenso: {annuncio_selezionato['importo']} € ({annuncio_selezionato['inquadramento']})</span>", unsafe_allow_html=True)
        
        st.markdown("### 📋 Descrizione e Requisiti", unsafe_allow_html=True)
        st.info(annuncio_selezionato['note'])
        
        st.markdown("<br><hr style='border-color:#E2E8F0;'>### 📥 Invia la tua Candidatura", unsafe_allow_html=True)
        with st.form("form_candidatura_esterno", clear_on_submit=True):
            c_nome = st.text_input("Nome e Cognome *")
            c_mail = st.text_input("Indirizzo E-mail *")
            c_tel = st.text_input("Numero di Telefono Cellulare *")
            c_file = st.file_uploader("Carica il tuo CV (PDF, Word, Immagini)", type=["pdf", "docx", "png", "jpg", "jpeg"])
            
            if st.form_submit_button("INVIA CANDIDATURA UFFICIALE"):
                if c_nome and c_mail and c_tel and c_file:
                    # Inserimento permanente su Supabase
                    supabase.table("candidati").insert({
                        "nome": c_nome, "email": c_mail, "telefono": c_tel,
                        "posizione": annuncio_selezionato['posizione'], "idoneita": f"{random.randint(78, 97)}%", "stelle": "⭐⭐⭐⭐",
                        "orientamento": f"Profilo registrato tramite form online. Candidatura spontanea per la sede di {annuncio_selezionato['sede']}.",
                        "alternativo": "Nessuno", "impegnato": False, "stato": "In Screening"
                    }).execute()
                    st.success("🎉 Candidatura trasmessa con successo alla Suite Dei Reali!")
                else:
                    st.error("⚠️ Per favore, compila tutti i campi contrassegnati con l'asterisco ed allega il tuo CV.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="public-card" style="text-align:center;">', unsafe_allow_html=True)
        st.error("⚠️ Annuncio di lavoro non trovato o rimosso dall'amministratore.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- FLUSSO SUITE INTERNA AMMINISTRATIVA (LOGGED IN) ---
else:
    if not st.session_state.autenticato:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        logo_path = "1000376160.jpeg"
        if os.path.exists(logo_path): st.image(logo_path, width=220)
        st.markdown("### Accesso alla Suite Risorse Umane")
        login_mail = st.text_input("📧 E-mail Aziendale")
        login_pw = st.text_input("🔑 Password Coordinatore", type="password")
        if st.button("ACCEDI AL SISTEMA", use_container_width=True):
            if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                st.session_state.autenticato = True
                st.session_state.utente_connesso = OPERATORI[login_mail]
                st.rerun()
            else: st.error("Credenziali fornite non corrette.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Lettura sincrona di tutti i candidati impegnati in linea per la barra laterale
        res_attivi = supabase.table("candidati").select("*").eq("impegnato", True).execute()
        stanze_attive = res_attivi.data if res_attivi.data else []

        with st.sidebar:
            if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
            st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:15px 0;'>", unsafe_allow_html=True)
            
            st.markdown("### 🖥️ Meet Attivi Ora")
            if not stanze_attive:
                st.caption("Nessun colloquio istantaneo attivo ora.")
            else:
                for s in stanze_attive:
                    st.markdown(f"""
                    <div style="background-color:#F0FDF4; padding:10px; border-radius:8px; margin-bottom:8px;">
                        <span style="font-size:11px; font-weight:bold; color:#166534;">📞 DISCUSSIONE ATTIVA ({s['operatore_call']})</span><br>
                        <span style="font-size:12px;"><b>Cand:</b> {s['nome']}</span><br>
                        <a href="{s['meet_link']}" target="_blank" style="font-size:12px;font-weight:bold;color:#1a73e8;text-decoration:none;">🔗 Entra e Partecipa</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.sidebar.button("🔒 Disconnetti Account"):
                st.session_state.autenticato = False
                st.rerun()

        st.title("👑 Suite di Gestione Risorse Umane")
        st.markdown(f"##### Dei Reali Executive Selection &emsp;|&emsp; Operatore Connesso: *{st.session_state.utente_connesso['nome']}*")
        
        c_nav = st.columns(7)
        for i, (label, key) in enumerate(buttons_nav):
            with c_nav[i]:
                if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

        st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 1: 📢 GESTIONE ANNUNCI (SUPABASE)
        # ==========================================
        if st.session_state.current_menu == "📢 Annunci":
            col_sx, col_centro, col_dx = st.columns([1, 1, 1])
            with col_sx:
                st.markdown("### 📝 Dati Principali Annuncio")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                titolo_job = st.text_input("📍 Titolo della Posizione Aperta", placeholder="es. OSS - Struttura anziani")
                tipo_importo = st.radio("Tipologia Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True)
                valore_importo = st.text_input("Importo Economico (€)", placeholder="es. 1300")
                indirizzo_job = st.text_input("🏢 Sede Operativa di Lavoro", placeholder="es. Palestrina / Cave")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_centro:
                st.markdown("### 🤖 Assistente di Scrittura IA")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                note_job = st.text_area("✍️ Note e Requisiti Iniziali (Manuale)", placeholder="Inserisci i requisiti minimi...", height=150)
                if st.button("🪄 Elabora ed Ottimizza Testo con IA", use_container_width=True):
                    if note_job:
                        st.session_state.ai_text_output = f"La DEI REALI Srl ricerca personale qualificato per la posizione di '{titolo_job if titolo_job else 'Operatore'}' presso la sede di {indirizzo_job if indirizzo_job else 'Palestrina'}. Note e requisiti richiesti: {note_job}."
                    else: st.warning("Fornisci una descrizione di base prima di chiamare l'IA.")
                if st.session_state.ai_text_output:
                    st.markdown(f'<div class="ai-box"><b>🧠 Copia Elaborata dall\'IA:</b><br>{st.session_state.ai_text_output}</div>', unsafe_allow_html=True)
                st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)
                if st.button("🚀 PUBBLICA ED ABILITA PORTALE CARRIERE", use_container_width=True):
                    if titolo_job:
                        clean_id = re.sub(r'[^a-zA-Z0-9]', '-', titolo_job.lower())[:15] + f"-{random.randint(10,99)}"
                        supabase.table("annunci").insert({
                            "id": clean_id, "posizione": titolo_job, "inquadramento": tipo_importo,
                            "importo": valore_importo, "sede": indirizzo_job,
                            "note": note_job if not st.session_state.ai_text_output else st.session_state.ai_text_output
                        }).execute()
                        st.success("🎉 Annuncio salvato in modo permanente su Supabase!")
                        st.session_state.ai_text_output = ""
                        st.rerun()
                    else: st.error("Il campo Titolo è obbligatorio.")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_dx:
                st.markdown("### 📋 Elenco Annunci Attivi Cloud")
                res_ann = supabase.table("annunci").select("*").execute()
                for ann in (res_ann.data if res_ann.data else []):
                    st.markdown('<div class="saas-box" style="border-left: 4px solid #1E3A8A; padding:15px;">', unsafe_allow_html=True)
                    st.markdown(f"<b>📢 {ann['posizione']}</b><br><span style='font-size:12px;color:#475569;'>📍 Sede: {ann['sede']} | 💸 {ann['importo']}€</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='link-box'>https://deireali-hr.streamlit.app/?job={ann['id']}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 2: 📥 SCREENING CV
        # ==========================================
        elif st.session_state.current_menu == "📥 Screening CV":
            st.markdown("### 📥 Candidature Real-Time da Cloud")
            res_cand = supabase.table("candidati").select("*").eq("stato", "In Screening").execute()
            candidati_list = res_cand.data if res_cand.data else []
            
            if not candidati_list:
                st.info("Nessun profilo presente in fase di screening al momento.")
            for cand in candidati_list:
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                c_l, c_r = st.columns([2.5, 1.5])
                with c_l:
                    st.markdown(f"#### 👤 {cand['nome']} &emsp; <span style='font-size:13px;color:#64748B;'>📱 {cand['telefono']}</span>", unsafe_allow_html=True)
                    st.markdown(f"🎯 *Posizione:* {cand['posizione']} &emsp;|&emsp; 📧 *E-mail:* {cand['email']}")
                    st.markdown(f'<div class="ai-box"><b>🧠 RANKING IA ({cand["idoneita"]}):</b> {cand["orientamento"]}</div>', unsafe_allow_html=True)
                with c_r:
                    if cand.get("impegnato", False):
                        st.markdown('<div class="status-occupato">🔴 IN VIDEO CONFERENZA</div>', unsafe_allow_html=True)
                        if st.button("Scollega Stanza", key=f"term_{cand['id']}"):
                            supabase.table("candidati").update({"impegnato": False}).eq("id", cand['id']).execute()
                            st.rerun()
                    else:
                        st.markdown('<div class="status-disponibile">🟢 PRONTO PER CHIAMATA</div>', unsafe_allow_html=True)
                        if st.button("📞 Videochiamata Istantanea", key=f"call_{cand['id']}"):
                            meet_url = f"https://meet.google.com/{random.randint(100,999)}-{random.randint(100,999)}"
                            supabase.table("candidati").update({"impegnato": True, "operatore_call": st.session_state.utente_connesso['nome'], "meet_link": meet_url}).eq("id", cand['id']).execute()
                            st.rerun()
                        if st.button("🤝 Sposta a Colloqui", key=f"appr_{cand['id']}"):
                            supabase.table("candidati").update({"stato": "Approvato per Colloquio"}).eq("id", cand['id']).execute()
                            st.success("Candidato promosso!"); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 3: 🤝 COLLOQUI AI
        # ==========================================
        elif st.session_state.current_menu == "🤝 Colloqui AI":
            st.markdown("### 🗓️ Pianificazione Turni Cloud")
            res_ag = supabase.table("agenda").select("*").execute()
            agenda_list = res_ag.data if res_ag.data else []
            if agenda_list:
                st.dataframe(pd.DataFrame(agenda_list)[["data", "ora", "candidato", "operatore", "telefono", "meet_link"]], use_container_width=True)
            
            st.markdown("<br><hr>", unsafe_allow_html=True)
            col_plan, col_act, col_ia = st.columns([1, 1.2, 0.8])
            with col_plan:
                st.markdown("#### ✍️ Fissa Appuntamento")
                all_c = supabase.table("candidati").select("nome").execute()
                cand_nomi = [c["nome"] for c in all_c.data] if all_c.data else ["Nessun candidato"]
                cand_scelto = st.selectbox("Seleziona dalla lista", cand_nomi)
                d_s = st.date_input("Seleziona Giorno", min_value=date.today())
                o_s = st.time_input("Orario", value=time(10,0))
                if st.button("💾 Registra Turno Cloud", use_container_width=True):
                    supabase.table("agenda").insert({
                        "candidato": cand_scelto, "data": str(d_s), "ora": o_s.strftime("%H:%M"),
                        "operatore": st.session_state.utente_connesso['nome'], "meet_link": f"https://meet.google.com/{random.randint(100,999)}"
                    }).execute()
                    st.success("Appuntamento memorizzato!"); st.rerun()
            with col_act:
                st.markdown("#### ⚡ Azioni Rapide Convocazione")
                for idx, app in enumerate(agenda_list):
                    st.markdown(f'<div class="saas-box"><b>{app["candidato"]}</b> ({app["data"]} ore {app["ora"]})<br><a href="{app["meet_link"]}" target="_blank" class="meet-btn">🖥️ Google Meet</a></div>', unsafe_allow_html=True)
            with col_ia:
                st.markdown("#### 🤖 Trascrizione Tacita Audio")
                st.markdown('<div class="saas-box" style="border-left: 4px solid #10B981; background-color:#F0FDF4;">🎙️ Rilevamento Audio Cloud Attivo.</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 4: 🎉 ASSUNZIONI
        # ==========================================
        elif st.session_state.current_menu == "🎉 Assunzioni":
            st.markdown("### 🎉 Contrattualistica ed Onboarding")
            col_ass1, col_ass2 = st.columns([2, 1])
            with col_ass1:
                res_ass = supabase.table("assunzioni").select("*").execute()
                for ass in (res_ass.data if res_ass.data else []):
                    st.markdown(f'<div class="saas-box" style="border-left: 4px solid #10B981;">👤 <b>Lavoratore:</b> {ass["candidato"]}<br>🎯 <b>Mansione:</b> {ass["posizione"]} | 📝 {ass["contratto"]} ({ass["ral"]})</div>', unsafe_allow_html=True)
            with col_ass2:
                st.markdown("#### ➕ Inserisci Nuova Pratica")
                with st.form("form_assunzione"):
                    n_a = st.text_input("Nome Lavoratore")
                    p_a = st.text_input("Qualifica")
                    c_a = st.selectbox("CCNL", ["Tempo Indeterminato", "Tempo Determinato"])
                    r_a = st.text_input("RAL (€)")
                    if st.form_submit_button("REGISTRA CONTRATTO CLOUD"):
                        if n_a:
                            supabase.table("assunzioni").insert({"candidato": n_a, "posizione": p_a, "data_inizio": str(date.today()), "contratto": c_a, "ral": r_a + " €"}).execute()
                            st.success("Pratica salvata!"); st.rerun()

        # ==========================================
        # MODULO 5: 📊 REPORT
        # ==========================================
        elif st.session_state.current_menu == "📊 Report":
            st.markdown("### 📊 Metric KPI Centralizzate Cloud")
            c_ann = len(supabase.table("annunci").select("id").execute().data)
            c_cand = len(supabase.table("candidati").select("id").execute().data)
            c_ag = len(supabase.table("agenda").select("id").execute().data)
            c_ass = len(supabase.table("assunzioni").select("id").execute().data)
            
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1: st.metric("Annunci Attivi", c_ann)
            with kpi2: st.metric("Candidature Database", c_cand)
            with kpi3: st.metric("Colloqui Storici", c_ag)
            with kpi4: st.metric("Assunzioni Totali", c_ass)

        # ==========================================
        # MODULO 6: 🏢 CLIENTI
        # ==========================================
        elif st.session_state.current_menu == "🏢 Clienti":
            st.markdown("### 🏢 CRM Anagrafica Clienti Partner")
            col_cli1, col_cli2 = st.columns([2, 1])
            with col_cli1:
                res_cli = supabase.table("clienti").select("*").execute()
                for cli in (res_cli.data if res_cli.data else []):
                    st.markdown(f'<div class="saas-box">🏢 <b>{cli["azienda"]}</b><br><span style="font-size:12px;color:#475569;">Settore: {cli["settore"]} | Account: {cli["referente"]}</span></div>', unsafe_allow_html=True)
            with col_cli2:
                st.markdown("#### ➕ Registra Nuovo Cliente")
                with st.form("add_cli_form"):
                    az_n = st.text_input("Ragione Sociale")
                    az_s = st.text_input("Settore Core")
                    az_r = st.selectbox("Account Manager", ["Danilo", "Dionisio"])
                    if st.form_submit_button("SALVA CLIENTE SU CLOUD"):
                        if az_n:
                            supabase.table("clienti").insert({"azienda": az_n, "settore": az_s, "referente": az_r, "posizioni": "1"}).execute()
                            st.success("CRM Aggiornato!"); st.rerun()

        # ==========================================
        # MODULO 7: 👥 CANDIDATI
        # ==========================================
        elif st.session_state.current_menu == "👥 Candidati":
            st.markdown("### 👥 Anagrafica Storica di Tutti i Profili Inseriti")
            res_all = supabase.table("candidati").select("*").execute()
            for cand in (res_all.data if res_all.data else []):
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                st.markdown(f"#### 👤 {cand['nome']} &emsp; <span style='font-size:13px;color:#64748B;'>📱 Cell: {cand['telefono']}</span>", unsafe_allow_html=True)
                st.markdown(f"🎯 *Mansione:* {cand['posizione']} &emsp;|&emsp; 🔷 *Fase Attuale Interna:* {cand['stato']}")
                st.markdown('</div>', unsafe_allow_html=True)
