import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd
from sympy import symbols, Eq, solve, diff, integrate, limit, sin, cos, tan, binomial, factorial

st.set_page_config(page_title="Calculadora de Mateus - Matemática", layout="wide", page_icon="🧮")

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

st.title("🧮 Matemática")
st.markdown("**Todas as ferramentas caprichadas** — organizadas, intuitivas e com gráficos quando possível!")

opcao = st.selectbox(
    "Escolha a ferramenta:",
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
    st.subheader("Bem-vindo ao MathCloud! 👋")
    st.write("Um app completo e bonito de Matemática com cálculos interativos, gráficos e explicações.")
    st.write("Escolha qualquer ferramenta no menu acima e divirta-se estudando!")
    st.caption("Feito com carinho por Grok para você, Mateus! 🚀")

# ===================== ÁLGEBRA BÁSICA =====================
elif opcao == "Álgebra Básica":
    st.subheader("🧩 Álgebra Básica")
    expr = st.text_input("Digite a expressão algébrica:", "2*x**2 + 3*x - 5")
    try:
        resultado = sp.sympify(expr)
        st.latex(f"Expressão simplificada: {sp.latex(resultado)}")
        valor = st.number_input("Substituir x por:", value=2.0, step=0.1)
        st.success(f"Resultado quando x = {valor} → **{resultado.subs(x, valor)}**")
    except:
        st.error("Expressão inválida. Use * para multiplicação e ** para potência.")

# ===================== RESOLUÇÃO DE EQUAÇÕES =====================
elif opcao == "Resolução de Equações":
    st.subheader("🔢 Resolução de Equações")
    eq = st.text_input("Digite a equação (ex: x**2 - 5*x + 6 = 0):", "x**2 - 5*x + 6 = 0")
    if st.button("Resolver"):
        try:
            lhs, rhs = [p.strip() for p in eq.split("=")]
            sol = solve(Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
            st.write("**Soluções encontradas:**")
            for s in sol:
                st.latex(sp.latex(s))
        except:
            st.error("Não foi possível resolver. Verifique a sintaxe.")

# ===================== FUNÇÕES E GRÁFICOS (já estava boa, mantive e refinei) =====================
elif opcao == "Funções e Gráficos":
    st.subheader("📈 Funções e Gráficos Interativos")
    tipo = st.radio("Tipo de função:", 
        ["Linear (1º grau)", "Quadrática (2º grau)", "Cúbica (3º grau)", 
         "Trigonométrica", "Exponencial", "Personalizada"], horizontal=True)
    
    xmin, xmax = st.slider("Intervalo de x:", -10, 10, (-5, 5))
    x_vals = np.linspace(xmin, xmax, 600)
    
    if tipo == "Linear (1º grau)":
        a = st.number_input("Coeficiente angular a:", value=2.0)
        b = st.number_input("Coeficiente linear b:", value=-3.0)
        func = a*x + b
        f_str = f"{a}x + {b}"
    elif tipo == "Quadrática (2º grau)":
        a = st.number_input("a (x²):", value=1.0)
        b = st.number_input("b (x):", value=-4.0)
        c = st.number_input("c:", value=3.0)
        func = a*x**2 + b*x + c
        f_str = f"{a}x² + {b}x + {c}"
    elif tipo == "Cúbica (3º grau)":
        a = st.number_input("a (x³):", value=1.0)
        b = st.number_input("b (x²):", value=0.0)
        c = st.number_input("c (x):", value=-2.0)
        d = st.number_input("d:", value=1.0)
        func = a*x**3 + b*x**2 + c*x + d
        f_str = f"{a}x³ + {b}x² + {c}x + {d}"
    elif tipo == "Trigonométrica":
        trig = st.selectbox("Escolha:", ["sen(x)", "cos(x)", "tan(x)"])
        func = sin(x) if trig == "sen(x)" else cos(x) if trig == "cos(x)" else tan(x)
        f_str = trig
    elif tipo == "Exponencial":
        base = st.number_input("Base a:", value=2.0)
        func = base**x
        f_str = f"{base}^x"
    else:
        f_str = st.text_input("Digite f(x):", "x**2 - 4*x + 3")
        func = sp.sympify(f_str)
    
    f_num = sp.lambdify(x, func, 'numpy')
    y_vals = f_num(x_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f_str,
                             line=dict(color='#C71585', width=5)))
    fig.update_layout(title=f"Gráfico de f(x) = {f_str}", xaxis_title="x", yaxis_title="f(x)",
                      template="plotly_dark", height=520)
    st.plotly_chart(fig, use_container_width=True)
    
    st.latex(f"f(x) = {sp.latex(func)}")

# ===================== DERIVADAS =====================
elif opcao == "Derivadas":
    st.subheader("📐 Cálculo de Derivadas")
    f = st.text_input("Função f(x):", "x**3 + 2*x**2 - 5*x + 1")
    ordem = st.slider("Ordem da derivada:", 1, 5, 1)
    func = sp.sympify(f)
    deriv = diff(func, x, ordem)
    st.latex(f"f^{{{ordem}}}(x) = {sp.latex(deriv)}")

# ===================== INTEGRAIS =====================
elif opcao == "Integrais":
    st.subheader("📏 Cálculo de Integrais")
    f = st.text_input("Função f(x):", "x**2 + 3*x + 2")
    func = sp.sympify(f)
    integral_indef = integrate(func, x)
    st.latex(f"\\int {sp.latex(func)}\\, dx = {sp.latex(integral_indef)} + C")

# ===================== SISTEMAS DE EQUAÇÕES =====================
elif opcao == "Sistemas de Equações":
    st.subheader("🔄 Sistemas de Equações Lineares")
    tamanho = st.radio("Tamanho do sistema:", ["2 variáveis (2x2)", "3 variáveis (3x3)"])
    if tamanho == "2 variáveis (2x2)":
        col1, col2, col3 = st.columns(3)
        a = col1.number_input("a", value=2.0)
        b = col2.number_input("b", value=3.0)
        c = col3.number_input("c", value=8.0)
        d = col1.number_input("d", value=4.0)
        e = col2.number_input("e", value=-1.0)
        f_val = col3.number_input("f", value=7.0)
        
        mat = sp.Matrix([[a, b], [d, e]])
        const = sp.Matrix([c, f_val])
        try:
            sol = mat.solve(const)
            st.success(f"**Solução:** x = {sol[0]:.4f}   |   y = {sol[1]:.4f}")
        except:
            st.error("Sistema sem solução única ou inconsistente.")

# ===================== MATRIZES =====================
elif opcao == "Matrizes e Determinantes":
    st.subheader("🔢 Matrizes e Determinantes")
    n = st.slider("Tamanho da matriz (n × n):", 2, 4, 3)
    st.write("Edite os valores da matriz:")
    df = pd.DataFrame(np.zeros((n, n)), columns=[f"Col {i+1}" for i in range(n)])
    edited = st.data_editor(df, use_container_width=True)
    mat = sp.Matrix(edited.values)
    st.latex(f"Matriz inserida: {sp.latex(mat)}")
    st.write(f"**Determinante** = **{mat.det()}**")
    if mat.det() != 0:
        st.latex(f"**Inversa:** {sp.latex(mat.inv())}")

# ===================== TRIGONOMETRIA =====================
elif opcao == "Trigonometria":
    st.subheader("📐 Trigonometria")
    ang_graus = st.number_input("Ângulo em graus:", value=30.0, step=1.0)
    ang_rad = np.deg2rad(ang_graus)
    col1, col2, col3 = st.columns(3)
    col1.metric("sen", f"{np.sin(ang_rad):.6f}")
    col2.metric("cos", f"{np.cos(ang_rad):.6f}")
    col3.metric("tan", f"{np.tan(ang_rad):.6f}")

# ===================== TEOREMA DE PITÁGORAS =====================
elif opcao == "Teorema de Pitágoras":
    st.subheader("📏 Teorema de Pitágoras")
    a = st.number_input("Cateto a:", value=3.0)
    b = st.number_input("Cateto b:", value=4.0)
    c = np.sqrt(a**2 + b**2)
    st.success(f"**Hipotenusa c = {c:.4f}**")
    st.latex(f"c = \\sqrt{{{a}^2 + {b}^2}} = {c:.4f}")

# ===================== SEQUÊNCIAS =====================
elif opcao == "Sequências e Progressões":
    st.subheader("📈 Sequências e Progressões")
    tipo = st.selectbox("Tipo de progressão:", ["Progressão Aritmética (PA)", "Progressão Geométrica (PG)"])
    a1 = st.number_input("Primeiro termo (a1):", value=2.0)
    n = st.number_input("Número de termos:", 2, 20, 10)
    
    if tipo == "Progressão Aritmética (PA)":
        r = st.number_input("Razão comum (r):", value=3.0)
        termos = [a1 + (k-1)*r for k in range(1, n+1)]
        soma = sum(termos)
    else:
        q = st.number_input("Razão comum (q):", value=2.0)
        termos = [a1 * (q ** (k-1)) for k in range(1, n+1)]
        soma = sum(termos)
    
    st.write("**Termos:**", [round(t, 4) for t in termos])
    st.success(f"**Soma dos termos = {soma:.4f}**")

# ===================== COMBINATÓRIA =====================
elif opcao == "Combinatória":
    st.subheader("🎲 Combinatória")
    n = st.number_input("n (elementos totais):", 1, 30, 5)
    k = st.number_input("k (escolher):", 0, n, 2)
    st.write(f"**Combinação** C({n}, {k}) = **{binomial(n, k)}**")
    st.write(f"**Arranjo** A({n}, {k}) = **{factorial(n) / factorial(n-k)}**")
    st.write(f"**Fatorial** {n}! = **{factorial(n)}**")

# ===================== LIMITES =====================
elif opcao == "Limites":
    st.subheader("→ Limites")
    f_str = st.text_input("Função f(x):", "sin(x)/x")
    ponto = st.number_input("x tendendo a:", value=0.0, step=0.1)
    try:
        lim = limit(sp.sympify(f_str), x, ponto)
        st.latex(f"\\lim_{{x \\to {ponto}}} {sp.latex(sp.sympify(f_str))} = {sp.latex(lim)}")
    except:
        st.error("Não foi possível calcular o limite.")

# ===================== ESTATÍSTICA =====================
elif opcao == "Estatística Básica":
    st.subheader("📊 Estatística Básica")
    dados_str = st.text_input("Digite os números separados por vírgula:", "2, 4, 4, 5, 5, 7, 9, 10")
    try:
        dados = np.array([float(i.strip()) for i in dados_str.split(',')])
        st.write(f"**Quantidade de dados:** {len(dados)}")
        st.write(f"**Média:** {np.mean(dados):.4f}")
        st.write(f"**Mediana:** {np.median(dados):.4f}")
        st.write(f"**Desvio Padrão:** {np.std(dados, ddof=1):.4f}")
        
        fig = go.Figure(data=go.Box(y=dados, boxpoints="all", jitter=0.3))
        fig.update_layout(template="plotly_dark", title="Boxplot dos dados")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Insira números válidos separados por vírgula.")

st.caption("✅Mateus Agostinho, feito com Streamlit! ")
