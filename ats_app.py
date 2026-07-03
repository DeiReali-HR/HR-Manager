# --- TAB 9: PORTALE CARRIERE (LAYOUT COMPATTATO DEFINITIVO) ---
        with scelta_tab[8]:
            st.markdown("## 🌐 Portale Carriere & Vetrina Annunci")

            res_vetrina_live = supabase.table("annunci").select("*").execute()
            elenco_live = res_vetrina_live.data if res_vetrina_live.data else []
            annunci_vivi = [a for a in elenco_live if a.get("stato") != "Sospeso"]

            # --- BLOCCO VETRINA + TITOLO ELENCO (CONTENITORE UNICO) ---
            st.markdown("""
                <style>
                .custom-wrapper { margin-bottom: -15px !important; }
                .vetrina-container { display: flex; flex-direction: row; gap: 12px; overflow-x: auto; padding-bottom: 10px; }
                </style>
            """, unsafe_allow_html=True)

            with st.container():
                st.markdown("### 🌟 In Vetrina")
                annunci_flag_vetrina = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:8]
                
                if annunci_flag_vetrina:
                    html_vetrina = '<div class="vetrina-container">'
                    for a in annunci_flag_vetrina:
                        img = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                        html_vetrina += f'<a href="https://deireali-hr.streamlit.app/?job={a["id"]}" target="_blank" style="flex: 0 0 140px; aspect-ratio: 395/704; background-image: url(\'{img}\'); background-size: cover; border-radius: 8px; border: 1px solid #E2E8F0;"></a>'
                    html_vetrina += '</div>'
                    st.components.v1.html(html_vetrina, height=250, scrolling=False)
                
                # Titolo dell'elenco forzato verso l'alto
                st.markdown("<h3 style='margin-top: -20px;'>📋 Tutte le Posizioni Aperte</h3>", unsafe_allow_html=True)

            # --- ELENCO POSIZIONI ---
            col_search1, col_search2 = st.columns(2)
            ruoli = ["Tutti i Ruoli"] + sorted(list(set([a["posizione"] for a in annunci_vivi if a.get("posizione")])))
            citta = ["Tutte le Sedi"] + sorted(list(set([a["sede"] for a in annunci_vivi if a.get("sede")])))
            
            with col_search1: search_ruolo = st.selectbox("Qualifica", ruoli)
            with col_search2: search_citta = st.selectbox("Città / Sede", citta)

            annunci_da_mostrare = [a for a in annunci_vivi if a.get("in_evidenza") not in [True, 1, "true", "True"]]
            if search_ruolo != "Tutti i Ruoli": annunci_da_mostrare = [a for a in annunci_da_mostrare if a.get("posizione") == search_ruolo]
            if search_citta != "Tutte le Sedi": annunci_da_mostrare = [a for a in annunci_da_mostrare if a.get("sede") == search_citta]

            for a in annunci_da_mostrare:
                with st.container():
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        st.image(a.get("foto_annuncio") or a.get("immagine"), use_container_width=True)
                    with c2:
                        st.markdown(f"**{a['posizione']}**<br>📍 {a.get('sede')} • 💸 {a.get('importo')} €", unsafe_allow_html=True)
                        if st.button("Candidati", key=f"btn_{a['id']}"):
                            st.switch_page(f"https://deireali-hr.streamlit.app/?job={a['id']}")
                    st.divider()
