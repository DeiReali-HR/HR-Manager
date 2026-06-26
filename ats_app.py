import streamlit as st
import pandas as pd
import os
import re
import random
from datetime import date
from supabase import create_client, Client
from pypdf import PdfReader
from google import genai

# Configurazione Pagina
st.set_page_config(page_title="Dei Reali - Suite Enterprise", page_icon="👑", layout="wide")

# Connessione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
ai_client = genai.Client(api_key=st.secrets["gemini"]["api_key"])

# --- SIDEBAR GLOBALE (Presenza IA) ---
with st.sidebar:
    st.markdown("## 👑 DEI REALI")
    st.write(f"🟢 **Dionisio** (HR Director)")
    st.success("🤖 Assistente IA Attivo")
    st.markdown("---")
    st.markdown("### ✍️ Note Colloquio Live")
    if "note_colloquio" not in st.session_state: st.session_state.note_colloquio = ""
    st.session_state.note_colloquio = st.text_area("Scrivi durante il meeting:", value=st.session_state.note_colloquio, height=300)
    if st.button("🔒 Disconnetti"): st.session_state.clear(); st.rerun()

# --- NAVIGAZIONE ---
if "menu" not in st.session_state: st.session_state.menu = "Annunci"
menu_opzioni = ["Annunci", "Screening", "Colloqui", "Assunzioni", "Report", "Clienti", "Candidati"]
c_nav = st.columns(len(menu_opzioni))
for i, nome in enumerate(menu_opzioni):
    if c_nav[i].button(nome): st.session_state.menu = nome

# --- LOGICA PAGINE ---
menu = st.session_state.menu

if menu == "Colloqui":
    st.subheader("🤝 Gestione Colloqui e Report IA")
    col_agenda, col_nuovo = st.columns([2, 1])
    
    # Recupero Dati
    colloqui = supabase.table("candidati").select("*").eq("stato", "Approvato per Colloquio").execute().data
    agenda = supabase.table("agenda").select("*").execute().data
    
    with col_agenda:
        for c in colloqui:
            match = next((a for a in agenda if a['candidato'] == c['nome']), {})
            st.markdown(f"### 👤 {c['nome']}")
            st.write(f"🗓️ {match.get('data', 'Da pianificare')} ore {match.get('ora', 'N/D')}")
            
            c1, c2 = st.columns(2)
            c1.link_button("📹 Avvia Meet", "https://meet.google.com/new")
            
            # Pulsante di salvataggio collegato alla Sidebar
            if c2.button("📝 CHIUDI COLLOQUIO E SALVA", key=f"save_{c['id']}"):
                if st.session_state.note_colloquio:
                    with st.spinner("IA in elaborazione..."):
                        prompt = f"Crea un report professionale per il candidato {c['nome']} basato su queste note: {st.session_state.note_colloquio}"
                        report = ai_client.models.generate_content(model='gemini-2.0-flash', contents=prompt).text
                        # Salvataggio diretto nel database
                        supabase.table("candidati").update({"orientamento": report}).eq("id", c['id']).execute()
                        st.success("Scheda salvata nel database!")
                        st.session_state.note_colloquio = "" # Reset note
                        st.rerun()
                else:
                    st.warning("La sezione Note è vuota!")

    with col_nuovo:
        st.markdown("### ✍️ Pianificazione")
        c_sel = st.selectbox("Candidato", [c['nome'] for c in colloqui])
        d = st.date_input("Data")
        o = st.time_input("Ora")
        if st.button("Salva Appuntamento"):
            supabase.table("agenda").insert({"candidato": c_sel, "data": str(d), "ora": o.strftime("%H:%M")}).execute()
            st.success("Salvato!")
            st.rerun()

elif menu == "Annunci":
    st.subheader("📢 Annunci")
    res = supabase.table("annunci").select("*").execute().data
    st.table(pd.DataFrame(res)) if res else st.info("Nessun annuncio.")

elif menu == "Screening":
    st.subheader("📥 Screening")
    cands = supabase.table("candidati").select("*").eq("stato", "In Screening").execute().data
    for c in cands:
        st.write(f"👤 {c['nome']}")
        if st.button("Approva", key=f"ap_{c['id']}"):
            supabase.table("candidati").update({"stato": "Approvato per Colloquio"}).eq("id", c['id']).execute()
            st.rerun()

elif menu == "Assunzioni":
    st.subheader("🎉 Assunzioni")
    st.write(supabase.table("candidati").select("*").eq("stato", "Assunto").execute().data)

elif menu == "Report":
    st.subheader("📊 Report")
    data = supabase.table("candidati").select("stato").execute().data
    if data: st.bar_chart(pd.DataFrame(data)["stato"].value_counts())

elif menu == "Clienti":
    st.subheader("🏢 Clienti")
    nome = st.text_input("Ragione Sociale")
    if st.button("Aggiungi"):
        supabase.table("clienti").insert({"ragione_sociale": nome}).execute()
        st.rerun()

elif menu == "Candidati":
    st.subheader("👥 Tutti i Candidati")
    st.write(supabase.table("candidati").select("*").execute().data)
