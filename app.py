import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import pandas as pd
from sympy import symbols, Eq, solve, diff, integrate, limit, sin, cos, tan, binomial, factorial

st.set_page_config(page_title="MathCloud", layout="wide", page_icon="🧮")

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

# ===================== TRADUÇÕES =====================
TRADUCOES = {
    "pt": {
        "menu_title": "Escolha uma ferramenta:",
        "tools": [
            "Início", "Álgebra Básica", "Resolução de Equações", "Funções e Gráficos",
            "Derivadas", "Integrais", "Sistemas de Equações", "Matrizes e Determinantes",
            "Trigonometria", "Teorema de Pitágoras", "Sequências e Progressões",
            "Combinatória", "Limites", "Estatística Básica"
        ],
        "home_title": "Bem-vindo à calculadora de matemática!",
        "home_sub": "### App completo de Matemática",
        "home_desc": "Escolha qualquer ferramenta no menu lateral.",
        "home_tools": "Ferramentas", "home_graphs": "Gráficos", "home_inter": "Interativo",
        "home_caption": "Feito em Python, por Mateus! 🚀",
        "step": "Passo", "calculate": "Calcular", "show_steps": "Mostrar passo a passo",
        "invalid_expr": "Expressão inválida", "invalid_func": "Função inválida",
        "solve_btn": "Resolver", "solutions": "**Soluções:**", "no_solution": "Não consegui resolver",
        "deriv_order": "Ordem da derivada",
        "graph_success": "✅ Gráfico gerado com sucesso!", "graph_error": "Erro ao gerar gráfico",
        "graph_interval": "Intervalo de x:", "func_type": "Tipo de função:",
        "func_types": ["Linear (1º grau)", "Quadrática (2º grau)", "Cúbica (3º grau)", "Trigonométrica", "Exponencial", "Personalizada"],
        "choose": "Escolha", "custom_fx": "f(x) =",
        "sys_title": "Sistema 2x2", "no_unique": "Sistema sem solução única",
        "mat_size": "Tamanho da matriz", "determinant": "**Determinante**", "inverse": "Inversa",
        "angle_deg": "Ângulo (graus)",
        "have_angle": "Tenho o ângulo → quero sen/cos/tan",
        "have_ratio": "Tenho sen/cos/tan → quero o ângulo",
        "what_have": "O que você tem?", "ratio_type": "Qual razão você tem?",
        "ratio_val": "Valor da razão (entre -1 e 1 para sen/cos):", "invalid_val": "Valor inválido",
        "trig_options": ["seno", "cosseno", "tangente"],
        "trig_inv_names": {"seno": ("arcsen", np.arcsin), "cosseno": ("arccos", np.arccos), "tangente": ("arctan", np.arctan)},
        "sin_label": "sen",
        "calc_hyp": "Hipotenusa (c)", "calc_a": "Cateto a", "calc_b": "Cateto b",
        "what_missing": "### Qual valor está faltando?", "calc_label": "Calcular:",
        "hyp_greater": "A hipotenusa deve ser maior que o cateto!",
        "result_hyp": "Hipotenusa c", "result_a": "Cateto a", "result_b": "Cateto b",
        "seq_type": ["PA - Progressão Aritmética", "PG - Progressão Geométrica"],
        "pa_mode1": "Tenho a₁ e a razão → listar termos",
        "pa_mode2": "Tenho a₁ e outro termo → achar a razão",
        "pa_mode3": "Tenho a razão e um termo → achar a₁",
        "pg_mode1": "Tenho a₁ e a razão → listar termos",
        "pg_mode2": "Tenho a₁ e outro termo → achar a razão",
        "pg_mode3": "Tenho a razão e um termo → achar a₁",
        "first_term": "Primeiro termo (a₁)", "ratio_r": "Razão (r)", "ratio_q": "Razão (q)",
        "num_terms": "Número de termos", "term_pos": "Posição do outro termo (n)",
        "known_pos": "Posição do termo conhecido (n)",
        "terms_label": "Termos:", "sum_label": "Soma",
        "ratio_result": "Razão r", "ratio_q_result": "Razão q",
        "a1_zero": "a₁ não pode ser zero numa PG", "q_zero": "A razão não pode ser zero numa PG",
        "mode_label": "Modo:",
        "comb_combo": "**Combinação**", "comb_fact": "**Fatorial**",
        "limit_input": "f(x)", "limit_point": "x →", "limit_error": "Erro no limite",
        "stat_input": "Números (separados por vírgula)",
        "stat_mean": "Média", "stat_std": "Desvio Padrão", "stat_error": "Digite números corretamente",
        "x_value": "Valor de x:", "result": "Resultado",
        "equation_input": "Digite a equação:", "expr_input": "Digite a expressão:", "func_input": "Função f(x):",
        "version": "✅ Versão Completa - v2.0",
        "pit_step1_hyp": "Fórmula do Teorema de Pitágoras: <b>c² = a² + b²</b>",
        "pit_step2_hyp": "Substituir os valores: c² = {a}² + {b}²",
        "pit_step3_hyp": "Calcular os quadrados: c² = {a2} + {b2}",
        "pit_step4_hyp": "Somar: c² = {ab2}",
        "pit_step5_hyp": "Tirar a raiz quadrada: c = √{ab2} = <b>{c:.4f}</b>",
        "pit_step1_cat": "Fórmula: <b>c² = a² + b²</b> → isolando {v}: <b>{v}² = c² - {u}²</b>",
        "pit_step2_cat": "Substituir: {v}² = {c}² - {u}²",
        "pit_step3_cat": "Calcular: {v}² = {c2} - {u2}",
        "pit_step4_cat": "Subtrair: {v}² = {diff}",
        "pit_step5_cat": "Raiz quadrada: {v} = √{diff} = <b>{res:.4f}</b>",
        "trig_step1_ang": "Converter o ângulo para radianos: {ang}° × (π/180) = <b>{rad:.6f} rad</b>",
        "trig_step2_ang": "Calcular seno: sen({ang}°) = <b>{seno:.4f}</b>",
        "trig_step3_ang": "Calcular cosseno: cos({ang}°) = <b>{cos:.4f}</b>",
        "trig_step4_ang": "Calcular tangente: tan = sen/cos = {seno:.4f} / {cos:.4f} = <b>{tan:.4f}</b>",
        "trig_step1_inv": "Você tem {tipo} = <b>{val}</b>",
        "trig_step2_inv": "Aplicar a função inversa: {func}({val}) = <b>{rad:.6f} rad</b>",
        "trig_step3_inv": "Converter para graus: {rad:.6f} × (180/π) = <b>{ang:.4f}°</b>",
        "trig_result": "Ângulo = **{ang:.4f}°** ({rad:.4f} rad)",
        "pa_formula": "Fórmula do termo geral: <b>aₙ = a₁ + (n-1) × r</b>",
        "pa_with": "Com a₁ = {a1} e r = {r}",
        "pa_term": "a{i} = {a1} + ({i}-1) × {r} = {a1} + {delta} = <b>{t}</b>",
        "pa_sum": "Soma da PA: S = n × (a₁ + aₙ) / 2 = {n} × ({a1} + {last}) / 2 = <b>{soma}</b>",
        "pa_isolate_r": "Isolar r: <b>r = (aₙ - a₁) / (n - 1)</b>",
        "pa_sub_r": "Substituir: r = ({an} - {a1}) / ({n} - 1)",
        "pa_calc_r": "Calcular: r = {num} / {den} = <b>{r:.4f}</b>",
        "pa_isolate_a1": "Isolar a₁: <b>a₁ = aₙ - (n-1) × r</b>",
        "pa_sub_a1": "Substituir: a₁ = {an} - ({n}-1) × {r}",
        "pa_calc_a1": "Calcular: a₁ = {an} - {delta} = <b>{a1:.4f}</b>",
        "pg_formula": "Fórmula do termo geral: <b>aₙ = a₁ × q^(n-1)</b>",
        "pg_with": "Com a₁ = {a1} e q = {q}",
        "pg_term": "a{i} = {a1} × {q}^({i}-1) = {a1} × {qi} = <b>{t}</b>",
        "pg_isolate_q": "Isolar q: <b>q = (aₙ / a₁)^(1/(n-1))</b>",
        "pg_sub_q": "Substituir: q = ({an} / {a1})^(1/({n}-1))",
        "pg_calc_q": "Calcular: q = {ratio}^(1/{exp}) = <b>{q:.4f}</b>",
        "pg_isolate_a1": "Isolar a₁: <b>a₁ = aₙ / q^(n-1)</b>",
        "pg_sub_a1": "Substituir: a₁ = {an} / {q}^({n}-1)",
        "pg_calc_a1": "Calcular: a₁ = {an} / {denom} = <b>{a1:.4f}</b>",
    },
    "en": {
        "menu_title": "Choose a tool:",
        "tools": [
            "Home", "Basic Algebra", "Equation Solver", "Functions & Graphs",
            "Derivatives", "Integrals", "Systems of Equations", "Matrices & Determinants",
            "Trigonometry", "Pythagorean Theorem", "Sequences & Progressions",
            "Combinatorics", "Limits", "Basic Statistics"
        ],
        "home_title": "Welcome to the Math Calculator!",
        "home_sub": "### Complete Math App",
        "home_desc": "Choose any tool from the sidebar.",
        "home_tools": "Tools", "home_graphs": "Graphs", "home_inter": "Interactive",
        "home_caption": "Built in Python, by Mateus! 🚀",
        "step": "Step", "calculate": "Calculate", "show_steps": "Show step by step",
        "invalid_expr": "Invalid expression", "invalid_func": "Invalid function",
        "solve_btn": "Solve", "solutions": "**Solutions:**", "no_solution": "Couldn't solve it",
        "deriv_order": "Derivative order",
        "graph_success": "✅ Graph generated successfully!", "graph_error": "Error generating graph",
        "graph_interval": "x interval:", "func_type": "Function type:",
        "func_types": ["Linear (1st degree)", "Quadratic (2nd degree)", "Cubic (3rd degree)", "Trigonometric", "Exponential", "Custom"],
        "choose": "Choose", "custom_fx": "f(x) =",
        "sys_title": "2x2 System", "no_unique": "System has no unique solution",
        "mat_size": "Matrix size", "determinant": "**Determinant**", "inverse": "Inverse",
        "angle_deg": "Angle (degrees)",
        "have_angle": "I have the angle → get sin/cos/tan",
        "have_ratio": "I have sin/cos/tan → get the angle",
        "what_have": "What do you have?", "ratio_type": "Which ratio do you have?",
        "ratio_val": "Ratio value (between -1 and 1 for sin/cos):", "invalid_val": "Invalid value",
        "trig_options": ["sine", "cosine", "tangent"],
        "trig_inv_names": {"sine": ("arcsin", np.arcsin), "cosine": ("arccos", np.arccos), "tangent": ("arctan", np.arctan)},
        "sin_label": "sin",
        "calc_hyp": "Hypotenuse (c)", "calc_a": "Leg a", "calc_b": "Leg b",
        "what_missing": "### Which value is missing?", "calc_label": "Calculate:",
        "hyp_greater": "The hypotenuse must be greater than the leg!",
        "result_hyp": "Hypotenuse c", "result_a": "Leg a", "result_b": "Leg b",
        "seq_type": ["AP - Arithmetic Progression", "GP - Geometric Progression"],
        "pa_mode1": "I have a₁ and ratio → list terms",
        "pa_mode2": "I have a₁ and another term → find ratio",
        "pa_mode3": "I have ratio and a term → find a₁",
        "pg_mode1": "I have a₁ and ratio → list terms",
        "pg_mode2": "I have a₁ and another term → find ratio",
        "pg_mode3": "I have ratio and a term → find a₁",
        "first_term": "First term (a₁)", "ratio_r": "Common difference (d)", "ratio_q": "Common ratio (r)",
        "num_terms": "Number of terms", "term_pos": "Position of the other term (n)",
        "known_pos": "Position of the known term (n)",
        "terms_label": "Terms:", "sum_label": "Sum",
        "ratio_result": "Common difference d", "ratio_q_result": "Common ratio r",
        "a1_zero": "a₁ cannot be zero in a GP", "q_zero": "The ratio cannot be zero in a GP",
        "mode_label": "Mode:",
        "comb_combo": "**Combination**", "comb_fact": "**Factorial**",
        "limit_input": "f(x)", "limit_point": "x →", "limit_error": "Error computing limit",
        "stat_input": "Numbers (comma separated)",
        "stat_mean": "Mean", "stat_std": "Standard Deviation", "stat_error": "Enter numbers correctly",
        "x_value": "Value of x:", "result": "Result",
        "equation_input": "Enter the equation:", "expr_input": "Enter the expression:", "func_input": "Function f(x):",
        "version": "✅ Full Version - v2.0",
        "pit_step1_hyp": "Pythagorean Theorem: <b>c² = a² + b²</b>",
        "pit_step2_hyp": "Substitute: c² = {a}² + {b}²",
        "pit_step3_hyp": "Compute squares: c² = {a2} + {b2}",
        "pit_step4_hyp": "Add: c² = {ab2}",
        "pit_step5_hyp": "Square root: c = √{ab2} = <b>{c:.4f}</b>",
        "pit_step1_cat": "Formula: <b>c² = a² + b²</b> → solving for {v}: <b>{v}² = c² - {u}²</b>",
        "pit_step2_cat": "Substitute: {v}² = {c}² - {u}²",
        "pit_step3_cat": "Compute: {v}² = {c2} - {u2}",
        "pit_step4_cat": "Subtract: {v}² = {diff}",
        "pit_step5_cat": "Square root: {v} = √{diff} = <b>{res:.4f}</b>",
        "trig_step1_ang": "Convert to radians: {ang}° × (π/180) = <b>{rad:.6f} rad</b>",
        "trig_step2_ang": "Compute sine: sin({ang}°) = <b>{seno:.4f}</b>",
        "trig_step3_ang": "Compute cosine: cos({ang}°) = <b>{cos:.4f}</b>",
        "trig_step4_ang": "Compute tangent: tan = sin/cos = {seno:.4f} / {cos:.4f} = <b>{tan:.4f}</b>",
        "trig_step1_inv": "You have {tipo} = <b>{val}</b>",
        "trig_step2_inv": "Apply inverse: {func}({val}) = <b>{rad:.6f} rad</b>",
        "trig_step3_inv": "Convert to degrees: {rad:.6f} × (180/π) = <b>{ang:.4f}°</b>",
        "trig_result": "Angle = **{ang:.4f}°** ({rad:.4f} rad)",
        "pa_formula": "General term: <b>aₙ = a₁ + (n-1) × d</b>",
        "pa_with": "With a₁ = {a1} and d = {r}",
        "pa_term": "a{i} = {a1} + ({i}-1) × {r} = {a1} + {delta} = <b>{t}</b>",
        "pa_sum": "AP sum: S = n × (a₁ + aₙ) / 2 = {n} × ({a1} + {last}) / 2 = <b>{soma}</b>",
        "pa_isolate_r": "Isolate d: <b>d = (aₙ - a₁) / (n - 1)</b>",
        "pa_sub_r": "Substitute: d = ({an} - {a1}) / ({n} - 1)",
        "pa_calc_r": "Calculate: d = {num} / {den} = <b>{r:.4f}</b>",
        "pa_isolate_a1": "Isolate a₁: <b>a₁ = aₙ - (n-1) × d</b>",
        "pa_sub_a1": "Substitute: a₁ = {an} - ({n}-1) × {r}",
        "pa_calc_a1": "Calculate: a₁ = {an} - {delta} = <b>{a1:.4f}</b>",
        "pg_formula": "General term: <b>aₙ = a₁ × r^(n-1)</b>",
        "pg_with": "With a₁ = {a1} and r = {q}",
        "pg_term": "a{i} = {a1} × {q}^({i}-1) = {a1} × {qi} = <b>{t}</b>",
        "pg_isolate_q": "Isolate r: <b>r = (aₙ / a₁)^(1/(n-1))</b>",
        "pg_sub_q": "Substitute: r = ({an} / {a1})^(1/({n}-1))",
        "pg_calc_q": "Calculate: r = {ratio}^(1/{exp}) = <b>{q:.4f}</b>",
        "pg_isolate_a1": "Isolate a₁: <b>a₁ = aₙ / r^(n-1)</b>",
        "pg_sub_a1": "Substitute: a₁ = {an} / {q}^({n}-1)",
        "pg_calc_a1": "Calculate: a₁ = {an} / {denom} = <b>{a1:.4f}</b>",
    },
    "es": {
        "menu_title": "Elige una herramienta:",
        "tools": [
            "Inicio", "Álgebra Básica", "Resolución de Ecuaciones", "Funciones y Gráficos",
            "Derivadas", "Integrales", "Sistemas de Ecuaciones", "Matrices y Determinantes",
            "Trigonometría", "Teorema de Pitágoras", "Sucesiones y Progresiones",
            "Combinatoria", "Límites", "Estadística Básica"
        ],
        "home_title": "¡Bienvenido a la calculadora de matemáticas!",
        "home_sub": "### App completa de Matemáticas",
        "home_desc": "Elige cualquier herramienta del menú lateral.",
        "home_tools": "Herramientas", "home_graphs": "Gráficos", "home_inter": "Interactivo",
        "home_caption": "Hecho en Python, por Mateus! 🚀",
        "step": "Paso", "calculate": "Calcular", "show_steps": "Mostrar paso a paso",
        "invalid_expr": "Expresión inválida", "invalid_func": "Función inválida",
        "solve_btn": "Resolver", "solutions": "**Soluciones:**", "no_solution": "No pude resolver",
        "deriv_order": "Orden de la derivada",
        "graph_success": "✅ ¡Gráfico generado con éxito!", "graph_error": "Error al generar gráfico",
        "graph_interval": "Intervalo de x:", "func_type": "Tipo de función:",
        "func_types": ["Lineal (1er grado)", "Cuadrática (2do grado)", "Cúbica (3er grado)", "Trigonométrica", "Exponencial", "Personalizada"],
        "choose": "Elige", "custom_fx": "f(x) =",
        "sys_title": "Sistema 2x2", "no_unique": "El sistema no tiene solución única",
        "mat_size": "Tamaño de la matriz", "determinant": "**Determinante**", "inverse": "Inversa",
        "angle_deg": "Ángulo (grados)",
        "have_angle": "Tengo el ángulo → quiero sen/cos/tan",
        "have_ratio": "Tengo sen/cos/tan → quiero el ángulo",
        "what_have": "¿Qué tienes?", "ratio_type": "¿Qué razón tienes?",
        "ratio_val": "Valor de la razón (entre -1 y 1 para sen/cos):", "invalid_val": "Valor inválido",
        "trig_options": ["seno", "coseno", "tangente"],
        "trig_inv_names": {"seno": ("arcsen", np.arcsin), "coseno": ("arccos", np.arccos), "tangente": ("arctan", np.arctan)},
        "sin_label": "sen",
        "calc_hyp": "Hipotenusa (c)", "calc_a": "Cateto a", "calc_b": "Cateto b",
        "what_missing": "### ¿Qué valor falta?", "calc_label": "Calcular:",
        "hyp_greater": "¡La hipotenusa debe ser mayor que el cateto!",
        "result_hyp": "Hipotenusa c", "result_a": "Cateto a", "result_b": "Cateto b",
        "seq_type": ["PA - Progresión Aritmética", "PG - Progresión Geométrica"],
        "pa_mode1": "Tengo a₁ y la razón → listar términos",
        "pa_mode2": "Tengo a₁ y otro término → hallar razón",
        "pa_mode3": "Tengo la razón y un término → hallar a₁",
        "pg_mode1": "Tengo a₁ y la razón → listar términos",
        "pg_mode2": "Tengo a₁ y otro término → hallar razón",
        "pg_mode3": "Tengo la razón y un término → hallar a₁",
        "first_term": "Primer término (a₁)", "ratio_r": "Razón (r)", "ratio_q": "Razón (q)",
        "num_terms": "Número de términos", "term_pos": "Posición del otro término (n)",
        "known_pos": "Posición del término conocido (n)",
        "terms_label": "Términos:", "sum_label": "Suma",
        "ratio_result": "Razón r", "ratio_q_result": "Razón q",
        "a1_zero": "a₁ no puede ser cero en una PG", "q_zero": "La razón no puede ser cero en una PG",
        "mode_label": "Modo:",
        "comb_combo": "**Combinación**", "comb_fact": "**Factorial**",
        "limit_input": "f(x)", "limit_point": "x →", "limit_error": "Error en el límite",
        "stat_input": "Números (separados por coma)",
        "stat_mean": "Media", "stat_std": "Desviación estándar", "stat_error": "Escribe los números correctamente",
        "x_value": "Valor de x:", "result": "Resultado",
        "equation_input": "Escribe la ecuación:", "expr_input": "Escribe la expresión:", "func_input": "Función f(x):",
        "version": "✅ Versión Completa - v2.0",
        "pit_step1_hyp": "Fórmula del Teorema de Pitágoras: <b>c² = a² + b²</b>",
        "pit_step2_hyp": "Sustituir valores: c² = {a}² + {b}²",
        "pit_step3_hyp": "Calcular cuadrados: c² = {a2} + {b2}",
        "pit_step4_hyp": "Sumar: c² = {ab2}",
        "pit_step5_hyp": "Raíz cuadrada: c = √{ab2} = <b>{c:.4f}</b>",
        "pit_step1_cat": "Fórmula: <b>c² = a² + b²</b> → despejando {v}: <b>{v}² = c² - {u}²</b>",
        "pit_step2_cat": "Sustituir: {v}² = {c}² - {u}²",
        "pit_step3_cat": "Calcular: {v}² = {c2} - {u2}",
        "pit_step4_cat": "Restar: {v}² = {diff}",
        "pit_step5_cat": "Raíz cuadrada: {v} = √{diff} = <b>{res:.4f}</b>",
        "trig_step1_ang": "Convertir a radianes: {ang}° × (π/180) = <b>{rad:.6f} rad</b>",
        "trig_step2_ang": "Calcular seno: sen({ang}°) = <b>{seno:.4f}</b>",
        "trig_step3_ang": "Calcular coseno: cos({ang}°) = <b>{cos:.4f}</b>",
        "trig_step4_ang": "Calcular tangente: tan = sen/cos = {seno:.4f} / {cos:.4f} = <b>{tan:.4f}</b>",
        "trig_step1_inv": "Tienes {tipo} = <b>{val}</b>",
        "trig_step2_inv": "Aplicar función inversa: {func}({val}) = <b>{rad:.6f} rad</b>",
        "trig_step3_inv": "Convertir a grados: {rad:.6f} × (180/π) = <b>{ang:.4f}°</b>",
        "trig_result": "Ángulo = **{ang:.4f}°** ({rad:.4f} rad)",
        "pa_formula": "Término general: <b>aₙ = a₁ + (n-1) × r</b>",
        "pa_with": "Con a₁ = {a1} y r = {r}",
        "pa_term": "a{i} = {a1} + ({i}-1) × {r} = {a1} + {delta} = <b>{t}</b>",
        "pa_sum": "Suma PA: S = n × (a₁ + aₙ) / 2 = {n} × ({a1} + {last}) / 2 = <b>{soma}</b>",
        "pa_isolate_r": "Despejar r: <b>r = (aₙ - a₁) / (n - 1)</b>",
        "pa_sub_r": "Sustituir: r = ({an} - {a1}) / ({n} - 1)",
        "pa_calc_r": "Calcular: r = {num} / {den} = <b>{r:.4f}</b>",
        "pa_isolate_a1": "Despejar a₁: <b>a₁ = aₙ - (n-1) × r</b>",
        "pa_sub_a1": "Sustituir: a₁ = {an} - ({n}-1) × {r}",
        "pa_calc_a1": "Calcular: a₁ = {an} - {delta} = <b>{a1:.4f}</b>",
        "pg_formula": "Término general: <b>aₙ = a₁ × q^(n-1)</b>",
        "pg_with": "Con a₁ = {a1} y q = {q}",
        "pg_term": "a{i} = {a1} × {q}^({i}-1) = {a1} × {qi} = <b>{t}</b>",
        "pg_isolate_q": "Despejar q: <b>q = (aₙ / a₁)^(1/(n-1))</b>",
        "pg_sub_q": "Sustituir: q = ({an} / {a1})^(1/({n}-1))",
        "pg_calc_q": "Calcular: q = {ratio}^(1/{exp}) = <b>{q:.4f}</b>",
        "pg_isolate_a1": "Despejar a₁: <b>a₁ = aₙ / q^(n-1)</b>",
        "pg_sub_a1": "Sustituir: a₁ = {an} / {q}^({n}-1)",
        "pg_calc_a1": "Calcular: a₁ = {an} / {denom} = <b>{a1:.4f}</b>",
    }
}

# ===================== SELEÇÃO DE IDIOMA =====================
idioma_opcoes = {"Português 🇧🇷": "pt", "English 🇺🇸": "en", "Español 🇪🇸": "es"}
idioma_selecionado = st.sidebar.selectbox("🌐 Idioma / Language", list(idioma_opcoes.keys()))
lang = idioma_opcoes[idioma_selecionado]
T = TRADUCOES[lang]

# ===================== MENU =====================
st.sidebar.title("🧮 MathCloud")
opcao_idx = st.sidebar.radio(T["menu_title"], range(len(T["tools"])), format_func=lambda i: T["tools"][i])

x = symbols('x')

def mostrar_passo(numero, texto):
    st.markdown(f"""
    <div class="step-box">
        <strong>{T['step']} {numero}:</strong> {texto}
    </div>
    """, unsafe_allow_html=True)

# ===================== INÍCIO =====================
if opcao_idx == 0:
    st.title(T["home_title"])
    st.markdown(T["home_sub"])
    st.write(T["home_desc"])
    col1, col2, col3 = st.columns(3)
    col1.metric(T["home_tools"], "14")
    col2.metric(T["home_graphs"], "✅")
    col3.metric(T["home_inter"], "100%")
    st.caption(T["home_caption"])

# ===================== FUNÇÕES E GRÁFICOS =====================
elif opcao_idx == 3:
    st.title(f"📈 {T['tools'][3]}")
    tipo = st.radio(T["func_type"], T["func_types"], horizontal=True)
    xmin, xmax = st.slider(T["graph_interval"], -10, 10, (-5, 5))
    x_vals = np.linspace(xmin, xmax, 600)

    if tipo == T["func_types"][0]:
        a = st.number_input("a", value=2.0); b = st.number_input("b", value=-3.0)
        func = a*x + b; f_str = f"{a}x + {b}"
    elif tipo == T["func_types"][1]:
        a = st.number_input("a (x²)", value=1.0); b = st.number_input("b (x)", value=-4.0); c = st.number_input("c", value=3.0)
        func = a*x**2 + b*x + c; f_str = f"{a}x² + {b}x + {c}"
    elif tipo == T["func_types"][2]:
        a = st.number_input("a (x³)", value=1.0); b = st.number_input("b (x²)", value=0.0)
        c = st.number_input("c (x)", value=-2.0); d = st.number_input("d", value=1.0)
        func = a*x**3 + b*x**2 + c*x + d; f_str = f"{a}x³ + {b}x² + {c}x + {d}"
    elif tipo == T["func_types"][3]:
        trig = st.selectbox(T["choose"], ["sin(x)", "cos(x)", "tan(x)"])
        func = sin(x) if trig == "sin(x)" else cos(x) if trig == "cos(x)" else tan(x); f_str = trig
    elif tipo == T["func_types"][4]:
        base = st.number_input("Base", value=2.0); func = base**x; f_str = f"{base}^x"
    else:
        f_str = st.text_input(T["custom_fx"], "x**2 - 4*x + 3"); func = sp.sympify(f_str)

    try:
        f_num = sp.lambdify(x, func, modules=['numpy'])
        y_vals = f_num(x_vals)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f_str, line=dict(color='#FF69B4', width=5)))
        fig.update_layout(title=f"f(x) = {f_str}", xaxis_title="x", yaxis_title="f(x)", template="plotly_dark", height=550)
        st.plotly_chart(fig, use_container_width=True)
        st.success(T["graph_success"])
    except Exception as e:
        st.error(f"{T['graph_error']}: {str(e)}")

# ===================== OUTRAS SEÇÕES =====================
else:
    st.title(T["tools"][opcao_idx])

    # ÁLGEBRA BÁSICA
    if opcao_idx == 1:
        expr = st.text_input(T["expr_input"], "2*x**2 + 3*x - 5")
        try:
            res = sp.sympify(expr)
            val = st.number_input(T["x_value"], value=2.0)
            st.success(f"{T['result']} = **{res.subs(x, val)}**")
            st.latex(f"{sp.latex(res)}")
        except:
            st.error(T["invalid_expr"])

    # RESOLUÇÃO DE EQUAÇÕES
    elif opcao_idx == 2:
        eq = st.text_input(T["equation_input"], "x**2 - 5*x + 6 = 0")
        if st.button(T["solve_btn"]):
            try:
                lhs, rhs = [p.strip() for p in eq.split("=")]
                sol = solve(Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
                st.write(T["solutions"])
                for s in sol:
                    st.latex(sp.latex(s))
            except:
                st.error(T["no_solution"])

    # DERIVADAS
    elif opcao_idx == 4:
        f = st.text_input(T["func_input"], "x**3 + 2*x**2 - 5*x")
        ordem = st.slider(T["deriv_order"], 1, 5, 1)
        try:
            deriv = diff(sp.sympify(f), x, ordem)
            st.latex(f"f^{{{ordem}}}(x) = {sp.latex(deriv)}")
        except:
            st.error(T["invalid_func"])

    # INTEGRAIS
    elif opcao_idx == 5:
        f = st.text_input(T["func_input"], "x**2 + 3*x")
        try:
            integral = integrate(sp.sympify(f), x)
            st.latex(f"\\int {sp.latex(sp.sympify(f))} dx = {sp.latex(integral)} + C")
        except:
            st.error(T["invalid_func"])

    # SISTEMAS DE EQUAÇÕES
    elif opcao_idx == 6:
        st.write(T["sys_title"])
        col1, col2 = st.columns(2)
        a = col1.number_input("a", value=2.0); b = col1.number_input("b", value=3.0)
        c = col2.number_input("c", value=8.0); d = col1.number_input("d", value=4.0)
        e = col1.number_input("e", value=-1.0); f_val = col2.number_input("f", value=7.0)
        try:
            mat = sp.Matrix([[a, b], [d, e]]); const = sp.Matrix([c, f_val])
            sol = mat.solve(const)
            st.success(f"x = {sol[0]:.4f} | y = {sol[1]:.4f}")
        except:
            st.error(T["no_unique"])

    # MATRIZES E DETERMINANTES
    elif opcao_idx == 7:
        n = st.slider(T["mat_size"], 2, 4, 3)
        df = pd.DataFrame(np.zeros((n, n)))
        edited = st.data_editor(df, use_container_width=True)
        mat = sp.Matrix(edited.values)
        st.write(f"{T['determinant']} = {mat.det()}")
        if mat.det() != 0:
            st.latex(f"{T['inverse']} = {sp.latex(mat.inv())}")

    # TRIGONOMETRIA
    elif opcao_idx == 8:
        st.markdown(f"### {T['what_have']}")
        modo = st.radio(T["what_have"], [T["have_angle"], T["have_ratio"]], horizontal=True)
        passo_a_passo = st.checkbox(T["show_steps"])

        if modo == T["have_angle"]:
            ang = st.number_input(T["angle_deg"], value=30.0)
            if st.button(T["calculate"]):
                rad = np.deg2rad(ang)
                seno = np.sin(rad); cosseno = np.cos(rad); tangente = np.tan(rad)
                if passo_a_passo:
                    mostrar_passo(1, T["trig_step1_ang"].format(ang=ang, rad=rad))
                    mostrar_passo(2, T["trig_step2_ang"].format(ang=ang, seno=seno))
                    mostrar_passo(3, T["trig_step3_ang"].format(ang=ang, cos=cosseno))
                    mostrar_passo(4, T["trig_step4_ang"].format(seno=seno, cos=cosseno, tan=tangente))
                else:
                    c1, c2, c3 = st.columns(3)
                    c1.metric(T["sin_label"], f"{seno:.4f}")
                    c2.metric("cos", f"{cosseno:.4f}")
                    c3.metric("tan", f"{tangente:.4f}")
        else:
            razao_tipo = st.selectbox(T["ratio_type"], T["trig_options"])
            valor = st.number_input(T["ratio_val"], value=0.5, format="%.4f")
            if st.button(T["calculate"]):
                try:
                    nome_func, func_inv = T["trig_inv_names"][razao_tipo]
                    rad = func_inv(valor)
                    ang_res = np.rad2deg(rad)
                    if passo_a_passo:
                        mostrar_passo(1, T["trig_step1_inv"].format(tipo=razao_tipo, val=valor))
                        mostrar_passo(2, T["trig_step2_inv"].format(func=nome_func, val=valor, rad=rad))
                        mostrar_passo(3, T["trig_step3_inv"].format(rad=rad, ang=ang_res))
                    else:
                        st.success(T["trig_result"].format(ang=ang_res, rad=rad))
                except Exception as e:
                    st.error(f"{T['invalid_val']}: {str(e)}")

    # TEOREMA DE PITÁGORAS
    elif opcao_idx == 9:
        st.markdown(T["what_missing"])
        faltando = st.radio(T["calc_label"], [T["calc_hyp"], T["calc_a"], T["calc_b"]], horizontal=True)
        passo_a_passo = st.checkbox(T["show_steps"])

        if faltando == T["calc_hyp"]:
            a = st.number_input(T["calc_a"], value=3.0, min_value=0.01)
            b = st.number_input(T["calc_b"], value=4.0, min_value=0.01)
            if st.button(T["calculate"]):
                c = np.sqrt(a**2 + b**2)
                if passo_a_passo:
                    mostrar_passo(1, T["pit_step1_hyp"])
                    mostrar_passo(2, T["pit_step2_hyp"].format(a=a, b=b))
                    mostrar_passo(3, T["pit_step3_hyp"].format(a2=a**2, b2=b**2))
                    mostrar_passo(4, T["pit_step4_hyp"].format(ab2=a**2+b**2))
                    mostrar_passo(5, T["pit_step5_hyp"].format(ab2=a**2+b**2, c=c))
                else:
                    st.success(f"{T['result_hyp']} = **{c:.4f}**")

        elif faltando == T["calc_a"]:
            c = st.number_input(T["calc_hyp"], value=5.0, min_value=0.01)
            b = st.number_input(T["calc_b"], value=4.0, min_value=0.01)
            if st.button(T["calculate"]):
                if c <= b:
                    st.error(T["hyp_greater"])
                else:
                    a = np.sqrt(c**2 - b**2)
                    if passo_a_passo:
                        mostrar_passo(1, T["pit_step1_cat"].format(v="a", u="b"))
                        mostrar_passo(2, T["pit_step2_cat"].format(v="a", c=c, u=b))
                        mostrar_passo(3, T["pit_step3_cat"].format(v="a", c2=c**2, u2=b**2))
                        mostrar_passo(4, T["pit_step4_cat"].format(v="a", diff=c**2-b**2))
                        mostrar_passo(5, T["pit_step5_cat"].format(v="a", diff=c**2-b**2, res=a))
                    else:
                        st.success(f"{T['result_a']} = **{a:.4f}**")
        else:
            c = st.number_input(T["calc_hyp"], value=5.0, min_value=0.01)
            a = st.number_input(T["calc_a"], value=3.0, min_value=0.01)
            if st.button(T["calculate"]):
                if c <= a:
                    st.error(T["hyp_greater"])
                else:
                    b = np.sqrt(c**2 - a**2)
                    if passo_a_passo:
                        mostrar_passo(1, T["pit_step1_cat"].format(v="b", u="a"))
                        mostrar_passo(2, T["pit_step2_cat"].format(v="b", c=c, u=a))
                        mostrar_passo(3, T["pit_step3_cat"].format(v="b", c2=c**2, u2=a**2))
                        mostrar_passo(4, T["pit_step4_cat"].format(v="b", diff=c**2-a**2))
                        mostrar_passo(5, T["pit_step5_cat"].format(v="b", diff=c**2-a**2, res=b))
                    else:
                        st.success(f"{T['result_b']} = **{b:.4f}**")

    # SEQUÊNCIAS E PROGRESSÕES
    elif opcao_idx == 10:
        tipo = st.selectbox("", T["seq_type"])
        passo_a_passo = st.checkbox(T["show_steps"])

        if tipo == T["seq_type"][0]:  # PA
            st.markdown(f"### {T['what_have']}")
            modo = st.radio(T["mode_label"], [T["pa_mode1"], T["pa_mode2"], T["pa_mode3"]])

            if modo == T["pa_mode1"]:
                a1 = st.number_input(T["first_term"], value=2.0)
                r = st.number_input(T["ratio_r"], value=3.0)
                n = st.number_input(T["num_terms"], 2, 20, 8)
                if st.button(T["calculate"]):
                    termos = [a1 + (k-1)*r for k in range(1, int(n)+1)]
                    soma = sum(termos)
                    if passo_a_passo:
                        mostrar_passo(1, T["pa_formula"])
                        mostrar_passo(2, T["pa_with"].format(a1=a1, r=r))
                        for i, t in enumerate(termos, 1):
                            mostrar_passo(i+2, T["pa_term"].format(i=i, a1=a1, r=r, delta=(i-1)*r, t=t))
                        mostrar_passo(len(termos)+3, T["pa_sum"].format(n=int(n), a1=a1, last=termos[-1], soma=soma))
                    else:
                        st.write(T["terms_label"], [round(t, 4) for t in termos])
                        st.write(f"**{T['sum_label']} = {soma:.4f}**")

            elif modo == T["pa_mode2"]:
                a1 = st.number_input(T["first_term"], value=2.0)
                n = st.number_input(T["term_pos"], 2, 50, 5)
                an = st.number_input(f"a{int(n)}", value=14.0)
                if st.button(T["calculate"]):
                    r = (an - a1) / (n - 1)
                    if passo_a_passo:
                        mostrar_passo(1, T["pa_formula"])
                        mostrar_passo(2, T["pa_isolate_r"])
                        mostrar_passo(3, T["pa_sub_r"].format(an=an, a1=a1, n=int(n)))
                        mostrar_passo(4, T["pa_calc_r"].format(num=an-a1, den=n-1, r=r))
                    else:
                        st.success(f"{T['ratio_result']} = **{r:.4f}**")

            else:
                r = st.number_input(T["ratio_r"], value=3.0)
                n = st.number_input(T["known_pos"], 2, 50, 4)
                an = st.number_input(f"a{int(n)}", value=11.0)
                if st.button(T["calculate"]):
                    a1 = an - (n - 1) * r
                    if passo_a_passo:
                        mostrar_passo(1, T["pa_formula"])
                        mostrar_passo(2, T["pa_isolate_a1"])
                        mostrar_passo(3, T["pa_sub_a1"].format(an=an, n=int(n), r=r))
                        mostrar_passo(4, T["pa_calc_a1"].format(an=an, delta=(n-1)*r, a1=a1))
                    else:
                        st.success(f"{T['first_term']} = **{a1:.4f}**")

        else:  # PG
            st.markdown(f"### {T['what_have']}")
            modo = st.radio(T["mode_label"], [T["pg_mode1"], T["pg_mode2"], T["pg_mode3"]])

            if modo == T["pg_mode1"]:
                a1 = st.number_input(T["first_term"], value=2.0)
                q = st.number_input(T["ratio_q"], value=3.0)
                n = st.number_input(T["num_terms"], 2, 20, 6)
                if st.button(T["calculate"]):
                    termos = [a1 * (q ** (k-1)) for k in range(1, int(n)+1)]
                    if passo_a_passo:
                        mostrar_passo(1, T["pg_formula"])
                        mostrar_passo(2, T["pg_with"].format(a1=a1, q=q))
                        for i, t in enumerate(termos, 1):
                            mostrar_passo(i+2, T["pg_term"].format(i=i, a1=a1, q=q, qi=round(q**(i-1),4), t=round(t,4)))
                    else:
                        st.write(T["terms_label"], [round(t, 4) for t in termos])

            elif modo == T["pg_mode2"]:
                a1 = st.number_input(T["first_term"], value=2.0)
                n = st.number_input(T["term_pos"], 2, 20, 4)
                an = st.number_input(f"a{int(n)}", value=54.0)
                if st.button(T["calculate"]):
                    if a1 == 0:
                        st.error(T["a1_zero"])
                    else:
                        q = (an / a1) ** (1 / (n - 1))
                        if passo_a_passo:
                            mostrar_passo(1, T["pg_formula"])
                            mostrar_passo(2, T["pg_isolate_q"])
                            mostrar_passo(3, T["pg_sub_q"].format(an=an, a1=a1, n=int(n)))
                            mostrar_passo(4, T["pg_calc_q"].format(ratio=round(an/a1,4), exp=int(n-1), q=q))
                        else:
                            st.success(f"{T['ratio_q_result']} = **{q:.4f}**")
            else:
                q = st.number_input(T["ratio_q"], value=3.0)
                n = st.number_input(T["known_pos"], 2, 20, 4)
                an = st.number_input(f"a{int(n)}", value=54.0)
                if st.button(T["calculate"]):
                    if q == 0:
                        st.error(T["q_zero"])
                    else:
                        a1 = an / (q ** (n - 1))
                        if passo_a_passo:
                            mostrar_passo(1, T["pg_formula"])
                            mostrar_passo(2, T["pg_isolate_a1"])
                            mostrar_passo(3, T["pg_sub_a1"].format(an=an, q=q, n=int(n)))
                            mostrar_passo(4, T["pg_calc_a1"].format(an=an, denom=round(q**(n-1),4), a1=a1))
                        else:
                            st.success(f"{T['first_term']} = **{a1:.4f}**")

    # COMBINATÓRIA
    elif opcao_idx == 11:
        n = st.number_input("n", 5, 20, 5)
        k = st.number_input("k", 0, n, 2)
        st.write(f"{T['comb_combo']} C({n},{k}) = {binomial(n,k)}")
        st.write(f"{T['comb_fact']} {n}! = {factorial(n)}")

    # LIMITES
    elif opcao_idx == 12:
        f_str = st.text_input(T["limit_input"], "sin(x)/x")
        ponto = st.number_input(T["limit_point"], value=0.0)
        try:
            lim = limit(sp.sympify(f_str), x, ponto)
            st.latex(f"lim = {sp.latex(lim)}")
        except:
            st.error(T["limit_error"])

    # ESTATÍSTICA BÁSICA
    elif opcao_idx == 13:
        dados = st.text_input(T["stat_input"], "2,4,4,5,5,7,9")
        try:
            nums = np.array([float(i) for i in dados.split(",")])
            st.write(f"{T['stat_mean']} = {np.mean(nums):.3f}")
            st.write(f"{T['stat_std']} = {np.std(nums):.3f}")
        except:
            st.error(T["stat_error"])

st.sidebar.caption(T["version"])
