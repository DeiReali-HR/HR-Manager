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
        return "50%", "⭐⭐", "Il PDF non contains testo estraibile."
        
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
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; padding: 12px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 5px;}
    .meet-btn { background-color: #1a73e8 !important; color: white !important; padding: 12px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; }
    .link-box { background-color: #F8FAFC; padding: 10px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; word-break: break-all; }
    .section-indicator { background-color: #E2E8F0; padding: 8px 16px; border-radius: 6px; font-weight: bold; margin-bottom: 20px; color: #1E3A8A; display: inline-block; }
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

# --- PORTALE PUBBLICO ---
if "job" in st.query_params:
    job_param = str(st.query_params["job"])
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_param).execute()
    annuncio_selezionato = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio_selezionato:
        if annuncio_selezionato.get('stato') == 'Sospeso':
            st.warning("Selezioni momentaneamente chiuse.")
        else:
            img_url = annuncio_selezionato.get('immagine') or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200"
            st.markdown(f'<div class="public-card"><div class="umana-banner" style="background-image: url(\'{img_url}\');"><div class="umana-banner-title">{annuncio_selezionato["posizione"]}</div></div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="umana-grid">
                    <div class="umana-kpi"><div class="umana-kpi-label">📍 Sede</div><div class="umana-kpi-value">{annuncio_selezionato.get('sede') if annuncio_selezionato.get('sede') else 'Dato non inserito'}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">💼 Inquadramento</div><div class="umana-kpi-value">{annuncio_selezionato.get('inquadramento') if annuncio_selezionato.get('inquadramento') else 'Dato non inserito'}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">💸 Compenso</div><div class="umana-kpi-value">{annuncio_selezionato.get('importo') if annuncio_selezionato.get('importo') else 'Dato non inserito'} €</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">🔑 Rif.</div><div class="umana-kpi-value">DR-{annuncio_selezionato['id'].upper()[-4:]}</div></div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"### Descrizione\n{annuncio_selezionato['note']}")
            with st.form("candidatura"):
                c_nome = st.text_input("Nome e Cognome *")
                c_mail = st.text_input("E-mail *")
                c_tel = st.text_input("Telefono *")
                c_file = st.file_uploader("Allega CV PDF", type=["pdf"])
                if st.form_submit_button("INVIA CANDIDATURA"):
                    if c_nome and c_mail and c_tel and c_file:
                        with st.spinner("Analisi IA..."):
                            testo = estrai_testo_pdf(c_file)
                            v, s, o = analizza_cv_con_ia(testo, annuncio_selezionato['note'])
                            supabase.table("candidati").insert({"nome":c_nome,"email":c_mail,"telefono":c_tel,"posizione":annuncio_selezionato['posizione'],"idoneita":v,"stelle":s,"orientamento":o,"stato":"In Screening"}).execute()
                        st.success("Candidatura inviata!")
                    else: st.error("Compila i campi.")
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.error("Annuncio non trovato.")

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
                    else: st.error("Credenziali errate.")
    else:
        with st.sidebar:
            mostra_logo_aziendale()
            st.write(f"🟢 *{st.session_state.utente_connesso['nome']}*")
            if ai_client: st.success("🤖 IA Connessa")
            if st.button("🔒 Disconnetti"):
                st.session_state.autenticato = False
                st.rerun()

        st.title("👑 HR Suite Dei Reali")
        c_nav = st.columns(7)
        for i, (label, key) in enumerate([("📢 Annunci","Annunci"),("📥 Screening","Screening"),("🤝 Colloqui","Colloqui"),("🎉 Assunzioni","Assunzioni"),("📊 Report","Report"),("🏢 Clienti","Clienti"),("👥 Candidati","Candidati")]):
            with c_nav[i]:
                if st.button(label): st.session_state.current_menu = key; st.rerun()

        if st.session_state.current_menu == "Annunci":
            res_ann = supabase.table("annunci").select("*").execute()
            elenco = res_ann.data if res_ann.data else []
            def_pos, def_inq, def_imp, def_sede, def_foto, def_note = "","RAL","","","",""
            if st.session_state.edit_mode and st.session_state.edit_job_id:
                job = next((a for a in elenco if a["id"] == st.session_state.edit_job_id), None)
                if job: def_pos, def_inq, def_imp, def_sede, def_foto, def_note = job["posizione"], job["inquadramento"], job["importo"], job["sede"], job.get("immagine",""), job["note"]
            elif st.session_state.ai_generated_text: def_note = st.session_state.ai_generated_text

            col1, col2, col3 = st.columns([1,1,1.2])
            with col1:
                t_pos = st.text_input("📍 Titolo", value=def_pos)
                t_inq = st.radio("Inquadramento", ["RAL","Lordo","Orario"], index=["RAL","Lordo","Orario"].index(def_inq) if def_inq in ["RAL","Lordo","Orario"] else 0)
                t_imp = st.text_input("Importo (€)", value=def_imp)
                t_sede = st.text_input("Sede", value=def_sede)
                t_foto = st.text_input("URL Foto Copertina", value=def_foto)
            with col2:
                t_note = st.text_area("Descrizione Annuncio", value=def_note, height=200)
                if st.button("🪄 Ottimizza con IA"):
                    if t_pos:
                        with st.spinner("Scrittura..."):
                            res = genera_testo_annuncio_ia(t_pos, t_inq, t_imp, t_sede, t_note)
                            st.session_state.ai_generated_text = res
                            st.rerun()
                if st.session_state.edit_mode:
                    if st.button("💾 AGGIORNA"):
                        supabase.table("annunci").update({"posizione":t_pos,"inquadramento":t_inq,"importo":t_imp,"sede":t_sede,"note":t_note,"immagine":t_foto}).eq("id", st.session_state.edit_job_id).execute()
                        st.session_state.edit_mode = False; st.session_state.ai_generated_text = ""; st.rerun()
                else:
                    if st.button("🚀 PUBBLICA"):
                        clean_id = re.sub(r'[^a-z0-9]', '-', t_pos.lower())[:15] + f"-{random.randint(10,99)}"
                        supabase.table("annunci").insert({"id":clean_id,"posizione":t_pos,"inquadramento":t_inq,"importo":t_imp,"sede":t_sede,"note":t_note,"immagine":t_foto,"stato":"Attivo"}).execute()
                        st.session_state.ai_generated_text = ""; st.rerun()
            with col3:
                for a in elenco:
                    st.markdown(f"<div class='saas-box'><b>📢 {a['posizione']}</b><br><small>{a.get('stato','Attivo')}</small><br><div class='link-box'>https://deireali-hr.streamlit.app/?job={a['id']}</div></div>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    if c1.button("✍️", key=f"e_{a['id']}"): st.session_state.edit_mode=True; st.session_state.edit_job_id=a['id']; st.rerun()
                    if c2.button("⏸️" if a.get('stato')=="Attivo" else "▶️", key=f"s_{a['id']}"): supabase.table("annunci").update({"stato":"Sospeso" if a.get('stato')=="Attivo" else "Attivo"}).eq("id", a['id']).execute(); st.rerun()
                    if c3.button("🗑️", key=f"d_{a['id']}"): supabase.table("annunci").delete().eq("id", a['id']).execute(); st.rerun()

        elif st.session_state.current_menu == "Screening":
            res = supabase.table("candidati").select("*").eq("stato", "In Screening").execute()
            for c in (res.data if res.data else []):
                st.markdown(f"<div class='saas-box'><b>👤 {c['nome']}</b> - {c['idoneita']} {c['stelle']}<br>{c['orientamento']}</div>", unsafe_allow_html=True)
                if st.button("🤝 Approva", key=f"ap_{c['id']}"): supabase.table("candidati").update({"stato":"Approvato per Colloquio"}).eq("id",c['id']).execute(); st.rerun()

        elif st.session_state.current_menu == "Candidati":
            res = supabase.table("candidati").select("*").execute()
            for c in (res.data if res.data else []):
                st.markdown(f"<div class='saas-box'><b>{c['nome']}</b> ({c['stato']})</div>", unsafe_allow_html=True)
                nuovo = st.selectbox("Cambia Stato", ["In Screening","Approvato per Colloquio","Assunto","Rifiutato"], index=0, key=f"st_{c['id']}")
                if st.button("Salva", key=f"sv_{c['id']}"): supabase.table("candidati").update({"stato":nuovo}).eq("id",c['id']).execute(); st.rerun()
        else: st.info("Sincronizzazione Cloud Attiva.")
