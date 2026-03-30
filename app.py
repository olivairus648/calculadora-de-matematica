import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd
from sympy import symbols, Eq, solve, diff, integrate, limit, sin, cos, tan, binomial, factorial

st.set_page_config(page_title="MathCloud - Matemática", layout="wide", page_icon="🧮")

# CSS Melhorado
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1F002E, #4A0B6B); }
    .stApp, p, span, div { color: #F0E6FF !important; }
    h1, h2, h3 { color: #E0B0FF !important; }
    div[data-testid="stVerticalBlock"] > div > div {
        background: rgba(30, 10, 50, 0.9) !important;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(200, 150, 255, 0.2);
    }
    .stButton>button { background: #C71585; color: white; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# MENU LATERAL
st.sidebar.title("🧮 MathCloud")
opcao = st.sidebar.radio(
    "Escolha uma ferramenta:",
    [
        "Início", "Álgebra Básica", "Resolução de Equações", "Funções e Gráficos",
        "Derivadas", "Integrais", "Sistemas de Equações", "Matrizes e Determinantes",
        "Trigonometria", "Teorema de Pitágoras", "Sequências e Progressões",
        "Combinatória", "Limites", "Estatística Básica"
    ]
)

x = symbols('x')

# ===================== INÍCIO =====================
if opcao == "Início":
    st.title("👋 Bem-vindo ao MathCloud!")
    st.write("Use o menu à esquerda para navegar entre as ferramentas.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ferramentas", "14")
    col2.metric("Gráficos", "✅")
    col3.metric("Interativo", "100%")

# ===================== FUNÇÕES E GRÁFICOS =====================
elif opcao == "Funções e Gráficos":
    st.title("📈 Funções e Gráficos")
    
    tipo = st.radio("Tipo de função:", 
        ["Linear (1º grau)", "Quadrática (2º grau)", "Cúbica (3º grau)", 
         "Trigonométrica", "Exponencial", "Personalizada"], horizontal=True)
    
    xmin, xmax = st.slider("Intervalo de x:", -10, 10, (-5, 5))
    x_vals = np.linspace(xmin, xmax, 600)
    
    if tipo == "Linear (1º grau)":
        a = st.number_input("a", value=2.0)
        b = st.number_input("b", value=-3.0)
        func = a*x + b
        f_str = f"{a}x + {b}"
    elif tipo == "Quadrática (2º grau)":
        a = st.number_input("a (x²)", value=1.0)
        b = st.number_input("b (x)", value=-4.0)
        c = st.number_input("c", value=3.0)
        func = a*x**2 + b*x + c
        f_str = f"{a}x² + {b}x + {c}"
    elif tipo == "Cúbica (3º grau)":
        a = st.number_input("
