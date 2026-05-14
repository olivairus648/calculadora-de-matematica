import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd
from sympy import symbols, Eq, solve, diff, integrate, limit, sin, cos, tan, binomial, factorial

st.set_page_config(page_title="MathCloud - Matemática", layout="wide", page_icon="🧮")

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
    .step-box {
        background: rgba(199, 21, 133, 0.15) !important;
        border-left: 4px solid #C71585;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    .success { color: #90EE90; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

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

def mostrar_passo(numero, texto):
    st.markdown(f"""
    <div class="step-box">
        <strong>Passo {numero}:</strong> {texto}
    </div>
    """, unsafe_allow_html=True)

# ===================== INÍCIO =====================
if opcao == "Início":
    st.title("Bem-vindo a calculadora de matemática!")
    st.markdown("### App completo de Matemática")
    st.write("Escolha qualquer ferramenta no menu lateral.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ferramentas", "14")
    col2.metric("Gráficos", "✅")
    col3.metric("Interativo", "100%")
    st.caption("Feito em python, por Mateus! 🚀")

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
        fig.update_layout(title=f"Gráfico de f(x) = {f_str}", xaxis_title="x",
                         yaxis_title="f(x)", template="plotly_dark", height=550)
        st.plotly_chart(fig, use_container_width=True)
        st.success("✅ Gráfico gerado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {str(e)}")

# ===================== OUTRAS SEÇÕES =====================
else:
    st.title(opcao)

    # ===================== ÁLGEBRA BÁSICA =====================
    if opcao == "Álgebra Básica":
        expr = st.text_input("Digite a expressão:", "2*x**2 + 3*x - 5")
        try:
            res = sp.sympify(expr)
            val = st.number_input("Valor de x:", value=2.0)
            st.success(f"Resultado = **{res.subs(x, val)}**")
            st.latex(f"{sp.latex(res)}")
        except:
            st.error("Expressão inválida")

    # ===================== RESOLUÇÃO DE EQUAÇÕES =====================
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

    # ===================== DERIVADAS =====================
    elif opcao == "Derivadas":
        f = st.text_input("Função f(x):", "x**3 + 2*x**2 - 5*x")
        ordem = st.slider("Ordem da derivada", 1, 5, 1)
        try:
            deriv = diff(sp.sympify(f), x, ordem)
            st.latex(f"f^{{{ordem}}}(x) = {sp.latex(deriv)}")
        except:
            st.error("Função inválida")

    # ===================== INTEGRAIS =====================
    elif opcao == "Integrais":
        f = st.text_input("Função f(x):", "x**2 + 3*x")
        try:
            integral = integrate(sp.sympify(f), x)
            st.latex(f"\\int {sp.latex(sp.sympify(f))} dx = {sp.latex(integral)} + C")
        except:
            st.error("Função inválida")

    # ===================== SISTEMAS DE EQUAÇÕES =====================
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

    # ===================== MATRIZES E DETERMINANTES =====================
    elif opcao == "Matrizes e Determinantes":
        n = st.slider("Tamanho da matriz", 2, 4, 3)
        df = pd.DataFrame(np.zeros((n, n)))
        edited = st.data_editor(df, use_container_width=True)
        mat = sp.Matrix(edited.values)
        st.write(f"**Determinante** = {mat.det()}")
        if mat.det() != 0:
            st.latex(f"Inversa = {sp.latex(mat.inv())}")

    # ===================== TRIGONOMETRIA =====================
    elif opcao == "Trigonometria":
        st.markdown("### Escolha o modo de cálculo")
        modo = st.radio("O que você tem?", 
                        ["Tenho o ângulo → quero sen/cos/tan", 
                         "Tenho sen/cos/tan → quero o ângulo"],
                        horizontal=True)
        passo_a_passo = st.checkbox("Mostrar passo a passo")

        if modo == "Tenho o ângulo → quero sen/cos/tan":
            ang = st.number_input("Ângulo (graus)", value=30.0)

            if st.button("Calcular"):
                rad = np.deg2rad(ang)
                seno = np.sin(rad)
                cosseno = np.cos(rad)
                tangente = np.tan(rad)

                if passo_a_passo:
                    mostrar_passo(1, f"Converter o ângulo para radianos: {ang}° × (π/180) = <b>{rad:.6f} rad</b>")
                    mostrar_passo(2, f"Calcular seno: sen({ang}°) = <b>{seno:.4f}</b>")
                    mostrar_passo(3, f"Calcular cosseno: cos({ang}°) = <b>{cosseno:.4f}</b>")
                    mostrar_passo(4, f"Calcular tangente: tan = sen/cos = {seno:.4f} / {cosseno:.4f} = <b>{tangente:.4f}</b>")
                else:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("sen", f"{seno:.4f}")
                    col2.metric("cos", f"{cosseno:.4f}")
                    col3.metric("tan", f"{tangente:.4f}")

        else:
            razao_tipo = st.selectbox("Qual razão você tem?", ["seno", "cosseno", "tangente"])
            valor = st.number_input("Valor da razão (entre -1 e 1 para sen/cos):", value=0.5, format="%.4f")

            if st.button("Calcular"):
                try:
                    if razao_tipo == "seno":
                        rad = np.arcsin(valor)
                        nome_func = "arcsen"
                    elif razao_tipo == "cosseno":
                        rad = np.arccos(valor)
                        nome_func = "arccos"
                    else:
                        rad = np.arctan(valor)
                        nome_func = "arctan"

                    ang = np.rad2deg(rad)

                    if passo_a_passo:
                        mostrar_passo(1, f"Você tem {razao_tipo} = <b>{valor}</b>")
                        mostrar_passo(2, f"Aplicar a função inversa: {nome_func}({valor}) = <b>{rad:.6f} rad</b>")
                        mostrar_passo(3, f"Converter para graus: {rad:.6f} × (180/π) = <b>{ang:.4f}°</b>")
                    else:
                        st.success(f"Ângulo = **{ang:.4f}°** ({rad:.4f} rad)")
                except Exception as e:
                    st.error(f"Valor inválido: {str(e)}")

    # ===================== TEOREMA DE PITÁGORAS =====================
    elif opcao == "Teorema de Pitágoras":
        st.markdown("### Qual valor está faltando?")
        faltando = st.radio("Calcular:", 
                            ["Hipotenusa (c)", "Cateto a", "Cateto b"],
                            horizontal=True)
        passo_a_passo = st.checkbox("Mostrar passo a passo")

        if faltando == "Hipotenusa (c)":
            a = st.number_input("Cateto a", value=3.0, min_value=0.01)
            b = st.number_input("Cateto b", value=4.0, min_value=0.01)
            if st.button("Calcular"):
                c = np.sqrt(a**2 + b**2)
                if passo_a_passo:
                    mostrar_passo(1, "Fórmula do Teorema de Pitágoras: <b>c² = a² + b²</b>")
                    mostrar_passo(2, f"Substituir os valores: c² = {a}² + {b}²")
                    mostrar_passo(3, f"Calcular os quadrados: c² = {a**2} + {b**2}")
                    mostrar_passo(4, f"Somar: c² = {a**2 + b**2}")
                    mostrar_passo(5, f"Tirar a raiz quadrada: c = √{a**2 + b**2} = <b>{c:.4f}</b>")
                else:
                    st.success(f"Hipotenusa c = **{c:.4f}**")

        elif faltando == "Cateto a":
            c = st.number_input("Hipotenusa c", value=5.0, min_value=0.01)
            b = st.number_input("Cateto b", value=4.0, min_value=0.01)
            if st.button("Calcular"):
                if c <= b:
                    st.error("A hipotenusa deve ser maior que o cateto!")
                else:
                    a = np.sqrt(c**2 - b**2)
                    if passo_a_passo:
                        mostrar_passo(1, "Fórmula: <b>c² = a² + b²</b> → isolando a: <b>a² = c² - b²</b>")
                        mostrar_passo(2, f"Substituir: a² = {c}² - {b}²")
                        mostrar_passo(3, f"Calcular: a² = {c**2} - {b**2}")
                        mostrar_passo(4, f"Subtrair: a² = {c**2 - b**2}")
                        mostrar_passo(5, f"Raiz quadrada: a = √{c**2 - b**2} = <b>{a:.4f}</b>")
                    else:
                        st.success(f"Cateto a = **{a:.4f}**")

        else:
            c = st.number_input("Hipotenusa c", value=5.0, min_value=0.01)
            a = st.number_input("Cateto a", value=3.0, min_value=0.01)
            if st.button("Calcular"):
                if c <= a:
                    st.error("A hipotenusa deve ser maior que o cateto!")
                else:
                    b = np.sqrt(c**2 - a**2)
                    if passo_a_passo:
                        mostrar_passo(1, "Fórmula: <b>c² = a² + b²</b> → isolando b: <b>b² = c² - a²</b>")
                        mostrar_passo(2, f"Substituir: b² = {c}² - {a}²")
                        mostrar_passo(3, f"Calcular: b² = {c**2} - {a**2}")
                        mostrar_passo(4, f"Subtrair: b² = {c**2 - a**2}")
                        mostrar_passo(5, f"Raiz quadrada: b = √{c**2 - a**2} = <b>{b:.4f}</b>")
                    else:
                        st.success(f"Cateto b = **{b:.4f}**")

    # ===================== SEQUÊNCIAS E PROGRESSÕES =====================
    elif opcao == "Sequências e Progressões":
        tipo = st.selectbox("Tipo", ["PA - Progressão Aritmética", "PG - Progressão Geométrica"])
        passo_a_passo = st.checkbox("Mostrar passo a passo")

        if tipo.startswith("PA"):
            st.markdown("### O que você tem?")
            modo = st.radio("Modo:", 
                            ["Tenho a₁ e a razão → listar termos",
                             "Tenho a₁ e outro termo → achar a razão",
                             "Tenho a razão e um termo → achar a₁"],
                            horizontal=False)

            if modo == "Tenho a₁ e a razão → listar termos":
                a1 = st.number_input("Primeiro termo (a₁)", value=2.0)
                r = st.number_input("Razão (r)", value=3.0)
                n = st.number_input("Número de termos", 2, 20, 8)

                if st.button("Calcular"):
                    termos = [a1 + (k-1)*r for k in range(1, int(n)+1)]
                    soma = sum(termos)

                    if passo_a_passo:
                        mostrar_passo(1, f"Fórmula do termo geral: <b>aₙ = a₁ + (n-1) × r</b>")
                        mostrar_passo(2, f"Com a₁ = {a1} e r = {r}")
                        for i, t in enumerate(termos, 1):
                            mostrar_passo(i+2, f"a{i} = {a1} + ({i}-1) × {r} = {a1} + {(i-1)*r} = <b>{t}</b>")
                        mostrar_passo(len(termos)+3, f"Soma da PA: S = n × (a₁ + aₙ) / 2 = {n} × ({a1} + {termos[-1]}) / 2 = <b>{soma}</b>")
                    else:
                        st.write("Termos:", [round(t, 4) for t in termos])
                        st.write(f"**Soma = {soma:.4f}**")

            elif modo == "Tenho a₁ e outro termo → achar a razão":
                a1 = st.number_input("Primeiro termo (a₁)", value=2.0)
                n = st.number_input("Posição do outro termo (n)", 2, 50, 5)
                an = st.number_input(f"Valor do termo a{int(n)}", value=14.0)

                if st.button("Calcular"):
                    r = (an - a1) / (n - 1)
                    if passo_a_passo:
                        mostrar_passo(1, "Fórmula: <b>aₙ = a₁ + (n-1) × r</b>")
                        mostrar_passo(2, f"Isolar r: <b>r = (aₙ - a₁) / (n - 1)</b>")
                        mostrar_passo(3, f"Substituir: r = ({an} - {a1}) / ({n} - 1)")
                        mostrar_passo(4, f"Calcular: r = {an - a1} / {n - 1} = <b>{r:.4f}</b>")
                    else:
                        st.success(f"Razão r = **{r:.4f}**")

            else:
                r = st.number_input("Razão (r)", value=3.0)
                n = st.number_input("Posição do termo conhecido (n)", 2, 50, 4)
                an = st.number_input(f"Valor do termo a{int(n)}", value=11.0)

                if st.button("Calcular"):
                    a1 = an - (n - 1) * r
                    if passo_a_passo:
                        mostrar_passo(1, "Fórmula: <b>aₙ = a₁ + (n-1) × r</b>")
                        mostrar_passo(2, f"Isolar a₁: <b>a₁ = aₙ - (n-1) × r</b>")
                        mostrar_passo(3, f"Substituir: a₁ = {an} - ({n}-1) × {r}")
                        mostrar_passo(4, f"Calcular: a₁ = {an} - {(n-1)*r} = <b>{a1:.4f}</b>")
                    else:
                        st.success(f"Primeiro termo a₁ = **{a1:.4f}**")

        else:  # PG
            st.markdown("### O que você tem?")
            modo = st.radio("Modo:",
                            ["Tenho a₁ e a razão → listar termos",
                             "Tenho a₁ e outro termo → achar a razão",
                             "Tenho a razão e um termo → achar a₁"],
                            horizontal=False)

            if modo == "Tenho a₁ e a razão → listar termos":
                a1 = st.number_input("Primeiro termo (a₁)", value=2.0)
                r = st.number_input("Razão (q)", value=3.0)
                n = st.number_input("Número de termos", 2, 20, 6)

                if st.button("Calcular"):
                    termos = [a1 * (r ** (k-1)) for k in range(1, int(n)+1)]
                    if passo_a_passo:
                        mostrar_passo(1, "Fórmula do termo geral: <b>aₙ = a₁ × q^(n-1)</b>")
                        mostrar_passo(2, f"Com a₁ = {a1} e q = {r}")
                        for i, t in enumerate(termos, 1):
                            mostrar_passo(i+2, f"a{i} = {a1} × {r}^({i}-1) = {a1} × {r**(i-1)} = <b>{round(t,4)}</b>")
                    else:
                        st.write("Termos:", [round(t, 4) for t in termos])

            elif modo == "Tenho a₁ e outro termo → achar a razão":
                a1 = st.number_input("Primeiro termo (a₁)", value=2.0)
                n = st.number_input("Posição do outro termo (n)", 2, 20, 4)
                an = st.number_input(f"Valor do termo a{int(n)}", value=54.0)

                if st.button("Calcular"):
                    if a1 == 0:
                        st.error("a₁ não pode ser zero numa PG")
                    else:
                        q = (an / a1) ** (1 / (n - 1))
                        if passo_a_passo:
                            mostrar_passo(1, "Fórmula: <b>aₙ = a₁ × q^(n-1)</b>")
                            mostrar_passo(2, "Isolar q: <b>q = (aₙ / a₁)^(1/(n-1))</b>")
                            mostrar_passo(3, f"Substituir: q = ({an} / {a1})^(1/({n}-1))")
                            mostrar_passo(4, f"Calcular: q = {an/a1}^(1/{n-1}) = <b>{q:.4f}</b>")
                        else:
                            st.success(f"Razão q = **{q:.4f}**")

            else:
                r = st.number_input("Razão (q)", value=3.0)
                n = st.number_input("Posição do termo conhecido (n)", 2, 20, 4)
                an = st.number_input(f"Valor do termo a{int(n)}", value=54.0)

                if st.button("Calcular"):
                    if r == 0:
                        st.error("A razão não pode ser zero numa PG")
                    else:
                        a1 = an / (r ** (n - 1))
                        if passo_a_passo:
                            mostrar_passo(1, "Fórmula: <b>aₙ = a₁ × q^(n-1)</b>")
                            mostrar_passo(2, "Isolar a₁: <b>a₁ = aₙ / q^(n-1)</b>")
                            mostrar_passo(3, f"Substituir: a₁ = {an} / {r}^({n}-1)")
                            mostrar_passo(4, f"Calcular: a₁ = {an} / {r**(n-1)} = <b>{a1:.4f}</b>")
                        else:
                            st.success(f"Primeiro termo a₁ = **{a1:.4f}**")

    # ===================== COMBINATÓRIA =====================
    elif opcao == "Combinatória":
        n = st.number_input("n", 5, 20, 5)
        k = st.number_input("k", 0, n, 2)
        st.write(f"**Combinação** C({n},{k}) = {binomial(n,k)}")
        st.write(f"**Fatorial** {n}! = {factorial(n)}")

    # ===================== LIMITES =====================
    elif opcao == "Limites":
        f_str = st.text_input("f(x)", "sin(x)/x")
        ponto = st.number_input("x →", value=0.0)
        try:
            lim = limit(sp.sympify(f_str), x, ponto)
            st.latex(f"lim = {sp.latex(lim)}")
        except:
            st.error("Erro no limite")

    # ===================== ESTATÍSTICA BÁSICA =====================
    elif opcao == "Estatística Básica":
        dados = st.text_input("Números (separados por vírgula)", "2,4,4,5,5,7,9")
        try:
            nums = np.array([float(i) for i in dados.split(",")])
            st.write(f"Média = {np.mean(nums):.3f}")
            st.write(f"Desvio Padrão = {np.std(nums):.3f}")
        except:
            st.error("Digite números corretamente")

st.sidebar.caption("✅ Versão Completa e Funcionando - v2.0")
