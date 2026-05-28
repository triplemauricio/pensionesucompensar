"""
CALCULADORA PENSIONAL SIMPLIFICADA — Colombia 2026
Proyecto de Matemática Fundamental — UCompensar
Actividad 1 — Aprendizaje Basado en Proyectos (ABP)

AUTORES: GRUPO 4 MATEMÁTICA FUNDAMENTAL
- María Camila González Cárdenas (macamilagonzalezc@ucompensar.edu.co)
- Carlos Mauricio Moreno Cruz (cmmorenoc@ucompensar.edu.co)
- Paola Andrea Serrato Orjuela (pandreaserrato@ucompensar.edu.co)
- Claudia Lizeth Tatiana Castro Manrique (clizethtatianacastro@ucompensar.edu.co)

ASIGNATURA: Matemática Fundamental
DOCENTE: Leidy Milena Hernández López
Ingeniería / Primer semestre

MATEMÁTICAS USADAS EN ESTE PROGRAMA (enunciadas en Actividad1_Calculadora_Pensional.docx)
──────────────────────────────────────────────────────────────────────────────
1. ARITMÉTICA BÁSICA (suma, resta, multiplicación, división)
   → Semanas restantes, años faltantes, cotizaciones acumuladas

2. PROPORCIONALIDAD Y PORCENTAJES
   → Aporte mensual = 16 % del IBC (proporción directa)
   → Razón: cuántos salarios mínimos equivale el ingreso

3. EXPRESIÓN ALGEBRAICA (función suelo ⌊x⌋)
   → Fórmula mesada pensional — Art. 34, Ley 100 de 1993

4. RADICACIÓN (raíz cuadrada)
   → Indicador de riesgo pensional: riesgo = √(fracción_faltante) × 10

5. LOGARITMOS (base 10)
   → Indicador de avance relativo: log₁₀(n+1) / log₁₀(N+1) × 100

6. ECUACIÓN LINEAL (y = mx + b)
   → BONUS: Proyección de rentabilidad en CDT (Interés simple)

BASE LEGAL
──────────────────────────────────────────────────────────────────────────────
- Ley 100 de 1993 · Ley 2381 de 2024 · SMMLV 2026: $1.750.905 COP
NOTA: Herramienta educativa y aproximada. No reemplaza asesoría oficial.
"""

import math
import streamlit as st


# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTES DEL SISTEMA PENSIONAL COLOMBIANO 2026
# ══════════════════════════════════════════════════════════════════════════════

SMMLV              = 1750905   # Salario Mínimo Mensual Legal Vigente 2026
PORCENTAJE_PENSION = 0.16        # 16 % del IBC (Art. 20, Ley 100/1993)
SEMANAS_MIN_MUJER  = 1000       # Ley 2381 de 2024 (reforma pensional)
SEMANAS_MIN_HOMBRE = 1300
EDAD_MIN_MUJER     = 57
EDAD_MIN_HOMBRE    = 62
SEMANAS_POR_ANO    = 52


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN 1: CALCULAR IBC
# Matemática: Aritmética (comparación y selección del máximo)
# ══════════════════════════════════════════════════════════════════════════════

def calcular_ibc(salario_bruto: float) -> float:
    """
    Calcula el Ingreso Base de Cotización (IBC) mensual.
    FÓRMULA: IBC = max(salario_bruto, SMMLV)
    El IBC nunca puede ser menor al salario mínimo (Art. 20, Ley 100/1993).
    """
    return max(salario_bruto, SMMLV)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN 2: CALCULAR APORTES MENSUALES
# Matemática: Proporcionalidad directa y porcentajes
# ══════════════════════════════════════════════════════════════════════════════

def calcular_aportes(ibc: float) -> dict:
    """
    Calcula la distribución del aporte mensual a pensión.
    FÓRMULAS:
        Aporte total     = IBC × 0.16   (16 % del IBC)
        Parte empleador  = IBC × 0.12   (12 %)
        Parte empleado   = IBC × 0.04   ( 4 %)
    Relación directa: si el IBC sube k veces, el aporte sube k veces.
    """
    return {
        "total":     round(ibc * 0.16, 0),
        "empleador": round(ibc * 0.12, 0),
        "empleado":  round(ibc * 0.04, 0),
    }


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN 3: CALCULAR PROGRESO EN SEMANAS
# Matemática: Aritmética (resta, división, porcentaje)
# ══════════════════════════════════════════════════════════════════════════════

def calcular_progreso(semanas_cotizadas: int, es_mujer: bool) -> dict:
    """
    Calcula el progreso del trabajador hacia la pensión.
    FÓRMULAS:
        semanas_rest  = semanas_req − semanas_cotizadas   [resta]
        anios_rest    = semanas_rest ÷ 52                 [división]
        avance (%)    = (semanas_cotizadas ÷ semanas_req) × 100
    """
    semanas_req  = SEMANAS_MIN_MUJER if es_mujer else SEMANAS_MIN_HOMBRE
    semanas_rest = max(0, semanas_req - semanas_cotizadas)
    anios_rest   = semanas_rest / SEMANAS_POR_ANO
    avance_pct   = min(100.0, (semanas_cotizadas / semanas_req) * 100)
    return {
        "semanas_req":   semanas_req,
        "semanas_rest":  semanas_rest,
        "anios_rest":    round(anios_rest, 1),
        "avance_pct":    round(avance_pct, 1),
        "ya_pensionado": semanas_cotizadas >= semanas_req,
    }


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN 4: INDICADOR DE RIESGO CON RAÍZ CUADRADA
# Matemática: Radicación (raíz cuadrada)
# ══════════════════════════════════════════════════════════════════════════════

def calcular_riesgo(semanas_cotizadas: int, semanas_req: int) -> float:
    """
    Calcula un indicador de riesgo pensional usando raíz cuadrada.
    FÓRMULA:
        fraccion_faltante = semanas_rest / semanas_req
        riesgo = √(fraccion_faltante) × 10        [escala 0 – 10]
    √x crece más lento que x → suaviza las diferencias grandes.
    """
    semanas_rest      = max(0, semanas_req - semanas_cotizadas)
    fraccion_faltante = semanas_rest / semanas_req
    return round(math.sqrt(fraccion_faltante) * 10, 2)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN 5: AVANCE LOGARÍTMICO
# Matemática: Logaritmo en base 10
# ══════════════════════════════════════════════════════════════════════════════

def calcular_avance_log(semanas_cotizadas: int, semanas_req: int) -> float:
    """
    Calcula el avance relativo usando logaritmos.
    FÓRMULA:
        avance_log = [log₁₀(n+1) / log₁₀(N+1)] × 100
    +1 evita log(0). El logaritmo pondera más los primeros aportes.
    """
    if semanas_cotizadas <= 0:
        return 0.0
    log_cot = math.log10(semanas_cotizadas + 1)
    log_req = math.log10(semanas_req + 1)
    return round(min(100.0, (log_cot / log_req) * 100), 1)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN 6: ESTIMAR MESADA PENSIONAL
# Matemática: Expresión algebraica con función suelo ⌊x⌋
# ══════════════════════════════════════════════════════════════════════════════

def estimar_mesada(semanas_cotizadas: int, ibc_promedio: float, es_mujer: bool) -> float:
    """
    Estima la mesada pensional mensual (Art. 34, Ley 100/1993).
    FÓRMULA:
        semanas_adicionales = n − N
        bonos = ⌊(n−N)/50⌋ × 0.015     (función suelo ⌊x⌋)
        tasa  = min(0.80, 0.65 + bonos) (máximo 80 %)
        mesada = tasa × IBC_promedio    (mínimo 1 SMMLV)
    """
    semanas_min = SEMANAS_MIN_MUJER if es_mujer else SEMANAS_MIN_HOMBRE
    if semanas_cotizadas < semanas_min:
        return 0.0
    semanas_adicionales = semanas_cotizadas - semanas_min
    bonos  = math.floor(semanas_adicionales / 50) * 0.015
    tasa   = min(0.80, 0.65 + bonos)
    mesada = max(tasa * ibc_promedio, SMMLV)
    return round(mesada, 0)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN 7: BONUS CDT (ECUACIÓN LINEAL)
# Matemática: Ecuación de la recta (y = mx + b)
# ══════════════════════════════════════════════════════════════════════════════

def calcular_cdt_lineal(capital: float, tasa_anual_pct: float, meses: int) -> dict:
    """
    Calcula la rentabilidad de un CDT de interés simple usando y = mx + b.
    y = Total final recibido (variable dependiente)
    m = Interés mensual fijo en dinero (pendiente)
    x = Meses del CDT (variable independiente)
    b = Capital inicial invertido (intercepto)
    """
    tasa_mensual = (tasa_anual_pct / 100) / 12
    interes_mensual_fijo = capital * tasa_mensual
    
    total = (interes_mensual_fijo * meses) + capital
    return {
        "total": round(total, 0),
        "m": round(interes_mensual_fijo, 0),
        "x": meses,
        "b": capital
    }


# ══════════════════════════════════════════════════════════════════════════════
# INTERFAZ STREAMLIT — reemplaza a generar_reporte() de la versión consola
# ══════════════════════════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="Calculadora Pensional — UCompensar",
        page_icon="🧮",
        layout="centered",
    )

    # ── Encabezado ─────────────────────────────────────────────────────────
    st.title("🧮 Calculadora Pensional Simplificada")
    st.markdown(
        "**Matemática Fundamental · UCompensar 2026** — Actividad 1 ABP  \n"
        "**Autores: Grupo 4** \n"
        "- María Camila González Cárdenas (`macamilagonzalezc@ucompensar.edu.co`)  \n"
        "- Carlos Mauricio Moreno Cruz (`cmmorenoc@ucompensar.edu.co`)  \n"
        "- Paola Andrea Serrato Orjuela (`pandreaserrato@ucompensar.edu.co`)  \n"
        "- Claudia Lizeth Tatiana Castro Manrique (`clizethtatianacastro@ucompensar.edu.co`)  \n\n"
        "**Docente:** Leidy Milena Hernández López"
    )
    st.divider()

    # ── Panel de entrada ───────────────────────────────────────────────────
    st.subheader("📝 Ingresa tus datos")

    col1, col2 = st.columns(2)
    with col1:
        nombre            = st.text_input("Nombre", value="Ana García")
        edad              = st.number_input("Edad actual", min_value=18, max_value=80, value=30)
        genero            = st.radio("Género", ["Mujer", "Hombre"], horizontal=True)
    with col2:
        salario_bruto     = st.number_input(
            "Salario bruto mensual (COP)",
            min_value=500_000, max_value=30_000_000,
            value=2_500_000, step=100_000, format="%d"
        )
        semanas_cotizadas = st.number_input(
            "Semanas cotizadas", min_value=0, max_value=3_000, value=200
        )

    es_mujer = (genero == "Mujer")

    st.divider()

    # ── Bonus CDT Entrada ──────────────────────────────────────────────────
    st.subheader("🎁 Bonus: Ahorro Adicional en CDT (Ecuación Lineal)")
    st.markdown("Calcula cuánto sacarías extra en un CDT de interés simple ($y=mx+b$).")
    
    col3, col4 = st.columns(2)
    with col3:
        cdt_capital = st.number_input("Capital a invertir ($) [b]", min_value=0, value=1000000, step=100000)
        cdt_tasa = st.number_input("Tasa Efectiva Anual (%)", min_value=0.0, value=10.0, step=0.5)
    with col4:
        cdt_meses = st.number_input("Meses del CDT [x]", min_value=1, max_value=120, value=12)

    st.divider()

    if not st.button("⚡ Calcular", type="primary", use_container_width=True):
        st.info("Completa los datos y pulsa **Calcular**.")
        return

    # ── Cálculos (mismas funciones del .py original) ───────────────────────
    ibc       = calcular_ibc(salario_bruto)
    aportes   = calcular_aportes(ibc)
    prog      = calcular_progreso(semanas_cotizadas, es_mujer)
    riesgo    = calcular_riesgo(semanas_cotizadas, prog["semanas_req"])
    avance_log= calcular_avance_log(semanas_cotizadas, prog["semanas_req"])
    mesada    = estimar_mesada(semanas_cotizadas, ibc, es_mujer)

    # Cálculo extra del Bonus CDT
    res_cdt   = calcular_cdt_lineal(cdt_capital, cdt_tasa, cdt_meses)

    # Operaciones adicionales enunciadas en el documento
    # (proporcionalidad: razón salario/SMMLV)
    razon_smmlv = round(salario_bruto / SMMLV, 2)

    # (aritmética: proyección de aportes acumulados)
    meses_cotizados  = round(semanas_cotizadas * 12 / 52, 1)
    total_aportado   = round(aportes["total"] * meses_cotizados, 0)
    meses_restantes  = round(prog["semanas_rest"] * 12 / 52, 1)
    total_por_aportar= round(aportes["total"] * meses_restantes, 0)

    # (aritmética: edad de pensión)
    edad_min      = EDAD_MIN_MUJER if es_mujer else EDAD_MIN_HOMBRE
    genero_str    = "Mujer" if es_mujer else "Hombre"

    # ── Métricas rápidas ───────────────────────────────────────────────────
    st.subheader(f"📊 Resultados de {nombre}")
    c1, c2, c3 = st.columns(3)
    c1.metric("IBC (base de aporte)", f"${ibc:,.0f}")
    c2.metric("Aporte mensual (16%)", f"${aportes['total']:,.0f}")
    c3.metric("Avance pensional", f"{prog['avance_pct']:.1f}%")

    st.divider()

    # ── 1. Aritmética básica ───────────────────────────────────────────────
    st.subheader("1️⃣ Aritmética básica — semanas y años")
    st.markdown(f"""
- **Semanas requeridas:** {prog['semanas_req']:,} &nbsp;({'mujer' if es_mujer else 'hombre'}, Ley 2381/2024)
- **Semanas restantes:** {prog['semanas_req']:,} − {semanas_cotizadas:,} = **{prog['semanas_rest']:,} sem.**
- **Años restantes:** {prog['semanas_rest']:,} ÷ 52 = **{prog['anios_rest']:.1f} años**
- **Avance:** ({semanas_cotizadas:,} ÷ {prog['semanas_req']:,}) × 100 = **{prog['avance_pct']:.1f}%**
- **Aportes acumulados** (≈{meses_cotizados:.0f} meses): ${aportes['total']:,.0f} × {meses_cotizados:.0f} = **${total_aportado:,.0f}**
- **Falta por aportar** (≈{meses_restantes:.0f} meses): ${aportes['total']:,.0f} × {meses_restantes:.0f} = **${total_por_aportar:,.0f}**
    """)
    st.progress(min(1.0, prog["avance_pct"] / 100),
                text=f"Progreso: {prog['avance_pct']:.1f}% de las semanas requeridas")
    if prog["ya_pensionado"]:
        st.success("✅ ¡Ya cumples las semanas mínimas para pensionarte!")

    # ── 2. Proporcionalidad y porcentajes ──────────────────────────────────
    st.subheader("2️⃣ Proporcionalidad y porcentajes")
    st.markdown(f"""
- **Razón salario / SMMLV:** ${salario_bruto:,.0f} ÷ ${SMMLV:,.0f} = **{razon_smmlv}×** el mínimo
- **IBC** = max(${salario_bruto:,.0f} ; ${SMMLV:,.0f}) = **${ibc:,.0f}**
- **Aporte total (16%):** ${ibc:,.0f} × 0,16 = **${aportes['total']:,.0f}**
  - Empleador (12%): ${ibc:,.0f} × 0,12 = **${aportes['empleador']:,.0f}**
  - Empleado (4%): &nbsp; ${ibc:,.0f} × 0,04 = **${aportes['empleado']:,.0f}**
  - Verificación: ${aportes['empleador']:,.0f} + ${aportes['empleado']:,.0f} = **${aportes['total']:,.0f} ✓**
    """)
    if salario_bruto < SMMLV:
        st.warning("⚠️ Salario < SMMLV → el IBC se ajusta automáticamente al mínimo legal.")

    # ── 3. Expresión algebraica (mesada) ───────────────────────────────────
    st.subheader("3️⃣ Expresión algebraica — Mesada pensional (Art. 34, Ley 100)")
    if mesada > 0:
        sem_min   = SEMANAS_MIN_MUJER if es_mujer else SEMANAS_MIN_HOMBRE
        sem_adic  = semanas_cotizadas - sem_min
        bonos     = math.floor(sem_adic / 50) * 0.015
        tasa      = min(0.80, 0.65 + bonos)
        st.markdown(f"""
- Semanas adicionales: {semanas_cotizadas} − {sem_min} = **{sem_adic}**
- Bonos = ⌊{sem_adic} ÷ 50⌋ × 0,015 = {math.floor(sem_adic/50)} × 0,015 = **{bonos:.3f}**
- Tasa = min(0,80 ; 0,65 + {bonos:.3f}) = **{tasa:.3f}** ({tasa*100:.1f}%)
- **Mesada estimada:** {tasa:.3f} × ${ibc:,.0f} = **${mesada:,.0f} / mes**

> 🔢 *Función suelo* ⌊x⌋: entero más grande ≤ x. Ej.: ⌊3,7⌋ = 3.  
> La mesada mínima garantizada es 1 SMMLV = ${SMMLV:,.0f}.
        """)
        st.success(f"💰 Mesada estimada: **${mesada:,.0f} COP / mes**")
    else:
        st.warning(
            f"⏳ Aún no tienes derecho a mesada. "
            f"Faltan **{prog['semanas_rest']:,} semanas** ({prog['anios_rest']:.1f} años)."
        )

    # ── 4. Raíz cuadrada (riesgo) ──────────────────────────────────────────
    st.subheader("4️⃣ Raíz cuadrada — Indicador de riesgo pensional")
    fraccion_f = prog["semanas_rest"] / prog["semanas_req"]
    st.markdown(f"""
- Fracción faltante: {prog['semanas_rest']} ÷ {prog['semanas_req']} = **{fraccion_f:.4f}**
- Riesgo = √{fraccion_f:.4f} × 10 = **{riesgo:.2f} / 10**

> *√x crece más lento que x* → amortigua diferencias grandes, igual que en modelos de riesgo financiero.
    """)
    if riesgo <= 2.0:
        st.success(f"🟢 Riesgo {riesgo:.2f} — BAJO: ¡Casi te pensionas!")
    elif riesgo <= 5.0:
        st.info(f"🟡 Riesgo {riesgo:.2f} — MEDIO: Vas bien, no pares de cotizar")
    elif riesgo <= 8.0:
        st.warning(f"🟠 Riesgo {riesgo:.2f} — ALTO: Considera aportes voluntarios")
    else:
        st.error(f"🔴 Riesgo {riesgo:.2f} — MUY ALTO: Apenas empiezas, ¡actúa ya!")

    # ── 5. Logaritmo (avance relativo) ─────────────────────────────────────
    st.subheader("5️⃣ Logaritmo base 10 — Avance relativo (esfuerzo acumulado)")
    if semanas_cotizadas > 0:
        l1 = math.log10(semanas_cotizadas + 1)
        l2 = math.log10(prog["semanas_req"] + 1)
        st.markdown(f"""
- log₁₀({semanas_cotizadas} + 1) = log₁₀({semanas_cotizadas+1}) = **{l1:.4f}**
- log₁₀({prog['semanas_req']} + 1) = log₁₀({prog['semanas_req']+1}) = **{l2:.4f}**
- Avance log = ({l1:.4f} ÷ {l2:.4f}) × 100 = **{avance_log:.1f}%**

| Métrica | Valor |
|---|---|
| Avance lineal (simple) | {prog['avance_pct']:.1f}% |
| Avance logarítmico | **{avance_log:.1f}%** |

> El logaritmo pondera más las *primeras semanas* (las de mayor riesgo).  
> Por eso el avance log siempre es ≥ al avance lineal.
        """)
    else:
        st.info("Sin semanas cotizadas → avance logarítmico = 0%.")

    # ── 6. Bonus CDT (Ecuación Lineal) ─────────────────────────────────────
    st.subheader("6️⃣ BONUS: Rentabilidad CDT (Ecuación Lineal)")
    st.info("El interés simple de un CDT crece en línea recta, por eso usamos la ecuación **y = mx + b**.")
    st.markdown(f"""
- **$m$ (Pendiente):** Interés fijo mensual = **${res_cdt['m']:,.0f}**
- **$x$ (Tiempo):** **{res_cdt['x']} meses**
- **$b$ (Intercepto):** Capital invertido = **${res_cdt['b']:,.0f}**

**Cálculo:**
$y = ({res_cdt['m']:,.0f} \\times {res_cdt['x']}) + {res_cdt['b']:,.0f}$
    """)
    st.success(f"📈 Total a recibir al final del CDT ($y$): **${res_cdt['total']:,.0f} COP**")

    # ── Edad proyectada ────────────────────────────────────────────────────
    st.subheader("⏰ Edad de pensión")
    st.markdown(f"""
- Edad mínima legal ({genero_str}): **{edad_min} años**
- Tu edad actual: **{edad} años**
    """)
    if edad >= edad_min:
        st.success(f"✅ Ya cumples la edad mínima ({edad_min} años).")
    else:
        st.info(f"Faltan {edad_min - edad} años para llegar a la edad de pensión.")

    # ── Nota legal ─────────────────────────────────────────────────────────
    st.divider()
    st.caption(
        "⚠️ Este cálculo es educativo y aproximado. "
        "Para asesoría real: Colpensiones ☎ 01 8000 91 0011 · "
        "Ley 100/1993 · Ley 2381/2024 · SMMLV 2026: $1.750.905."
    )


if __name__ == "__main__":
    main()