import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS "Hard-Coded" per evitare conflitti con Streamlit
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
    
    .page-container { font-family: 'Inter', sans-serif; }
    .epigrafe { font-size: 1.1rem; color: #475569; font-style: italic; margin-bottom: 20px; }
    .titolo-editoriale { font-family: 'Playfair Display', serif; font-size: 3.5rem; color: #0F172A; margin-bottom: 40px; }
    
    .box-vetrina-esterno { 
        background-color: #EFF6FF !important; 
        padding: 30px !important; 
        border-radius: 12px !important; 
        border: 1px solid #DBEAFE !important; 
        margin-bottom: 40px !important;
    }
    .flex-vetrina { display: flex; gap: 15px; overflow-x: auto; }
    .card-vetrina { min-width: 150px; flex: 1; aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 8px; border: 1px solid #E2E8F0; }
    
    .card-editoriale { display: flex; border-bottom: 1px solid #E2E8F0; padding: 40px 0; }
    .img-box { width: 220px; height: 300px; background-size: cover; background-position: center; border-radius: 4px; margin-right: 30px; }
    .testo-box { flex: 1; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # Renderizziamo tutto in un unico blocco HTML per prevenire "rotture"
    html_finale = '<div class="page-container">'
    html_finale += '<p class="epigrafe">Abbiamo dato spazio al valore e messo le persone al centro: ora tocca a te. Esplora le nostre opportunità d\'impiego sempre aggiornate e trova la posizione ideale per le tue competenze.</p>'
    html_finale += '<h1 class="titolo-editoriale">🌍 Portale Carriera & Opportunità</h1>'

    # Vetrina
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        html_finale += '<h3>🌟 In Vetrina</h3><div class="box-vetrina-esterno"><div class="flex-vetrina">'
        for a in evidenza:
            img = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
            html_finale += f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img}\');"></div></a>'
        html_finale += '</div></div>'

    # Lista
    html_finale += '<h2>Tutte le posizioni</h2>'
    for a in annunci_vivi:
        img = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
        html_finale += f'''
        <div class="card-editoriale">
            <div class="img-box" style="background-image: url('{img}');"></div>
            <div class="testo-box">
                <h2 style="font-family: 'Playfair Display', serif;">{a.get('posizione', 'Posizione')}</h2>
                <p>📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                <p>{a.get('note', '')[:300] + '...'}</p>
                <a href="?job={a['id']}" style="color: #0F172A; font-weight: bold;">Leggi l'offerta completa ↗</a>
            </div>
        </div>
        '''
    html_finale += '</div>'
    st.markdown(html_finale, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
