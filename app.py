import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd

# ===================== CONFIGURAÇÃO VISUAL (igual ao de Física) =====================
st.set_page_config(page_title="MathCloud - Matemática", layout="wide", page_icon="🧮")

# CSS roxo escuro suave com cards blur (mesmo estilo que você curtiu no app de Física)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #2C003E, #6A1B9A);
        color: white;
    }
    .card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    h1, h2, h3 {
        color: #E0B0FF;
    }
    .stButton>button {
        background: #C71585;
        color: white;
        border-radius: 10px;
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧮 MathCloud - Calculadora de Matemática")
st.markdown("**Versão Matemática** do seu app de Física. Contas, equações, funções, gráficos e muito mais!")

# ===================== MENU (igual ao de Física) =====================
opcao = st.selectbox(
    "Escolha a ferramenta de Matemática:",
    [
        "Início",
        "Álgebra Básica",
        "Resolução de Equações",
        "Funções e Gráficos",
        "Derivadas",
        "Integrais",
        "Matrizes e Determinantes",
        "Trigonometria",
        "Estatística"
    ]
)

# ===================== INÍCIO =====================
if opcao == "Início":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/1015/1200/400", use_column_width=True)
    st.subheader("Bem-vindo ao MathCloud! 👋")
    st.write("Aqui você tem tudo de matemática em um único app bonito e rápido, igual ao seu de Física.")
    st.write("Use o menu lateral para navegar entre cálculos, equações, funções, gráficos interativos e muito mais.")
    st.caption("Feito por Grok especialmente para você, Mateus! 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== ÁLGEBRA BÁSICA =====================
elif opcao == "Álgebra Básica":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/201/1200/400", use_column_width=True)
    st.subheader("🧩 Álgebra Básica")
    expr = st.text_input("Digite uma expressão (ex: 2*x**2 + 3*x - 5)", "x**2 + 3*x - 4")
    x = sp.symbols('x')
    try:
        resultado = sp.sympify(expr)
        st.latex(f"Expressão simplificada: {sp.latex(resultado)}")
        valor_x = st.number_input("Valor de x para calcular:", value=2.0)
        st.success(f"Resultado = {resultado.subs(x, valor_x)}")
    except:
        st.error("Expressão inválida")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== RESOLUÇÃO DE EQUAÇÕES =====================
elif opcao == "Resolução de Equações":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/1016/1200/400", use_column_width=True)
    st.subheader("🔢 Resolução de Equações")
    eq = st.text_input("Digite a equação (ex: x**2 - 5*x + 6 = 0)", "x**2 - 5*x + 6 = 0")
    if st.button("Resolver"):
        try:
            x = sp.symbols('x')
            lhs, rhs = eq.split('=')
            solucao = sp.solve(sp.Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
            st.write("**Soluções:**")
            for s in solucao:
                st.latex(sp.latex(s))
        except:
            st.error("Não consegui resolver. Verifique a equação.")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== FUNÇÕES E GRÁFICOS =====================
elif opcao == "Funções e Gráficos":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/1005/1200/400", use_column_width=True)
    st.subheader("📈 Funções e Gráficos Interativos")
    f = st.text_input("Digite a função f(x) =", "x**2 - 4*x + 3")
    xmin, xmax = st.slider("Intervalo de x", -10, 10, (-5, 5))
    x = sp.symbols('x')
    try:
        func = sp.sympify(f)
        f_num = sp.lambdify(x, func, 'numpy')
        x_vals = np.linspace(xmin, xmax, 500)
        y_vals = f_num(x_vals)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f, line=dict(color='#C71585', width=4)))
        fig.update_layout(title=f"Gráfico de {f}", xaxis_title="x", yaxis_title="f(x)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Função inválida")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== DERIVADAS =====================
elif opcao == "Derivadas":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/133/1200/400", use_column_width=True)
    st.subheader("📐 Derivadas")
    f = st.text_input("Função f(x) =", "x**3 + 2*x**2 - 5*x")
    ordem = st.number_input("Ordem da derivada", 1, 5, 1)
    x = sp.symbols('x')
    func = sp.sympify(f)
    deriv = sp.diff(func, x, ordem)
    st.latex(f"f^{{{ordem}}}(x) = {sp.latex(deriv)}")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== INTEGRAIS =====================
elif opcao == "Integrais":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/180/1200/400", use_column_width=True)
    st.subheader("📏 Integrais")
    f = st.text_input("Função f(x) =", "x**2 + 3*x")
    x = sp.symbols('x')
    func = sp.sympify(f)
    integral = sp.integrate(func, x)
    st.latex(f"\\int {sp.latex(func)} \\, dx = {sp.latex(integral)} + C")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== MATRIZES =====================
elif opcao == "Matrizes e Determinantes":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/251/1200/400", use_column_width=True)
    st.subheader("🔢 Matrizes e Determinantes")
    n = st.slider("Tamanho da matriz (n × n)", 2, 5, 3)
    df = pd.DataFrame(np.zeros((n, n)), columns=[f"Col {i+1}" for i in range(n)])
    edited_df = st.data_editor(df, num_rows="fixed")
    mat = sp.Matrix(edited_df.values)
    st.latex(f"Matriz = {sp.latex(mat)}")
    st.write(f"**Determinante** = {mat.det()}")
    if mat.det() != 0:
        st.latex(f"Inversa = {sp.latex(mat.inv())}")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== TRIGONOMETRIA =====================
elif opcao == "Trigonometria":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/101/1200/400", use_column_width=True)
    st.subheader("📐 Trigonometria")
    ang = st.number_input("Ângulo em graus", value=30.0)
    rad = np.deg2rad(ang)
    st.write(f"**sen({ang}°) =** {np.sin(rad):.4f}")
    st.write(f"**cos({ang}°) =** {np.cos(rad):.4f}")
    st.write(f"**tan({ang}°) =** {np.tan(rad):.4f}")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== ESTATÍSTICA =====================
elif opcao == "Estatística":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://picsum.photos/id/1005/1200/400", use_column_width=True)
    st.subheader("📊 Estatística Básica")
    dados = st.text_input("Digite os números separados por vírgula", "2, 4, 4, 4, 5, 5, 7, 9")
    try:
        nums = np.array([float(x) for x in dados.split(',')])
        st.write(f"**Média** = {np.mean(nums):.2f}")
        st.write(f"**Mediana** = {np.median(nums):.2f}")
        st.write(f"**Desvio padrão** = {np.std(nums):.2f}")
        
        fig = go.Figure()
        fig.add_trace(go.Box(y=nums, name="Boxplot"))
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Insira números válidos")
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("✅ App feito por Grok especialmente para você. Deploy no Streamlit Cloud e divirta-se! Qualquer ajuste (mais ferramentas, cores, etc.) é só pedir!")
