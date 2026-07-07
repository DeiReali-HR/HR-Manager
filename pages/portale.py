import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS
st.markdown("""
<style>
    .main-wrapper { max-width: 1200px; margin: auto; font-family: sans-serif; }
    .vetrina-box { background-color: #EFF6FF; padding: 30px; border-radius: 12px; margin-bottom: 40px; display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; }
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 8px; border: 1px solid #DBEAFE; }
    .lista-container { display: flex; flex-direction: column; gap: 30px; }
    .card-editoriale { display: flex; border-bottom: 1px solid #E2E8F0; padding-bottom: 30px; gap: 30px; align-items: flex-start; }
    .img-box { width: 220px; min-width: 220px; height: 300px; background-size: cover; background-position: center; border-radius: 4px; }
    .testo-box { flex: 1; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1>🌍 Portale Carriera & Opportunità</h1>', unsafe_allow_html=True)

    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.subheader("🌟 In Vetrina")
        html_vetrina = '<div class="vetrina-box">'
        for a in evidenza:
            img = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
            html_vetrina += f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img}\');"></div></a>'
        html_vetrina += '</div>'
        st.markdown(html_vetrina, unsafe_allow_html=True)

    st.header("Tutte le posizioni")
    html_lista = '<div class="lista-container">'
    for a in annunci_vivi:
        img = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
        html_lista += f'''
        <div class="card-editoriale">
            <div class="img-box" style="background-image: url('{img}');"></div>
            <div class="testo-box">
                <h2>{a.get('posizione', 'Posizione')}</h2>
                <p>📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                <p>{str(a.get('note', ''))[:250] + '...'}</p>
                <a href="?job={a['id']}" style="font-weight:bold; color:black;">Leggi l'offerta completa ↗</a>
            </div>
        </div>
        '''
    html_lista += '</div></div>'
    st.markdown(html_lista, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
