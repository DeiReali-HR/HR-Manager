import streamlit as st
import base64
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# Stili CSS
def get_image_as_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Convertiamo l'immagine per il CSS
img_base64 = get_image_as_base64("BOX_ASS.png")

st.markdown(f"""
<style>
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    /* Banner con immagine di sfondo */
    .banner-container {{
        position: relative;
        width: 100%;
        height: 300px;
        background-image: url('data:image/png;base64,{img_base64}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        margin-bottom: 30px;
    }}
    
    .input-overlay {{
        position: absolute;
        bottom: 30px; 
        left: 50px;
        display: flex;
        gap: 10px;
        align-items: center;
    }}
    
    .riga-blu {{ border-top: 2px solid #0f172a; margin: 20px 0; width: 100%; }}
    .titolo-area {{ font-family: 'Playfair Display', serif; font-size: 0.9rem; color: #64748b; margin-top: 25px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
    .vetrina-full-width {{ background-color: #f1f5f9; margin-left: -500px; margin-right: -500px; padding: 30px 500px; margin-bottom: 30px; }}
    .grid-vetrina {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; max-width: 1400px; margin: auto; }}
    .card-vetrina {{ aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 4px; border: 1px solid #cbd5e1; }}
    .card-orizzontale {{ display: flex; border: 1px solid #e2e8f0; border-radius: 8px; background: white; margin-bottom: 10px; height: 350px; overflow: hidden; }}
    .img-lato {{ width: 35%; height: 100%; background-size: contain; background-repeat: no-repeat; background-position: center; border-right: 1px solid #e2e8f0; background-color: #f1f5f9; }}
    .testo-lato {{ width: 65%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; height: 100%; }}
    .contenuto-scrollabile {{ flex-grow: 1; overflow-y: auto; margin-bottom: 15px; padding-right: 10px; }}
    .btn-black {{ background: #0f172a; color: white !important; padding: 12px; border-radius: 4px; text-align: center; text-decoration: none; font-weight: bold; display: block; font-size: 0.9rem; flex-shrink: 0; }}
</style>
""", unsafe_allow_html=True)

def render_card(a):
    img_url = a.get("foto_annuncio") or a.get("immagine") or "https://via.placeholder.com/200x350"
    note_testo = str(a.get('note', ''))
    link_candidatura = f"https://deireali-hr.streamlit.app/?job={a['id']}"
    return f"""
    <div class="card-orizzontale">
        <div class="img-lato" style="background-image: url('{img_url}');"></div>
        <div class="testo-lato">
            <div class="contenuto-scrollabile">
                <h3 style="font-family: 'Playfair Display', serif; margin-top:0; font-size:1.2rem;">{a.get('posizione', 'Posizione')}</h3>
                <p style="font-size:0.85rem; color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                <p style="font-size:0.85rem;">{note_testo}</p>
            </div>
            <a href="{link_candidatura}" target="_blank" class="btn-black">CANDIDATI ORA ↗️</a>
        </div>
    </div>
    """

def mostra_portale():
    # Banner con Login sovrapposto
    st.markdown('<div class="banner-container"></div>', unsafe_allow_html=True)
    
    # Area sovrapposta con input e bottone
    c1, c2, c3 = st.columns([1, 2, 4]) # Posizionamento custom
    with c2:
        codice = st.text_input("Codice:", type="password", label_visibility="collapsed", key="login_banner")
    with c3:
        if st.button("ACCEDI AL PROCESSO"):
            if codice == "As2026Reali@":
                st.query_params["area_assunzione"] = "true"
                st.rerun()
            else:
                st.error("Codice errato")
    
    st.markdown('<div class="riga-blu"></div>', unsafe_allow_html=True)
    
    # Caricamento Annunci
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]
    
    # Vetrina...
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.markdown('<p class="titolo-area">In primo piano</p>', unsafe_allow_html=True)
        # ... (restante logica vetrina)
        
    st.markdown('<p class="titolo-area">Selezioni Aperte</p>', unsafe_allow_html=True)
    # ... (restante logica selezioni)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
