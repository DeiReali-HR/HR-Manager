import streamlit as st
import pandas as pd
import json
import random
from datetime import datetime

st.set_page_config(page_title="Zenith ATS & HR Manager", page_icon="💼", layout="wide")

if 'jobs' not in st.session_state:
    st.session_state.jobs = [
        {"id": "JOB-001", "titolo": "Senior Python Developer", "cliente": "TechCorp S.r.l.", "stato": "Attivo", "link": "https://ats.zenith.hr/jobs/python-dev"},
        {"id": "JOB-002", "titolo": "Social Media Manager", "cliente": "Inbound Marketing SpA", "stato": "Bozza", "link": ""},
    ]

if 'candidates' not in st.session_state:
    st.session_state.candidates = [
        {"id": "CAND-001", "nome": "Marco Rossi", "competenze": "Python, Django, PostgreSQL", "formazione": "Laurea Informatica", "punteggio": 9, "stato": "Colloquio", "annuncio": "Senior Python Developer"},
        {"id": "CAND-002", "nome": "Giulia Bianchi", "competenze": "React, TypeScript, CSS", "formazione": "Master Front-End", "punteggio": 7, "stato": "Nuovo", "annuncio": "Senior Python Developer"},
        {"id": "CAND-003", "nome": "Alessandro Neri", "competenze": "Copywriting, ADV, SEO", "formazione": "Laurea Comunicazione", "punteggio": 8, "stato": "Assunto", "annuncio": "Social Media Manager"},
    ]

if 'clients' not in st.session_state:
    st.session_state.clients = [
        {"id": "CLI-001", "nome": "TechCorp S.r.l.", "settore": "IT & Software", "referente": "Ing. Riva"},
        {"id": "CLI-002", "nome": "Inbound Marketing SpA", "settore": "Digital Agency", "referente": "Dott.ssa Ferro"},
    ]

if 'interviews' not in st.session_state:
    st.session_state.interviews = []

st.sidebar.title("💼 Zenith ATS v1.0")
st.sidebar.caption("AI-Powered Recruitment Platform")
st.sidebar.markdown(f"*Utenti attivi:* 1/10 | *CV in Database:* {len(st.session_state.candidates)}/10000")

menu = st.sidebar.radio("Navigazione Aree:", [
    "📢 Creazione & Pubblicazione Annunci",
    "📥 Screening CV & Classificazione AI",
    "🤝 Area Colloqui (AI Assistant)",
    "🎉 Conferma Assunzione & Risorse",
    "📊 Report Attività & Analytics",
    "🏢 Elenco Clienti",
    "👥 Database Candidati Totale"
])

st.sidebar.divider()
st.sidebar.info("🤖 Intelligenza Artificiale connessa tramite API Gemini (Piano a consumo)")

if menu == "📢 Creazione & Pubblicazione Annunci":
    st.header("📢 Creazione e Pubblicazione Annunci con AI")
    st.subheader("Inserisci le informazioni di base per generare l'annuncio")
    col1, col2 = st.columns(2)
    with col1:
        titolo_job = st.text_input("Titolo della posizione", placeholder="es. Junior Data Analyst")
        cliente_job = st.selectbox("Seleziona Cliente", [c["nome"] for c in st.session_state.clients])
        competenze_req = st.text_area("Competenze chiave richieste (separate da virgola)", placeholder="es. SQL, Tableau, Excel")
        esperienza = st.slider("Anni di esperienza richiesti", 0, 10, 2)
    with col2:
        st.markdown("*🤖 Assistente Scrittura AI (Gemini):*")
        tono = st.selectbox("Tono dell'annuncio", ["Professionale", "Moderno/Startup", "Istituzionale"])
        if st.button("Genera/Ottimizza Annuncio con AI ✨"):
            if titolo_job:
                with st.spinner("Gemini sta elaborando..."):
                    testo_ai = f"### Offerta di Lavoro: {titolo_job} ({tono})\n\n*Azienda:* {cliente_job}\n\nCerchiamo un profilo con {esperienza} anni di esperienza in *{competenze_req}*."
                    st.session_state['last_generated_job'] = testo_ai
            else:
                st.error("Inserisci il titolo!")
    if 'last_generated_job' in st.session_state:
        st.markdown("---")
        edited_annuncio = st.text_area("Testo definitivo", value=st.session_state['last_generated_job'], height=250)
        if st.button("Conferma e Genera Pagina Web 🌐"):
            new_link = f"https://ats.zenith.hr/jobs/{titolo_job.lower().replace(' ', '-')}"
            st.session_state.jobs.append({"id": f"JOB-00{len(st.session_state.jobs)+1}", "titolo": titolo_job, "cliente": cliente_job, "stato": "Attivo", "link": new_link})
            st.success("🎉 Pagina Web dell'annuncio generata!")
            st.code(new_link)
    st.markdown("---")
    st.dataframe(pd.DataFrame(st.session_state.jobs), use_container_width=True)

elif menu == "📥 Screening CV & Classificazione AI":
    st.header("📥 Archivio CV & Analisi Predittiva AI")
    uploaded_files = st.file_uploader("Carica i file dei CV (PDF, DOCX)", accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files:
            if f.name not in [c["nome"] for c in st.session_state.candidates]:
                st.session_state.candidates.append({
                    "id": f"CAND-00{len(st.session_state.candidates)+1}", "nome": f.name.split(".")[0].title(),
                    "competenze": "Rilevate dall'AI", "formazione": "Analizzata dal CV",
                    "punteggio": random.randint(5, 10), "stato": "Nuovo", "annuncio": st.session_state.jobs[0]["titolo"]
                })
        st.success("CV analizzati con successo da Gemini!")
    df_cand = pd.DataFrame(st.session_state.candidates).sort_values(by="punteggio", ascending=False)
    st.data_editor(df_cand, column_config={"punteggio": st.column_config.ProgressColumn("Punteggio AI Match", min_value=1, max_value=10, format="%d")}, disabled=True, use_container_width=True)

elif menu == "🤝 Area Colloqui (AI Assistant)":
    st.header("🤝 Sala Colloqui Online Virtuale con Copilot AI")
    candidato_sel = st.selectbox("Seleziona candidato", [c["nome"] for c in st.session_state.candidates])
    if st.button("Inizia Colloquio Ora 🚀"):
        st.session_state.interviews.append({"candidato": candidato_sel, "data": datetime.now().strftime("%d/%m/%Y %H:%M"), "stato": "In Corso"})
    if st.session_state.interviews and st.session_state.interviews[-1]["stato"] == "In Corso":
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1: st.image("https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=400", caption="Streaming Video")
        with c2:
            st.markdown("#### 🤖 Suggerimenti Live di Gemini AI:")
            st.warning("💡 *Domanda Consigliata:* 'Chiedi come ha gestito l'ottimizzazione delle query nell'ultimo progetto.'")
            if st.button("Termina Colloquio e Salva 💾"):
                st.session_state.interviews[-1]["stato"] = "Completato"
                st.rerun()
    if st.session_state.interviews and st.session_state.interviews[-1]["stato"] == "Completato":
        st.markdown("---")
        st.success("### 📝 Scheda di Valutazione Finale (Generata da Gemini)")
        st.markdown(f"*Candidato:* {st.session_state.interviews[-1]['candidato']}\n\n* *Competenze Tecniche:* 8.5/10\n* *Soft Skills:* 9/10\n\n*Il candidato dimostra ottime capacità organizzative.*")

elif menu == "🎉 Conferma Assunzione & Risorse":
    st.header("🎉 Area Conferma Assunzione e Assegnazione")
    cand_assunto = st.selectbox("Candidato da Assumere", [c["nome"] for c in st.session_state.candidates])
    cliente_dest = st.selectbox("Assegna al Cliente", [c["nome"] for c in st.session_state.clients])
    if st.button("Conferma Assunzione e Genera Lettera 📝"):
        st.balloons()
        st.success(f"Risorsa '{cand_assunto}' configurata per '{cliente_dest}'!")
        for c in st.session_state.candidates:
            if c["nome"] == cand_assunto: c["stato"] = "Assunto"

elif menu == "📊 Report Attività & Analytics":
    st.header("📊 Area Report Attività & Analytics")
    st.metric("Totale CV Gestiti", f"{len(st.session_state.candidates)} / 10000")
    st.line_chart(pd.DataFrame({'Mese': ['Gen', 'Feb', 'Mar'], 'CV': [120, 240, len(st.session_state.candidates)]}).set_index('Mese'))

elif menu == "🏢 Elenco Clienti":
    st.header("🏢 Registro Aziende Clienti")
    st.dataframe(pd.DataFrame(st.session_state.clients), use_container_width=True)

elif menu == "👥 Database Candidati Totale":
    st.header("👥 Elenco Globale Candidati")
    st.dataframe(pd.DataFrame(st.session_state.candidates), use_container_width=True)