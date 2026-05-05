import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
import urllib.parse
import base64

# ---------------- CONFIGURAÇÕES INICIAIS ----------------
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

SEU_WHATSAPP = "5541992394879" 

# Configura a página
st.set_page_config(page_title="Capita Sports | Loja Oficial", page_icon="⚽", layout="wide")

def get_image_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

# ---------------- O CSS DEFINITIVO (BLINDADO) ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    
    /* Fundo geral do site branco gelo */
    .stApp { background-color: #F5F7FA !important; }
    
    html, body, [class*="css"], p, span, div, h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    /* Remove barra do topo e rodapé do sistema */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Topo Escuro */
    .top-bar {
        background-color: #000000;
        padding: 20px 10px;
        margin-top: -60px;
        margin-bottom: 25px;
        border-bottom: 4px solid #FFD700;
        text-align: center;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Ajuste fino dos formulários de tamanho (Selectbox) */
    div[data-testid="stSelectbox"] label {
        display: none !important; /* Esconde o texto feio "Tamanho" em cima da caixa */
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border: 2px solid #EEEEEE !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- CABEÇALHO DA LOJA ----------------
logo_b64 = get_image_as_base64("logo_nova.png")
if logo_b64:
    st.markdown(f'<div class="top-bar"><img src="data:image/png;base64,{logo_b64}" style="height: 60px;"></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="top-bar"><h1 style="color: #FFF; font-weight: 900; margin: 0;">CAPITA <span style="color: #FFD700;">SPORTS</span></h1></div>', unsafe_allow_html=True)

# ---------------- BANNER PROMOCIONAL ----------------
banner_b64 = get_image_as_base64("banner.jpg")
if banner_b64:
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/jpeg;base64,{banner_b64}" style="width: 100%; max-height: 350px; object-fit: cover; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        </div>
    """, unsafe_allow_html=True)

# ---------------- SELOS RÁPIDOS ----------------
c1, c2, c3 = st.columns(3)
c1.markdown("<div style='text-align:center; font-weight:700; color:#555;'>💬 Suporte WhatsApp</div>", unsafe_allow_html=True)
c2.markdown("<div style='text-align:center; font-weight:700; color:#555;'>📦 Estoque no Brasil</div>", unsafe_allow_html=True)
c3.markdown("<div style='text-align:center; font-weight:700; color:#555;'>🔒 Compra Segura</div>", unsafe_allow_html=True)

st.markdown("<h2 style='font-weight: 900; color: #111; margin-top: 40px; margin-bottom: 20px; font-size: 24px;'>🔥 DESTAQUES DA LOJA</h2>", unsafe_allow_html=True)

# ---------------- BUSCA NO BANCO DE DADOS ----------------
@st.cache_data(ttl=60)
def buscar_estoque():
    res = supabase.table("produtos").select("*").gt("quantidade", 0).order("nome").execute()
    return res.data

produtos = buscar_estoque()

if not produtos:
    st.warning("Estoque esgotado no momento. Fique de olho no nosso Instagram!")
    st.stop()

vitrine = {}
for p in produtos:
    nome = p["nome"]
    if nome not in vitrine:
        vitrine[nome] = {"imagem": p["imagem"], "valor": p["valor"], "tamanhos_disp": []}
    vitrine[nome]["tamanhos_disp"].append(p["tamanho"])

vitrine_lista = list(vitrine.items())

# ---------------- MONTAGEM DA GRADE (CARDS HTML PURO) ----------------
for i in range(0, len(vitrine_lista), 4):
    colunas = st.columns(4)
    
    for j in range(4):
        if i + j < len(vitrine_lista):
            nome, dados = vitrine_lista[i + j]
            
            with colunas[j]:
                # PARTE 1 DO CARD (Imagem, Nome e Preço em HTML puro para ficar perfeito)
                img_src = dados["imagem"] if dados["imagem"] else "https://via.placeholder.com/400x400?text=CAPITA"
                
                st.markdown(f"""
                <div style="background-color: #FFF; padding: 15px 15px 5px 15px; border-radius: 12px 12px 0 0; border: 1px solid #EAEAEA; border-bottom: none; text-align: center;">
                    <img src="{img_src}" style="width: 100%; border-radius: 8px;">
                    <p style="color: #111; font-weight: 800; font-size: 15px; text-transform: uppercase; margin-top: 15px; margin-bottom: 0px; line-height: 1.2;">{nome}</p>
                    <p style="color: #00A650; font-weight: 900; font-size: 22px; margin-top: 5px; margin-bottom: 10px;">R$ {dados['valor']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # PARTE 2 DO CARD (Seletor de Tamanho do Streamlit)
                tamanho_escolhido = st.selectbox("Tam", dados["tamanhos_disp"], key=f"tam_{nome}")
                
                # PARTE 3 DO CARD (Botão de Comprar estilo E-commerce fechando a caixa branca)
                mensagem = f"Olá Capita Sports! ⚽\nVim pelo site e quero comprar a camisa:\n*Modelo:* {nome}\n*Tamanho:* {tamanho_escolhido}\n*Preço:* R$ {dados['valor']:.2f}"
                link_wpp = f"https://wa.me/{SEU_WHATSAPP}?text={urllib.parse.quote(mensagem)}"
                
                st.markdown(f"""
                <div style="background-color: #FFF; padding: 0px 15px 15px 15px; border-radius: 0 0 12px 12px; border: 1px solid #EAEAEA; border-top: none; text-align: center; margin-bottom: 25px;">
                    <a href="{link_wpp}" target="_blank" style="display: block; background-color: #25D366; color: white; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: 800; font-size: 15px; transition: 0.2s;">🛒 COMPRAR AGORA</a>
                </div>
                """, unsafe_allow_html=True)

# ---------------- RODAPÉ ----------------
st.write("---")
st.markdown("<p style='text-align: center; color: #999; font-size: 12px; font-weight: 600;'>© 2026 CAPITA SPORTS. Desenvolvido para alta conversão.</p>", unsafe_allow_html=True)