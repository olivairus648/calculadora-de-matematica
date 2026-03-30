import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd
from sympy import symbols, Eq, solve, diff, integrate, limit, sin, cos, tan, binomial, factorial

st.set_page_config(page_title="MathCloud - Matemática", layout="wide", page_icon="🧮")

# CSS caprichado
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #2C003E, #6A1B9A); }
    div[data-testid="stVerticalBlock"] > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255,255,255,0.15);
    }
    h1, h2, h3 { color: #E0B0FF !important; }
    .stButton>button { background: #C71585; color: white; border-radius: 12px; height: 3em; font-weight: bold; }
    .success { color: #90EE90; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ===================== MENU NA BARRA LATERAL (só escolha, sem digitar) =====================
st.sidebar.title("🧮 MathCloud")
st.sidebar.markdown("**Escolha a ferramenta:**")

opcao = st.sidebar.selectbox(
    label="",  # tirei o label para ficar mais limpo
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
    label_visibility="hidden"  # esconde o rótulo para ficar mais bonito
)

# ===================== TELA INICIAL PERSONALIZADA =====================
if opcao == "Início":
    st.title("Bem-vindo ao MathCloud! 👋")
    st.markdown("### Seu app completo de Matemática")
    st.write("""
    Aqui você encontra todas as principais ferramentas de matemática de forma organizada e fácil de usar.
    
    Use o menu lateral (à esquerda) para navegar entre as calculadoras.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ferramentas", "14")
    with col2:
        st.metric("Interativo", "100%")
    with col3:
        st.metric("Gráficos", "Plotly")
    
    st.caption("Feito com carinho por Grok para você, Mateus! 🚀")
    st.image("https://picsum.photos/id/1015/800/300", use_column_width=True)  # imagem opcional bonita

# ===================== RESTO DAS FERRAMENTAS (mantidas caprichadas) =====================
else:
    st.title(opcao)
    
    x = symbols('x')

    if opcao == "Álgebra Básica":
        st.subheader("🧩 Álgebra Básica")
        expr = st.text_input("Digite a expressão:", "2*x**2 + 3*x - 5")
        try:
            resultado = sp.sympify(expr)
            st.latex(f"Expressão: {sp.latex(resultado)}")
            valor = st.number_input("Valor de x:", value=2.0)
            st.success(f"Resultado = **{resultado.subs(x, valor)}**")
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
                st.error("Não consegui resolver.")

    elif opcao == "Funções e Gráficos":
        st.subheader("📈 Funções e Gráficos")
        tipo = st.radio("Tipo de função:", 
            ["Linear (1º grau)", "Quadrática (2º grau)", "Cúbica (3º grau)", 
             "Trigonométrica", "Exponencial", "Personalizada"], horizontal=True)
        
        xmin, xmax = st.slider("Intervalo de x:", -10, 10, (-5, 5))
        x_vals = np.linspace(xmin, xmax, 600)
        
        if tipo == "Linear (1º grau)":
            a = st.number_input("a:", value=2.0)
            b = st.number_input("b:", value=-3.0)
            func = a*x + b
            f_str = f"{a}x + {b}"
        elif tipo == "Quadrática (2º grau)":
            a = st.number_input("a (x²):", value=1.0)
            b = st.number_input("b (x):", value=-4.0)
            c = st.number_input("c:", value=3.0)
            func = a*x**2 + b*x + c
            f_str = f"{a}x² + {b}x + {c}"
        # ... (o resto das funções continua igual ao código anterior)

       

    # ... (todas as outras seções continuam iguais às da versão anterior)

st.sidebar.caption("v1.0 - Feito para Mateus")
