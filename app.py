import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="MathCloud - Matemática", layout="wide", page_icon="🧮")

# CSS mais leve e compatível com Streamlit Cloud
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #2C003E, #6A1B9A); }
    div[data-testid="stVerticalBlock"] > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255,255,255,0.15);
    }
    h1, h2, h3 { color: #E0B0FF !important; }
    .stButton>button { background: #C71585; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🧮 Calculadora de Mateus - Matemática")
st.markdown("**App completo de Matemática** — limpo, rápido e com muitas ferramentas novas!")

opcao = st.selectbox(
    "Escolha a ferramenta de Matemática:",
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
        "Combinatória e Probabilidade",
        "Limites",
        "Estatística"
    ]
)

# ===================== INÍCIO =====================
if opcao == "Início":
    st.subheader("Bem-vindo ao MathCloud! 👋")
    st.write("Aqui você encontra várias ferramentas de matemática com cálculos interativos, gráficos e equações resolvidas na hora.")
    st.caption("Feito especialmente para você, Mateus! Qualquer coisa é só pedir mais ferramentas.")

# ===================== ÁLGEBRA BÁSICA =====================
elif opcao == "Álgebra Básica":
    st.subheader("🧩 Álgebra Básica")
    expr = st.text_input("Digite uma expressão (ex: 2*x**2 + 3*x - 5)", "x**2 + 3*x - 4")
    x = sp.symbols('x')
    try:
        resultado = sp.sympify(expr)
        st.latex(f"Expressão: {sp.latex(resultado)}")
        valor_x = st.number_input("Valor de x:", value=2.0)
        st.success(f"Resultado = {resultado.subs(x, valor_x)}")
    except:
        st.error("Expressão inválida")

# ===================== RESOLUÇÃO DE EQUAÇÕES =====================
elif opcao == "Resolução de Equações":
    st.subheader("🔢 Resolução de Equações")
    eq = st.text_input("Digite a equação (ex: x**2 - 5*x + 6 = 0)", "x**2 - 5*x + 6 = 0")
    if st.button("Resolver Equação"):
        try:
            x = sp.symbols('x')
            lhs, rhs = [part.strip() for part in eq.split('=')]
            solucao = sp.solve(sp.Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
            st.write("**Soluções:**")
            for s in solucao:
                st.latex(sp.latex(s))
        except:
            st.error("Não consegui resolver. Verifique a sintaxe.")

# ===================== FUNÇÕES E GRÁFICOS (melhorada) =====================
elif opcao == "Funções e Gráficos":
    st.subheader("📈 Funções e Gráficos")
    
    tipo_funcao = st.radio("Tipo de função:", 
        ["Linear (1º grau)", "Quadrática (2º grau)", "Cúbica (3º grau)", 
         "Trigonométrica", "Exponencial", "Personalizada"])
    
    xmin, xmax = st.slider("Intervalo de x", -10, 10, (-5, 5))
    x = sp.symbols('x')
    x_vals = np.linspace(xmin, xmax, 500)
    
    if tipo_funcao == "Linear (1º grau)":
        a = st.number_input("Coeficiente angular (a)", value=2.0)
        b = st.number_input("Coeficiente linear (b)", value=-3.0)
        func = a*x + b
        f_str = f"{a}x + {b}"
    elif tipo_funcao == "Quadrática (2º grau)":
        a = st.number_input("a (x²)", value=1.0)
        b = st.number_input("b (x)", value=-4.0)
        c = st.number_input("c (constante)", value=3.0)
        func = a*x**2 + b*x + c
        f_str = f"{a}x² + {b}x + {c}"
    elif tipo_funcao == "Cúbica (3º grau)":
        a = st.number_input("a (x³)", value=1.0)
        b = st.number_input("b (x²)", value=0.0)
        c = st.number_input("c (x)", value=-3.0)
        d = st.number_input("d (constante)", value=2.0)
        func = a*x**3 + b*x**2 + c*x + d
        f_str = f"{a}x³ + {b}x² + {c}x + {d}"
    elif tipo_funcao == "Trigonométrica":
        tipo_trig = st.selectbox("Função trigonométrica", ["sen(x)", "cos(x)", "tan(x)"])
        func = sp.sin(x) if tipo_trig == "sen(x)" else sp.cos(x) if tipo_trig == "cos(x)" else sp.tan(x)
        f_str = tipo_trig
    elif tipo_funcao == "Exponencial":
        a = st.number_input("Base (a)", value=2.0)
        func = a**x
        f_str = f"{a}^x"
    else:  # Personalizada
        f_str = st.text_input("Digite a função f(x) =", "x**2 - 4*x + 3")
        func = sp.sympify(f_str)
    
    f_num = sp.lambdify(x, func, 'numpy')
    y_vals = f_num(x_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', 
                            name=f_str, line=dict(color='#C71585', width=4)))
    fig.update_layout(title=f"Gráfico de {f_str}", xaxis_title="x", yaxis_title="f(x)", 
                      template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.latex(f"f(x) = {sp.latex(func)}")

# ===================== DERIVADAS =====================
elif opcao == "Derivadas":
    st.subheader("📐 Derivadas")
    f = st.text_input("Função f(x) =", "x**3 + 2*x**2 - 5*x")
    ordem = st.number_input("Ordem da derivada", 1, 5, 1)
    x = sp.symbols('x')
    func = sp.sympify(f)
    deriv = sp.diff(func, x, ordem)
    st.latex(f"f^{{{ordem}}}(x) = {sp.latex(deriv)}")

# ===================== INTEGRAIS =====================
elif opcao == "Integrais":
    st.subheader("📏 Integrais")
    f = st.text_input("Função f(x) =", "x**2 + 3*x")
    x = sp.symbols('x')
    func = sp.sympify(f)
    integral = sp.integrate(func, x)
    st.latex(f"\\int {sp.latex(func)} \\, dx = {sp.latex(integral)} + C")

# ===================== SISTEMAS DE EQUAÇÕES (nova) =====================
elif opcao == "Sistemas de Equações":
    st.subheader("🔄 Sistemas de Equações")
    tamanho = st.radio("Número de variáveis", ["2x2", "3x3"])
    if tamanho == "2x2":
        st.write("ax + by = c")
        st.write("dx + ey = f")
        a,b,c = st.columns(3)
        a1 = a.number_input("a", value=2.0)
        b1 = b.number_input("b", value=3.0)
        c1 = c.number_input("c", value=8.0)
        d1 = a.number_input("d", value=4.0)
        e1 = b.number_input("e", value=-1.0)
        f1 = c.number_input("f", value=7.0)
        mat = sp.Matrix([[a1, b1], [d1, e1]])
        const = sp.Matrix([c1, f1])
        try:
            sol = mat.solve(const)
            st.success(f"x = {sol[0]}, y = {sol[1]}")
        except:
            st.error("Sistema sem solução única")
    # (posso expandir para 3x3 se quiser)

# ===================== MATRIZES =====================
elif opcao == "Matrizes e Determinantes":
    st.subheader("🔢 Matrizes")
    n = st.slider("Tamanho da matriz", 2, 4, 2)
    df = pd.DataFrame(np.zeros((n, n)), columns=[f"Col{i+1}" for i in range(n)])
    edited = st.data_editor(df)
    mat = sp.Matrix(edited.values)
    st.latex(f"Matriz = {sp.latex(mat)}")
    st.write(f"**Determinante** = {mat.det()}")
    if mat.det() != 0:
        st.latex(f"Inversa = {sp.latex(mat.inv())}")

# ===================== TRIGONOMETRIA =====================
elif opcao == "Trigonometria":
    st.subheader("📐 Trigonometria")
    ang = st.number_input("Ângulo em graus", value=30.0)
    rad = np.deg2rad(ang)
    st.write(f"**sen({ang}°) =** {np.sin(rad):.4f}")
    st.write(f"**cos({ang}°) =** {np.cos(rad):.4f}")
    st.write(f"**tan({ang}°) =** {np.tan(rad):.4f}")

# ===================== TEOREMA DE PITÁGORAS (nova) =====================
elif opcao == "Teorema de Pitágoras":
    st.subheader("📏 Teorema de Pitágoras")
    lado1 = st.number_input("Cateto a", value=3.0)
    lado2 = st.number_input("Cateto b", value=4.0)
    hip = np.sqrt(lado1**2 + lado2**2)
    st.success(f"Hipotenusa = {hip:.3f}")
    st.latex(f"c = \\sqrt{{{lado1}^2 + {lado2}^2}} = {hip:.3f}")

# ===================== SEQUÊNCIAS (nova) =====================
elif opcao == "Sequências e Progressões":
    st.subheader("📈 Sequências")
    tipo = st.selectbox("Tipo", ["Progressão Aritmética (PA)", "Progressão Geométrica (PG)"])
    if tipo == "Progressão Aritmética (PA)":
        a1 = st.number_input("Primeiro termo", value=2.0)
        r = st.number_input("Razão", value=3.0)
        n = st.number_input("Número de termos", 1, 20, 10)
        termos = [a1 + (k-1)*r for k in range(1, n+1)]
        st.write("Termos:", termos)
        st.write(f"Soma = {sum(termos)}")
    else:
        a1 = st.number_input("Primeiro termo", value=2.0)
        q = st.number_input("Razão", value=2.0)
        n = st.number_input("Número de termos", 1, 15, 8)
        termos = [a1 * (q**(k-1)) for k in range(1, n+1)]
        st.write("Termos:", [round(t,4) for t in termos])

# ===================== COMBINATÓRIA (nova) =====================
elif opcao == "Combinatória e Probabilidade":
    st.subheader("🎲 Combinatória")
    n = st.number_input("n (total)", 1, 20, 5)
    k = st.number_input("k (escolher)", 0, n, 2)
    st.write(f"**Combinação** C({n},{k}) = {sp.binomial(n,k)}")
    st.write(f"**Arranjo** A({n},{k}) = {sp.factorial(n)/sp.factorial(n-k)}")
    st.write(f"**Fatorial** {n}! = {sp.factorial(n)}")

# ===================== LIMITES (nova) =====================
elif opcao == "Limites":
    st.subheader("→ Limites")
    f = st.text_input("Função f(x) =", "x**2 / (x-1)")
    ponto = st.number_input("x tendendo a", value=2.0)
    x = sp.symbols('x')
    try:
        lim = sp.limit(sp.sympify(f), x, ponto)
        st.latex(f"\\lim_{{x \\to {ponto}}} {sp.latex(sp.sympify(f))} = {sp.latex(lim)}")
    except:
        st.error("Não foi possível calcular o limite")

# ===================== ESTATÍSTICA =====================
elif opcao == "Estatística":
    st.subheader("📊 Estatística Básica")
    dados = st.text_input("Números separados por vírgula", "2, 4, 4, 4, 5, 5, 7, 9")
    try:
        nums = np.array([float(x.strip()) for x in dados.split(',')])
        st.write(f"**Média** = {np.mean(nums):.3f}")
        st.write(f"**Mediana** = {np.median(nums):.3f}")
        st.write(f"**Desvio padrão** = {np.std(nums):.3f}")
        fig = go.Figure(data=go.Box(y=nums))
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Insira números válidos separados por vírgula")

st.caption("✅ Feito por Mateus Agostinho, utilizando o Streamlit!!")
