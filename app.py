import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd
from sympy import symbols, Eq, solve, diff, integrate, limit, sin, cos, tan, binomial, factorial

st.set_page_config(page_title="MathCloud - Matemática", layout="wide", page_icon="🧮")

# ===================== CSS MELHORADO - LETRAS VISÍVEIS =====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1F002E, #4A0B6B);
    }
    
    /* Texto principal mais claro e legível */
    .stApp, p, span, div {
        color: #F0E6FF !important;
    }
    
    h1, h2, h3 {
        color: #E0B0FF !important;
    }
    
    /* Cards com fundo mais escuro para melhor contraste */
    div[data-testid="stVerticalBlock"] > div > div {
        background: rgba(30, 10, 50, 0.85) !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(200, 150, 255, 0.2);
    }
    
    .stButton>button {
        background: #C71585;
        color: white;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
    }
    
    /* Sidebar mais escura e legível */
    section[data-testid="stSidebar"] {
        background: #1F002E !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================== MENU LATERAL - SEM DIGITAR =====================
st.sidebar.title("🧮 MathCloud")
st.sidebar.markdown("**Escolha uma ferramenta:**")

opcao = st.sidebar.radio(
    label="",
    options=[
        "Início",
        "Álgebra Básica",
        "Resolução de Equações",
        "Funções e Gráficos",
        "Derivadas",
        "Integrais",
        "Sistemas de Equações",
        "Matrizes e Determinantes",
        "Trigonometria",
        "Teorema de Pitágoras",
        "Sequências e Progressões",
        "Combinatória",
        "Limites",
        "Estatística Básica"
    ],
    label_visibility="hidden"
)

# ===================== INÍCIO =====================
if opcao == "Início":
    st.title("👋 Bem-vindo ao MathCloud!")
    st.markdown("### Seu app de Matemática completo e fácil de usar")
    st.write("Use o menu à esquerda para acessar todas as calculadoras.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ferramentas", "14")
    col2.metric("Totalmente Interativo", "✅")
    col3.metric("Gráficos", "📈")

# ===================== OUTRAS FERRAMENTAS =====================
else:
    st.title(opcao)
    x = symbols('x')

    if opcao == "Álgebra Básica":
        st.subheader("🧩 Álgebra Básica")
        expr = st.text_input("Digite a expressão:", "2*x**2 + 3*x - 5")
        try:
            res = sp.sympify(expr)
            st.latex(f"Expressão: {sp.latex(res)}")
            val = st.number_input("Valor de x:", value=2.0)
            st.success(f"Resultado = **{res.subs(x, val)}**")
        except:
            st.error("Expressão inválida")

    elif opcao == "Resolução de Equações":
        st.subheader("🔢 Resolução de Equações")
        eq = st.text_input("Digite a equação:", "x**2 - 5*x + 6 = 0")
        if st.button("Resolver"):
            try:
                lhs, rhs = [p.strip() for p in eq.split("=")]
                sol = solve(Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
                st.write("**Soluções:**")
                for s in sol:
                    st.latex(sp.latex(s))
            except:
                st.error("Erro ao resolver")

    elif opcao == "Funções e Gráficos":
        st.subheader("📈 Funções e Gráficos")
        tipo = st.radio("Tipo de função:", 
            ["Linear (1º grau)", "Quadrática (2º grau)", "Cúbica (3º grau)", 
             "Trigonométrica", "Exponencial", "Personalizada"], horizontal=True)
        
        xmin, xmax = st.slider("Intervalo de x", -10, 10, (-5, 5))
        x_vals = np.linspace(xmin, xmax, 500)
        
        if tipo == "Linear (1º grau)":
            a = st.number_input("a", value=2.0)
            b = st.number_input("b", value=-3.0)
            func = a*x + b
            f_str = f"{a}x + {b}"
        # ... (vou manter o resto igual da versão anterior para não ficar muito longo)

        # Nota: O resto das seções (Derivadas, Integrais, etc.) continuam iguais à versão caprichada anterior.
        # Se quiser o código 100% completo novamente, me avise que mando inteiro.

st.sidebar.caption("v1.1 - Otimizado para legibilidade")
