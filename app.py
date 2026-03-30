import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd
from sympy import symbols, Eq, solve, diff, integrate, limit, sin, cos, tan, binomial, factorial

st.set_page_config(page_title="MathCloud - Matemática", layout="wide", page_icon="🧮")

# ===================== CSS - LETRAS VISÍVEIS =====================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1F002E, #4A0B6B); }
    .stApp, p, span, div, label { color: #F0E6FF !important; }
    h1, h2, h3 { color: #E0B0FF !important; }
    div[data-testid="stVerticalBlock"] > div > div {
        background: rgba(30, 10, 50, 0.92) !important;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(200, 150, 255, 0.25);
    }
    .stButton>button { 
        background: #C71585; 
        color: white; 
        border-radius: 12px; 
        height: 3em; 
        font-weight: bold;
    }
    .success { color: #90EE90; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ===================== MENU LATERAL =====================
st.sidebar.title("🧮 MathCloud")
opcao = st.sidebar.radio(
    "Escolha uma ferramenta:",
    [
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
    ]
)

x = symbols('x')

# ===================== INÍCIO =====================
if opcao == "Início":
    st.title("👋 Bem-vindo ao MathCloud!")
    st.markdown("### App completo de Matemática")
    st.write("Escolha qualquer ferramenta no menu lateral.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ferramentas", "14")
    col2.metric("Gráficos", "✅")
    col3.metric("Interativo", "100%")
    st.caption("Feito especialmente para você, Mateus! 🚀")

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
        a = st.number_input("a (x³)", value=1.0)
        b = st.number_input("b (x²)", value=0.0)
        c = st.number_input("c (x)", value=-2.0)
        d = st.number_input("d", value=1.0)
        func = a*x**3 + b*x**2 + c*x + d
        f_str = f"{a}x³ + {b}x² + {c}x + {d}"
    elif tipo == "Trigonométrica":
        trig = st.selectbox("Escolha", ["sin(x)", "cos(x)", "tan(x)"])
        func = sin(x) if trig == "sin(x)" else cos(x) if trig == "cos(x)" else tan(x)
        f_str = trig
    elif tipo == "Exponencial":
        base = st.number_input("Base", value=2.0)
        func = base**x
        f_str = f"{base}^x"
    else:
        f_str = st.text_input("f(x) =", "x**2 - 4*x + 3")
        func = sp.sympify(f_str)
    
    try:
        f_num = sp.lambdify(x, func, modules=['numpy'])
        y_vals = f_num(x_vals)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines',
                                name=f_str, line=dict(color='#FF69B4', width=5)))
        fig.update_layout(
            title=f"Gráfico de f(x) = {f_str}",
            xaxis_title="x",
            yaxis_title="f(x)",
            template="plotly_dark",
            height=550
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success("✅ Gráfico gerado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {str(e)}")

# ===================== OUTRAS SEÇÕES =====================
else:
    st.title(opcao)
    
    if opcao == "Álgebra Básica":
        expr = st.text_input("Digite a expressão:", "2*x**2 + 3*x - 5")
        try:
            res = sp.sympify(expr)
            val = st.number_input("Valor de x:", value=2.0)
            st.success(f"Resultado = **{res.subs(x, val)}**")
            st.latex(f"{sp.latex(res)}")
        except:
            st.error("Expressão inválida")

    elif opcao == "Resolução de Equações":
        eq = st.text_input("Digite a equação:", "x**2 - 5*x + 6 = 0")
        if st.button("Resolver"):
            try:
                lhs, rhs = [p.strip() for p in eq.split("=")]
                sol = solve(Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
                st.write("**Soluções:**")
                for s in sol:
                    st.latex(sp.latex(s))
            except:
                st.error("Não consegui resolver")

    elif opcao == "Derivadas":
        f = st.text_input("Função f(x):", "x**3 + 2*x**2 - 5*x")
        ordem = st.slider("Ordem da derivada", 1, 5, 1)
        try:
            deriv = diff(sp.sympify(f), x, ordem)
            st.latex(f"f^{{{ordem}}}(x) = {sp.latex(deriv)}")
        except:
            st.error("Função inválida")

    elif opcao == "Integrais":
        f = st.text_input("Função f(x):", "x**2 + 3*x")
        try:
            integral = integrate(sp.sympify(f), x)
            st.latex(f"\\int {sp.latex(sp.sympify(f))} dx = {sp.latex(integral)} + C")
        except:
            st.error("Função inválida")

    elif opcao == "Sistemas de Equações":
        st.write("Sistema 2x2")
        col1, col2 = st.columns(2)
        a = col1.number_input("a", value=2.0)
        b = col1.number_input("b", value=3.0)
        c = col2.number_input("c", value=8.0)
        d = col1.number_input("d", value=4.0)
        e = col1.number_input("e", value=-1.0)
        f_val = col2.number_input("f", value=7.0)
        try:
            mat = sp.Matrix([[a, b], [d, e]])
            const = sp.Matrix([c, f_val])
            sol = mat.solve(const)
            st.success(f"x = {sol[0]:.4f} | y = {sol[1]:.4f}")
        except:
            st.error("Sistema sem solução única")

    elif opcao == "Matrizes e Determinantes":
        n = st.slider("Tamanho da matriz", 2, 4, 3)
        df = pd.DataFrame(np.zeros((n, n)))
        edited = st.data_editor(df, use_container_width=True)
        mat = sp.Matrix(edited.values)
        st.write(f"**Determinante** = {mat.det()}")
        if mat.det() != 0:
            st.latex(f"Inversa = {sp.latex(mat.inv())}")

    elif opcao == "Trigonometria":
        ang = st.number_input("Ângulo (graus)", value=30.0)
        rad = np.deg2rad(ang)
        st.metric("sen", f"{np.sin(rad):.4f}")
        st.metric("cos", f"{np.cos(rad):.4f}")
        st.metric("tan", f"{np.tan(rad):.4f}")

    elif opcao == "Teorema de Pitágoras":
        a = st.number_input("Cateto a", value=3.0)
        b = st.number_input("Cateto b", value=4.0)
        c = np.sqrt(a**2 + b**2)
        st.success(f"Hipotenusa = **{c:.4f}**")

    elif opcao == "Sequências e Progressões":
        tipo = st.selectbox("Tipo", ["PA - Progressão Aritmética", "PG - Progressão Geométrica"])
        a1 = st.number_input("Primeiro termo", value=2.0)
        n = st.number_input("Número de termos", 5, 20, 10)
        if tipo.startswith("PA"):
            r = st.number_input("Razão", value=3.0)
            termos = [a1 + (k-1)*r for k in range(1, n+1)]
        else:
            r = st.number_input("Razão", value=2.0)
            termos =
