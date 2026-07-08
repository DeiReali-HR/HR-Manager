# --- TAB 9: PORTALE CARRIERE (GRIGLIA A 2 COLONNE) ---
        with scelta_tab[8]:
            st.markdown("## 🌐 Portale Carriere & Vetrina Annunci")
            st.caption("Layout ottimizzato: le card sono bloccate a un'altezza di 382px per una visualizzazione perfetta.")

            # 1. Rilettura annunci real-time da Supabase
            res_vetrina_live = supabase.table("annunci").select("*").execute()
            elenco_live = res_vetrina_live.data if res_vetrina_live.data else []
            annunci_vivi = [a for a in elenco_live if a.get("stato") != "Sospeso"]

            # 2. VETRINA SUPERIORE
            annunci_flag_vetrina = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
            st.markdown("### 🌟 In Vetrina (Selezionati)")
            if not annunci_flag_vetrina:
                st.info("Spunta il flag 'In Vetrina' nella gestione annunci per popolare questa sezione.")
            else:
                cols = st.columns(7)
                for index, a in enumerate(annunci_flag_vetrina):
                    img_v_url = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                    with cols[index]:
                        st.markdown(f'''
                            <a href="/?job={a['id']}" 
                               style="display: block; width: 100%; aspect-ratio: 395/704; 
                               background-image: url(\'{img_v_url}\'); background-size: cover; 
                               background-position: center; border-radius: 8px; border: 1px solid #E2E8F0;">
                            </a>
                        ''', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📋 Tutte le Posizioni Aperte")

            # 3. FILTRI
            ruoli_disponibili = sorted(list(set([a["posizione"] for a in annunci_vivi if a.get("posizione")])))
            citta_disponibili = sorted(list(set([a["sede"] for a in annunci_vivi if a.get("sede")])))
            
            col_search1, col_search2 = st.columns(2)
            with col_search1:
                search_ruolo = st.selectbox("🔍 Cosa stai cercando? (Qualifica)", ["Tutti i Ruoli"] + ruoli_disponibili)
            with col_search2:
                search_citta = st.selectbox("📍 Dove? (Città / Sede)", ["Tutte le Sedi"] + citta_disponibili)

            # Filtriamo gli annunci
            annunci_filtrati = [a for a in annunci_vivi if a.get("in_evidenza") not in [True, 1, "true", "True"]]
            if not annunci_filtrati: annunci_filtrati = annunci_vivi
            if search_ruolo != "Tutti i Ruoli": annunci_filtrati = [a for a in annunci_filtrati if a.get("posizione") == search_ruolo]
            if search_citta != "Tutte le Sedi": annunci_filtrati = [a for a in annunci_filtrati if a.get("sede") == search_citta]

            # 4. GRIGLIA ANNUNCI
            st.markdown("<div class='showcase-grid-2columns'>", unsafe_allow_html=True)
            
            # Utilizziamo un semplice ciclo per creare le card
            for i in range(0, len(annunci_filtrati), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(annunci_filtrati):
                        a = annunci_filtrati[i + j]
                        img_a = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                        
                        with cols[j]:
                            st.markdown(f"""
                            <div class="showcase-card-row">
                                <div class="showcase-img-side" style="background-image: url('{img_a}');"></div>
                                <div class="showcase-content-side">
                                    <div class="showcase-scrollable-body">
                                        <div class="showcase-title">{a.get('posizione', 'Posizione')}</div>
                                        <div class="showcase-meta-grid">📍 {a.get('sede', 'Roma')} | 💼 {a.get('inquadramento', 'RAL')}</div>
                                        <div class="showcase-text">{a.get('note', '')}</div>
                                    </div>
                                    <a href="/?job={a['id']}" class="showcase-btn">CANDIDATI ORA ↗️</a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
