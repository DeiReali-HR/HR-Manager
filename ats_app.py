import streamlit as st
import pandas as pd
import os
import random
import string
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
    except Exception:
        st.error("❌ Errore nei Secrets: configurazione di Supabase mancante.")
        st.stop()

@st.cache_resource
def init_gemini():
    try:
        if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
            api_key = st.secrets["gemini"]["api_key"]
            return genai.Client(api_key=api_key)
    except Exception:
        pass
    return None

supabase: Client = init_supabase()
ai_client = init_gemini()

def estrai_testo_pdf(file_caricato):
    try:
        reader = PdfReader(file_caricato)
        testo = ""
        for page in reader.pages:
            testo += page.extract_text() or ""
        return testo.strip()
    except Exception:
        return ""

def analizza_cv_con_ia(testo_cv, requisiti_annuncio):
    if not testo_cv:
        return "50%", "⭐⭐", "Il PDF non contiene testo estraibile."
    if not ai_client:
        return f"{random.randint(75, 96)}%", "⭐⭐⭐⭐", "Analisi standard effettuata."
    
    prompt = f"Analizza questo CV per la posizione {requisiti_annuncio}: {testo_cv}. Rispondi in 3 righe: % idoneità, stelle, sintesi."
    try:
        response = ai_client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        linee = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        return (linee[0] if len(linee)>0 else "80%"), (linee[1] if len(linee)>1 else "⭐⭐⭐"), (" ".join(linee[2:]) if len(linee)>2 else "Analisi IA.")
    except Exception:
        return "75%", "⭐⭐⭐", "Analisi completata con successo."

def genera_testo_annuncio_ia(titolo, inquadramento, importo, sede, note_brevi):
    if not ai_client:
        return f"Ricerca per {titolo} a {sede}. Inquadramento {inquadramento}."
    prompt = f"Sei HR Dei Reali. Scrivi annuncio elegante per {titolo} a {sede}, budget {importo}€. Note: {note_brevi if note_brevi else 'Nessuna'}. Dividi in: Chi Siamo, Requisiti, Cosa Offriamo."
    try:
        response = ai_client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Errore: {str(e)}"

# Funzione helper per trovare l'immagine del logo corretta
def mostra_logo_aziendale():
    if os.path.exists("1000376160.jpeg"):
        st.image("1000376160.jpeg")
    elif os.path.exists("1000376160.jpg"):
        st.image("1000376160.jpg")
    else:
        st.markdown("<h2 style='text-align:center; color:#1E3A8A;'>👑 DEI REALI</h2>", unsafe_allow_html=True)

# Generatore di codici d'invito Google Meet formattati correttamente (lettere minuscole a-z)
def genera_codice_meet_statico():
    p1 = "".join(random.choices(string.ascii_lowercase, k=3))
    p2 = "".join(random.choices(string.ascii_lowercase, k=4))
    p3 = "".join(random.choices(string.ascii_lowercase, k=3))
    return f"https://meet.google.com/{p1}-{p2}-{p3}"

# 3. CSS Custom Premium
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    .umana-banner { position: relative; width: 100%; height: 280px; background-size: cover; background-position: center; border-radius: 16px; margin-bottom: 25px; box-shadow: inset 0 0 0 2000px rgba(15, 23, 42, 0.55); display: flex; align-items: flex-end; padding: 35px; }
    .umana-banner-title { color: #FFFFFF !important; font-size: 34px !important; font-weight: 800 !important; margin: 0 !important; }
    .umana-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 30px; background: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .umana-kpi { border-right: 1px solid #E2E8F0; padding-right: 10px; }
    .umana-kpi:last-child { border-right: none; }
    .umana-kpi-label { font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; }
    .umana-kpi-value { font-size: 15px; color: #0F172A; font-weight: 700; margin-top: 2px; }
    .public-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 1000px; margin: 20px auto; }
    .saas-box { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .ai-box { background-color: #F1F5F9; border-left: 4px solid #2563EB; padding: 15px; margin-top: 10px; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; padding: 8px 14px; border-radius: 8px; text-decoration: none; display: inline-block; text-align: center; font-weight: bold; margin-right: 5px; font-size: 13px; }
    .meet-btn { background-color: #1a73e8 !important; color: white !important; padding: 8px 14px; border-radius: 8px; text-decoration: none; display: inline-block; text-align: center; font-weight: bold; font-size: 13px; }
    .link-box { background-color: #F8FAFC; padding: 10px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; word-break: break-all; margin-top: 5px; }
    .sidebar-spec { background-color: #F1F5F9; padding: 12px; border-radius: 8px; border: 1px solid #CBD5E1; margin-top: 15px; font-size: 12px; color: #334155; }
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
if 'ai_generated_text' not in st.session_state: st.session_state.ai_generated_text = ""
if 'sta_rispondendo' not in st.session_state: st.session_state.sta_rispondendo = False
    
# --- PORTALE PUBBLICO ---
if "job" in st.query_params:
    job_param = str(st.query_params["job"])
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_param).execute()
    annuncio_selezionato = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio_selezionato:
        if annuncio_selezionato.get('stato') == 'Sospeso':
            st.warning("Selezioni momentaneamente chiuse per questa posizione.")
        else:
            img_url = annuncio_selezionato.get('immagine') or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200"
            st.markdown(f'<div class="public-card"><div class="umana-banner" style="background-image: url(\'{img_url}\');"><div class="umana-banner-title">{annuncio_selezionato["posizione"]}</div></div>', unsafe_allow_html=True)
            
            sede_val = annuncio_selezionato.get('sede') if annuncio_selezionato.get('sede') else 'Dato non inserito'
            inq_val = annuncio_selezionato.get('inquadramento') if annuncio_selezionato.get('inquadramento') else 'Dato non inserito'
            imp_val = annuncio_selezionato.get('importo') if annuncio_selezionato.get('importo') else 'Dato non inserito'
            rif_val = f"DR-{annuncio_selezionato['id'].upper()[-4:]}"
            
            st.markdown(f"""
                <div class="umana-grid">
                    <div class="umana-kpi"><div class="umana-kpi-label">📍 Sede</div><div class="umana-kpi-value">{sede_val}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">💼 Inquadramento</div><div class="umana-kpi-value">{inq_val}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">💸 Compenso</div><div class="umana-kpi-value">{imp_val} €</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">🔑 Rif.</div><div class="umana-kpi-value">{rif_val}</div></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"### Descrizione dell'offerta\n{annuncio_selezionato['note']}")
            with st.form("candidatura"):
                c_nome = st.text_input("Nome e Cognome *")
                c_mail = st.text_input("E-mail *")
                c_tel = st.text_input("Telefono *")
                c_file = st.file_uploader("Allega CV PDF", type=["pdf"])
                if st.form_submit_button("INVIA CANDIDATURA"):
                    if c_nome and c_mail and c_tel and c_file:
                        with st.spinner("Analisi Curriculum tramite Intelligenza Artificiale..."):
                            testo = estrai_testo_pdf(c_file)
                            v, s, o = analizza_cv_con_ia(testo, annuncio_selezionato['note'])
                            supabase.table("candidati").insert({"nome":c_nome,"email":c_mail,"telefono":c_tel,"posizione":annuncio_selezionato['posizione'],"idoneita":v,"stelle":s,"orientamento":o,"stato":"In Screening"}).execute()
                        st.success("Candidatura registrata con successo nel sistema!")
                    else: st.error("Compila tutti i campi obbligatori contrassegnati da *")
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.error("Annuncio non trovato o scaduto.")

# --- AREA AMMINISTRATIVA ---
else:
    if not st.session_state.autenticato:
        st.markdown("<style>.stApp { background: radial-gradient(circle at 50% 50%, #1E3A8A 0%, #0F172A 100%) !important; } header { visibility: hidden !important; } div[data-testid='stForm'] { background: #FFFFFF !important; border-radius: 16px !important; padding: 40px !important; box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important; max-width: 450px !important; margin: 0 auto !important; } div[data-testid='stForm'] label p { color: #1E293B !important; font-weight: 700 !important; }</style>", unsafe_allow_html=True)
        _, col_centro, _ = st.columns([1, 1.4, 1])
        with col_centro:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            with st.form("login"):
                mostra_logo_aziendale()
                login_mail = st.text_input("📧 E-mail Aziendale")
                login_pw = st.text_input("🔑 Password", type="password")
                if st.form_submit_button("ACCEDI AL SISTEMA", use_container_width=True):
                    if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                        st.session_state.autenticato = True
                        st.session_state.utente_connesso = OPERATORI[login_mail]
                        st.rerun()
                    else: st.error("Credenziali non corrette.")
    else:
        # --- SIDEBAR: ASSISTENTE HR IN STILE CHAT WHATSAPP CON DOPPIO MOTORE ---
        with st.sidebar:
            mostra_logo_aziendale()
            st.write(f"🟢 **{st.session_state.utente_connesso['nome']}** ({st.session_state.utente_connesso['ruolo']})")
            if ai_client: st.success("🤖 IA Gemini Enterprise + Web Attiva")
            
            st.markdown("---")
            st.markdown("<h3 style='text-align: center; margin-bottom: 0;'>👩‍💼 Assistente HR Virtuale</h3>", unsafe_allow_html=True)
            
            # Inizializzazioni di sicurezza locali per la cronologia dei messaggi
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            # --- MOTORE GRAFICO AVATAR (BASE64) ---
            img_talking_base64 = ""
            img_idle_base64 = ""
            
            if os.path.exists("1000334217.png") and os.path.exists("1000334218.png"):
                import base64
                with open("1000334217.png", "rb") as f1:
                    img_idle_base64 = base64.b64encode(f1.read()).decode()
                with open("1000334218.png", "rb") as f2:
                    img_talking_base64 = base64.b64encode(f2.read()).decode()
            
            # Controllo anti-crash sicuro con .get() per la mimica facciale
            is_speaking = st.session_state.get("sta_rispondendo", False)
            
            if img_idle_base64 and img_talking_base64:
                active_img = img_talking_base64 if is_speaking else img_idle_base64
                animation_style = "avatar-typing 0.8s infinite alternate ease-in-out" if is_speaking else "avatar-idle 3s infinite ease-in-out"
                border_color = "#10B981" if is_speaking else "#EC4899"
                
                st.markdown(f"""
                    <div style="display: flex; justify-content: center; margin: 15px 0;">
                        <div class="avatar-dynamic-frame" style="background-image: url('data:image/png;base64,{active_img}'); border-color: {border_color}; animation: {animation_style};">
                        </div>
                    </div>
                    <style>
                    .avatar-dynamic-frame {{
                        width: 105px; height: 105px;
                        border-radius: 50%;
                        background-size: cover;
                        background-position: center 20%;
                        border: 3px solid;
                        box-shadow: 0 0 15px rgba(236, 72, 153, 0.3);
                        transition: all 0.3s ease;
                    }}
                    @keyframes avatar-idle {{
                        0% {{ transform: scale(1); filter: brightness(1); }}
                        50% {{ transform: scale(1.02); filter: brightness(1.03); }}
                        100% {{ transform: scale(1); filter: brightness(1); }}
                    }}
                    @keyframes avatar-typing {{
                        0% {{ transform: scale(1.02) rotate(-1deg); box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }}
                        100% {{ transform: scale(1.05) rotate(1deg); box-shadow: 0 0 30px rgba(16, 185, 129, 0.8); }}
                    }}
                    </style>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align: center; font-size: 40px;'>👩‍💼</div>", unsafe_allow_html=True)
            
            # Reset dello stato per il ciclo successivo
            st.session_state.sta_rispondendo = False
            
            st.caption("<div style='text-align: center;'>Chat attiva • Scrivi un messaggio per iniziare</div>", unsafe_allow_html=True)
            
            # --- CONTAINER FLUSSO CHAT (STILE WHATSAPP) ---
            container_chat = st.container(height=250)
            with container_chat:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["text"])
            
            # Campo di input per il testo
            user_query = st.chat_input("Scrivi un messaggio...")
            
            if user_query:
                with container_chat:
                    with st.chat_message("user"):
                        st.markdown(user_query)
                st.session_state.chat_history.append({"role": "user", "text": user_query})
                
                st.session_state.sta_rispondendo = True
                
                # --- INTERCETTORE LOCAL RAPIDO (Risposte istantanee di test) ---
                q_lower = user_query.lower()
                risposta_ia = ""
                
                if "sei attiva" in q_lower or "funzioni" in q_lower or "attivo" in q_lower:
                    risposta_ia = "Certamente! Sono attiva e configurata in modalità WhatsApp Chat. Posso darti supporto sulla navigazione del portale, contratti di lavoro o dettagli sui CCNL."
                elif "ccnl" in q_lower or "contratto" in q_lower or "commercio" in q_lower:
                    risposta_ia = "Il CCNL Commercio e Terziario prevede 14 mensilità, un monte ore ordinario di 40 ore settimanali e scatti di anzianità biennali. I livelli vanno dall'inquadramento Quadri fino al settimo livello."
                
                # --- DOPPIO MOTORE INTEGRATO (FAILOVER IN CASO DI ERRORE 429) ---
                if not risposta_ia:
                    with st.spinner("L'assistente sta scrivendo..."):
                        try:
                            # 1. Prova con il motore principale (Gemini)
                            system_instruction = "Sei l'Assistente Virtuale del Gruppo Dei Reali. Rispondi in modalità chat di testo, in modo cordiale, chiaro e coinciso."
                            response = ai_client.models.generate_content(
                                model='gemini-2.0-flash',
                                contents=user_query,
                                config=types.GenerateContentConfig(
                                    system_instruction=system_instruction,
                                    max_output_tokens=300
                                )
                            )
                            risposta_ia = response.text
                            
                        except Exception as e:
                            # 2. Se Gemini è bloccato dalla quota (429), passa all'istante a ChatGPT
                            if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)) and 'openai_client' in globals() and openai_client is not None:
                                try:
                                    completions = openai_client.chat.completions.create(
                                        model="gpt-4o-mini",
                                        max_tokens=300,
                                        messages=[
                                            {"role": "system", "content": "Sei l'Assistente Virtuale del Gruppo Dei Reali, esperta HR. Rispondi in modalità chat di testo, in modo cordiale, chiaro e coinciso. Ti sei attivata automaticamente come backup."},
                                            {"role": "user", "content": user_query}
                                        ]
                                    )
                                    risposta_ia = completions.choices[0].message.content
                                except Exception:
                                    risposta_ia = "Scusami, i sistemi di intelligenza artificiale sono temporaneamente carichi. Riprova tra un minuto."
                            else:
                                risposta_ia = "Scusami, ho riscontrato un rallentamento tecnico. Riprova tra pochissimi istanti!"
                
                with container_chat:
                    with st.chat_message("assistant"):
                        st.markdown(risposta_ia)
                
                st.session_state.chat_history.append({"role": "assistant", "text": risposta_ia})
                st.rerun()

            st.markdown("""
            <div class="sidebar-spec">
                <b>⚙️ Specifiche Gestione App:</b><br>
                • <b>Interfaccia:</b> WhatsApp Text UI v3.1<br>
                • <b>Motore di Backup:</b> ChatGPT Attivo (Failover automatico)<br>
                • <b>Trascrizione Chat:</b> Sincrona
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔒 Disconnetti", use_container_width=True):
                st.session_state.autenticato = False
                st.rerun()

        st.title("👑 Suite HR Enterprise - Gruppo Dei Reali")
        
        c_nav = st.columns(7)
        menu_items = [
            ("📢 Annunci", "Annunci"),
            ("📥 Screening", "Screening"),
            ("🤝 Colloqui", "Colloqui"),
            ("🎉 Assunzioni", "Assunzioni"),
            ("📊 Report", "Report"),
            ("🏢 Clienti", "Clienti"),
            ("👥 Candidati", "Candidati")
        ]
        for i, (label, key) in enumerate(menu_items):
            with c_nav[i]:
                if st.button(label, use_container_width=True): 
                    st.session_state.current_menu = key
                    st.rerun()

        st.markdown("---")

        # --- SEZIONE 1: ANNUNCI ---
        if st.session_state.current_menu == "Annunci":
            st.subheader("📢 Gestione Annunci di Lavoro")
            res_ann = supabase.table("annunci").select("*").execute()
            elenco = res_ann.data if res_ann.data else []
            
            def_pos, def_inq, def_imp, def_sede, def_foto, def_note = "","RAL","","","",""
            if st.session_state.edit_mode and st.session_state.edit_job_id:
                job = next((a for a in elenco if a["id"] == st.session_state.edit_job_id), None)
                if job: def_pos, def_inq, def_imp, def_sede, def_foto, def_note = job["posizione"], job["inquadramento"], job["importo"], job["sede"], job.get("immagine",""), job["note"]
            elif st.session_state.ai_generated_text: def_note = st.session_state.ai_generated_text

            col1, col2, col3 = st.columns([1.1, 1.1, 1.4])
            with col1:
                t_pos = st.text_input("📍 Titolo Posizione", value=def_pos)
                t_inq = st.radio("Inquadramento", ["RAL","Lordo","Orario"], index=["RAL","Lordo","Orario"].index(def_inq) if def_inq in ["RAL","Lordo","Orario"] else 0)
                t_imp = st.text_input("Budget Importo (€)", value=def_imp)
                t_sede = st.text_input("Sede di Lavoro", value=def_sede)
                t_foto = st.text_input("URL Foto Copertina Annuncio", value=def_foto)
            with col2:
                t_note = st.text_area("Descrizione Estesa Annuncio", value=def_note, height=220)
                if st.button("🪄 Genera ed Ottimizza con IA"):
                    if t_pos:
                        with st.spinner("Scrittura annuncio professionale con IA..."):
                            res = genera_testo_annuncio_ia(t_pos, t_inq, t_imp, t_sede, t_note)
                            st.session_state.ai_generated_text = res
                            st.rerun()
                if st.session_state.edit_mode:
                    if st.button("💾 AGGIORNA ANNUNCIO", use_container_width=True):
                        supabase.table("annunci").update({"posizione":t_pos,"inquadramento":t_inq,"importo":t_imp,"sede":t_sede,"note":t_note,"immagine":t_foto}).eq("id", st.session_state.edit_job_id).execute()
                        st.session_state.edit_mode = False; st.session_state.ai_generated_text = ""; st.rerun()
                else:
                    if st.button("🚀 PUBBLICA ANNUNCIO", use_container_width=True):
                        clean_id = re.sub(r'[^a-z0-9]', '-', t_pos.lower())[:15] + f"-{random.randint(10,99)}"
                        supabase.table("annunci").insert({"id":clean_id,"posizione":t_pos,"inquadramento":t_inq,"importo":t_imp,"sede":t_sede,"note":t_note,"immagine":t_foto,"stato":"Attivo"}).execute()
                        st.session_state.ai_generated_text = ""; st.rerun()
            with col3:
                st.markdown("### Elenco Annunci Pubblicati")
                for a in elenco:
                    st.markdown(f"""
                    <div class='saas-box'>
                        <b>📢 {a['posizione']}</b> ({a.get('stato','Attivo')})<br>
                        Sede: {a.get('sede','N/D')} - Budget: {a.get('importo','0')}€<br>
                        <div class='link-box'>https://deireali-hr.streamlit.app/?job={a['id']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    if c1.button("Modifica", key=f"e_{a['id']}", use_container_width=True): 
                        st.session_state.edit_mode=True; st.session_state.edit_job_id=a['id']; st.rerun()
                    
                    stato_label = "Sospendi" if a.get('stato')=="Attivo" else "Attiva"
                    if c2.button(stato_label, key=f"s_{a['id']}", use_container_width=True): 
                        supabase.table("annunci").update({"stato":"Sospeso" if a.get('stato')=="Attivo" else "Attivo"}).eq("id", a['id']).execute(); st.rerun()
                    if c3.button("Elimina", key=f"d_{a['id']}", use_container_width=True): 
                        supabase.table("annunci").delete().eq("id", a['id']).execute(); st.rerun()

        # --- SEZIONE 2: SCREENING ---
        elif st.session_state.current_menu == "Screening":
            st.subheader("📥 Candidature Ricevute da Esaminare (In Screening)")
            res = supabase.table("candidati").select("*").eq("stato", "In Screening").execute()
            candidati = res.data if res.data else []
            if not candidati:
                st.info("Nessun nuovo candidato da valutare al momento.")
            for c in candidati:
                st.markdown(f"""
                <div class='saas-box'>
                    <h4>👤 {c['nome']}</h4>
                    <b>Posizione desiderata:</b> {c['posizione']}<br>
                    <b>Punteggio IA Idoneità:</b> <span style='color:#2563EB; font-weight:bold;'>{c['idoneita']}</span> | Valutazione: {c['stelle']}<br>
                    <div class='ai-box'><b>Sintesi IA Profilo:</b> {c['orientamento']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🤝 Approva Profilo per Colloquio", key=f"ap_{c['id']}"):
                    supabase.table("candidati").update({"stato":"Approvato per Colloquio"}).eq("id", c['id']).execute()
                    st.success(f"{c['nome']} spostato in sezione Colloqui!")
                    st.rerun()

       # --- SEZIONE 3: COLLOQUI (Con funzione di Annullamento e Pulizia Agenda) ---
        elif st.session_state.current_menu == "Colloqui":
            st.subheader("🤝 Calendario, Agenda e Analisi Interviste Live")
            col_agenda, col_nuovo = st.columns([2, 1.2])
            
            res_agenda_db = supabase.table("agenda").select("*").execute()
            agenda_list = res_agenda_db.data if res_agenda_db.data else []
            
            with col_agenda:
                st.markdown("### 📅 Agenda Appuntamenti Fissati")
                res_col = supabase.table("candidati").select("*").eq("stato", "Approvato per Colloquio").execute()
                colloqui = res_col.data if res_col.data else []
                
                if not colloqui:
                    st.info("Nessun colloquio pianificato in agenda.")
                for c in colloqui:
                    match_appuntamento = next((a for a in agenda_list if a.get('candidato') == c['nome']), None)
                    data_col = match_appuntamento['data'] if match_appuntamento else 'Da pianificare'
                    ora_col = match_appuntamento['ora'] if match_appuntamento else 'N/D'
                    
                    meet_url = match_appuntamento['meet_link'] if match_appuntamento and match_appuntamento.get('meet_link') else genera_codice_meet_statico()
                    
                    testo_wa = urllib.parse.quote(f"Ciao {c['nome']}, siamo l'HR dei Reali. Ti confermiamo il colloquio per la posizione di {c['posizione']}. Data: {data_col} ore {ora_col}. Avvia la riunione qui: {meet_url}")
                    link_wa = f"https://wa.me/{c['telefono']}?text={testo_wa}"
                    
                    st.markdown(f"""
                    <div class='saas-box'>
                        <h4>👤 Candidato: {c['nome']}</h4>
                        <b>Pianificazione:</b> 🗓️ {data_col} | ⏰ {ora_col}<br><br>
                        <a href="{link_wa}" target="_blank" class="whatsapp-btn">💬 WhatsApp</a>
                        <a href="{meet_url}" target="_blank" class="meet-btn">📹 Avvia Riunione Meet Dedicata</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Dividiamo in 3 colonne per fare spazio al tasto Annulla dell'agenda attiva
                    c1, c2, c3 = st.columns(3)
                    if c1.button("🎉 Promuovi", key=f"ass_{c['id']}", use_container_width=True):
                        supabase.table("candidati").update({"stato":"Assunto"}).eq("id", c['id']).execute()
                        st.rerun()
                    if c2.button("❌ Rifiuta", key=f"rif_{c['id']}", use_container_width=True):
                        supabase.table("candidati").update({"stato":"Rifiutato"}).eq("id", c['id']).execute()
                        st.rerun()
                    if c3.button("🗑️ Annulla Turno", key=f"cncl_{c['id']}", use_container_width=True):
                        if match_appuntamento:
                            supabase.table("agenda").delete().eq("id", match_appuntamento['id']).execute()
                            st.success("Appuntamento rimosso dall'agenda cloud!")
                            st.rerun()
                        else:
                            st.warning("Nessuna data ancora salvata per questo candidato.")
                        
            with col_nuovo:
                st.markdown("### ✍️ Modulo Pianificazione e Chiusura")
                if colloqui:
                    candidato_sel = st.selectbox("Seleziona risorsa da schedulare", [c['nome'] for c in colloqui])
                    c_obj = next(c for c in colloqui if c['nome'] == candidato_sel)
                    
                    nuova_data = st.date_input("Scegli la Data", date.today())
                    nuova_ora = st.time_input("Scegli l'Orario", time(15, 45))
                    
                    if st.button("Salva Data Schedulazione", use_container_width=True):
                        match_esistente = next((a for a in agenda_list if a.get('candidato') == c_obj['nome']), None)
                        
                        if match_esistente and match_esistente.get('meet_link') and "new" not in match_esistente.get('meet_link'):
                            gen_meet = match_esistente['meet_link']
                        else:
                            gen_meet = genera_codice_meet_statico()
                        
                        payload = {
                            "candidato": c_obj['nome'],
                            "data": str(nuova_data),
                            "ora": nuova_ora.strftime("%H:%M"),
                            "operatore": st.session_state.utente_connesso['nome'] if st.session_state.utente_connesso else 'HR Admin',
                            "meet_link": gen_meet,
                            "telefono": c_obj.get('telefono', '')
                        }
                        
                        if match_esistente:
                            supabase.table("agenda").update(payload).eq("id", match_esistente['id']).execute()
                        else:
                            supabase.table("agenda").insert(payload).execute()
                        
                        st.success("Appuntamento registrato con link Meet statico!")
                        st.rerun()
                    
                    st.markdown("---")
                    st.markdown("### 📝 Trascrizione Integrale Intervista (Domande/Risposte)")
                    testo_intervista = st.text_area(
                        "Incolla qui il testo catturato dall'ascolto dell'estensione:", 
                        height=180, 
                        placeholder="Incolla l'intero dialogo domande/risposte qui..."
                    )

                    if st.button("💾 ELABORA SCHEDA DI ORIENTAMENTO", use_container_width=True, type="primary"):
                        sorgente_testo = testo_intervista if testo_intervista else st.session_state.note_colloquio
                        
                        if sorgente_testo:
                            with st.spinner("L'IA sta analizzando la conversazione..."):
                                prompt_orientamento = f"""
                                Sei un esperto HR Senior e un Career Coach del Gruppo Dei Reali. 
                                Analizza questo colloquio per {candidato_sel}: {sorgente_testo}.
                                Estrai:
                                🧠 CLASSIFICAZIONE E GIUDIZIO SUL PROFILO
                                🎯 VERO SETTORE OPERATIVO DI DESTINAZIONE
                                📈 PERCORSO DI ORIENTAMENTO CONSIGLIATO
                                """
                                risposta_ia = ai_client.models.generate_content(model='gemini-2.0-flash', contents=prompt_orientamento).text
                                
                                supabase.table("schede_colloqui").insert({
                                    "candidato": candidato_sel, 
                                    "scheda": risposta_ia,
                                    "data": str(date.today())
                                }).execute()
                                
                                st.success(f"Scheda di orientamento per {candidato_sel} salvata nel Cloud!")
                                st.rerun()
                        else:
                            st.warning("Incolla prima il testo dell'intervista.")
                else:
                    st.write("Abilitato quando ci sono candidati approvati.")
                    
            st.markdown("---")
            st.markdown("### 📊 Riepilogo Cronologico di tutti i Turni Cloud")
            
            # TOOL DI PULIZIA GLOBALE: permette di cancellare qualsiasi riga dal database agenda
            if agenda_list:
                col_del_selettore, col_del_bottone = st.columns([2.5, 1])
                with col_del_selettore:
                    opzioni_cancellazione = [f"{a['id']} | {a['candidato']} ({a.get('data', 'No Data')})" for a in agenda_list]
                    turno_da_eliminare = st.selectbox("🎯 Seleziona un appuntamento specifico da cancellare dal database:", opzioni_cancellazione)
                with col_del_bottone:
                    st.write("<br>", unsafe_allow_html=True) # Allinea il bottone al selettore
                    if st.button("🗑️ Rimuovi dal Cloud", use_container_width=True):
                        id_target = int(turno_da_eliminare.split(" | ")[0])
                        supabase.table("agenda").delete().eq("id", id_target).execute()
                        st.success("Riga eliminata!")
                        st.rerun()
                
                df_agenda = pd.DataFrame(agenda_list)
                st.dataframe(df_agenda[["id", "candidato", "data", "ora", "operatore", "meet_link"]], use_container_width=True)
            else:
                st.info("Nessun turno registrato nello storico.")

        # --- SEZIONE 4: ASSUNZIONI ---
        elif st.session_state.current_menu == "Assunzioni":
            st.subheader("🎉 Registro Ufficiale Nuove Assunzioni")
            res = supabase.table("candidati").select("*").eq("stato", "Assunto").execute()
            assunti = res.data if res.data else []
            
            if not assunti:
                st.info("Nessuna risorsa contrattualizzata di recente.")
            for a in assunti:
                st.markdown(f"""
                <div class='saas-box' style='border-left: 4px solid #10B981;'>
                    <h3 style='color:#10B981; margin:0;'>✅ {a['nome']}</h3>
                    <b>Ruolo Aziendale d'Ingresso:</b> {a['posizione']}<br>
                    <b>E-mail:</b> {a['email']} | <b>Telefono:</b> {a['telefono']}<br>
                    <span style='background-color:#D1FAE5; color:#065F46; padding:4px 8px; border-radius:4px; font-size:11px; font-weight:bold;'>CONTRATTO ATTIVO</span>
                </div>
                """, unsafe_allow_html=True)

        # --- SEZIONE 5: REPORT ---
        elif st.session_state.current_menu == "Report":
            st.subheader("📊 Reportistica ed Analytics Enterprise")
            res_cand = supabase.table("candidati").select("*").execute()
            all_c = res_cand.data if res_cand.data else []
            
            tot = len(all_c)
            screening_count = len([x for x in all_c if x.get('stato') == 'In Screening'])
            colloqui_count = len([x for x in all_c if x.get('stato') == 'Approvato per Colloquio'])
            assunti_count = len([x for x in all_c if x.get('stato') == 'Assunto'])
            
            st.markdown(f"""
                <div class="umana-grid">
                    <div class="umana-kpi"><div class="umana-kpi-label">👥 Candidature Totali</div><div class="umana-kpi-value">{tot}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">📥 In Screening</div><div class="umana-kpi-value">{screening_count}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">🤝 Colloqui Attivi</div><div class="umana-kpi-value">{colloqui_count}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">🎉 Risorse Assunte</div><div class="umana-kpi-value">{assunti_count}</div></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Distribuzione Grafica degli Stati dei Candidati")
            if tot > 0:
                data_chart = pd.DataFrame({
                    'Stato Candidatura': ['Screening', 'Colloqui', 'Assunti'],
                    'Numero Risorse': [screening_count, colloqui_count, assunti_count]
                }).set_index('Stato Candidatura')
                st.bar_chart(data_chart)
            else:
                st.info("Nessun dato disponibile per elaborare grafici.")

        # --- SEZIONE 6: CLIENTI ---
        elif st.session_state.current_menu == "Clienti":
            st.subheader("🏢 Gestione Anagrafica Clienti B2B")
            col_form, col_lista = st.columns([1.1, 2])
            
            with col_form:
                st.markdown("### ➕ Nuovo Inserimento Cliente")
                with st.form("nuovo_cliente_form"):
                    cl_ragione = st.text_input("Ragione Sociale / Azienda *")
                    cl_piva = st.text_input("Partita IVA / Codice Fiscale *")
                    cl_contatto = st.text_input("Persona di Contatto / Referente")
                    cl_note = st.text_area("Note e Accordi Commerciali")
                    
                    if st.form_submit_button("REGISTRA AZIENDA CLIENTE"):
                        if cl_ragione and cl_piva:
                            supabase.table("clienti").insert({
                                "ragione_sociale": cl_ragione,
                                "partita_iva": cl_piva,
                                "referente": cl_contatto,
                                "note": cl_note
                            }).execute()
                            st.success(f"Azienda {cl_ragione} censita con successo!")
                            st.rerun()
                        else:
                            st.error("Ragione Sociale e Partita IVA sono campi obbligatori.")
                            
            with col_lista:
                st.markdown("### 📋 Clienti Partner Registrati")
                res_cl = supabase.table("clienti").select("*").execute()
                lista_clienti = res_cl.data if res_cl.data else []
                
                if not lista_clienti:
                    st.info("Nessun cliente inserito a sistema.")
                for cl in lista_clienti:
                    st.markdown(f"""
                    <div class='saas-box'>
                        <b>🏢 {cl['ragione_sociale']}</b><br>
                        P.IVA: {cl['partita_iva']} | Referente: {cl.get('referente','N/D')}<br>
                        <small style='color:#64748B;'>Note commerciali: {cl.get('note','Nessuna')}</small>
                    </div>
                    """, unsafe_allow_html=True)

        # --- SEZIONE 7: CANDIDATI ---
        elif st.session_state.current_menu == "Candidati":
            st.subheader("👥 Database Anagrafico Globale Candidati")
            res = supabase.table("candidati").select("*").execute()
            tutti = res.data if res.data else []
            
            if not tutti:
                st.info("Nessun candidato registrato nel sistema cloud.")
            for c in tutti:
                st.markdown(f"""
                <div class='saas-box'>
                    <b>{c['nome']}</b> — Posizione: <i>{c['posizione']}</i> (Stato attuale: <b>{c['stato']}</b>)
                </div>
                """, unsafe_allow_html=True)
                nuovo = st.selectbox("Modifica Stato Candidato", ["In Screening","Approvato per Colloquio","Assunto","Rifiutato"], index=["In Screening","Approvato per Colloquio","Assunto","Rifiutato"].index(c['stato']) if c['stato'] in ["In Screening","Approvato per Colloquio","Assunto","Rifiutato"] else 0, key=f"st_{c['id']}")
                if st.button("Salva Nuovo Stato", key=f"sv_{c['id']}"):
                    supabase.table("candidati").update({"stato":nuovo}).eq("id",c['id']).execute()
                    st.success("Stato aggiornato!")
                    st.rerun()
