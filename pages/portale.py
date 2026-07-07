import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS Professionale
st.markdown("""
<style>
    /* Stile per la striscia dei 7 annunci in evidenza */
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 8px; border: 1px solid #E2E8F0; transition: transform 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .card-vetrina:hover { transform: scale(1.02); }

    /* Stile per la lista in basso */
    .card-orizzontale { display: flex; border: 1px solid #E2E8F0; border-radius: 12px; height: 380px; margin-bottom: 25px; overflow: hidden; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .img-lato { width: 40%; background-size: cover; background-position: center; border-right: 1px solid #E2E8F0; background-color: #f0f0f0; }
    .testo-lato { width: 60%; padding: 20px; display: flex; flex-direction: column; }
    .contenuto-scroll { flex-grow: 1; overflow-y: auto; margin-bottom: 15px; }
    .btn-black { background: #0F172A; color: white !important; padding: 12px; border-radius: 6px; text-align: center; text-decoration: none; font-weight: bold; width: 100%; display: block; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    st.title("📋 Tutte le Posizioni Aperte")
    
    # Recupero dati
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # 1. STRISCIA 7 ANNUNCI IN EVIDENZA (BOX AZZURRO INTEGRATO)
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.subheader("🌟 In Vetrina")
        
        # Creiamo un unico blocco HTML che contiene sfondo e immagini
        html_vetrina = '<div style="background-color: #EFF6FF; padding: 25px; border-radius: 12px; border: 1px solid #DBEAFE; margin-bottom: 30px; display: flex; gap: 15px;">'
        
        for a in evidenza:
            img_url = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
            # Ogni immagine è un link cliccabile
            html_vetrina += f'''
                <a href="?job={a['id']}" style="flex: 1; text-decoration: none;">
                    <div style="aspect-ratio: 395/704; background-image: url(\'{img_url}\'); background-size: cover; background-position: center; border-radius: 8px; border: 1px solid #E2E8F0; transition: transform 0.2s;">
                    </div>
                </a>
            '''
        
        html_vetrina += '</div>'
        st.markdown(html_vetrina, unsafe_allow_html=True)
        st.markdown("---")
        
    # 2. LISTA COMPLETA IN BASSO
    st.subheader("Tutte le posizioni")
    for i in range(0, len(annunci_vivi), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(annunci_vivi):
                a = annunci_vivi[i + j]
                img_url = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                with row[j]:
                    st.markdown(f"""
                    <div class="card-orizzontale">
                        <div class="img-lato" style="background-image: url('{img_url}');"></div>
                        <div class="testo-lato">
                            <div class="contenuto-scroll">
                                <h3>{a.get('posizione', 'Posizione Aperta')}</h3>
                                <p style="font-size:12px; color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                                <div style="font-size:13px;">{a.get('note', '')}</div>
                            </div>
                            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗️</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Gestione navigazione
if "job" in st.query_params:
    st.write("Redirect al form di candidatura...")
else:
    mostra_portale()
