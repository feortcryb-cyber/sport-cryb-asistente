    border-radius: 16px;
    padding: 9px 13px;
    color: #172b3a;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li {
    color: #172b3a !important;
}
.stButton button {
    border-radius: 14px;
    border: 1px solid #9bcce7;
    background: #d8efff;
    color: #123c5a;
    min-height: 44px;
    font-weight: 650;
}
.stButton button:hover {
    border-color: #1976b9;
    background: #c3e6fb;
    color: #123c5a;
}
div[data-testid="stChatInput"] {
    background: #f8fcff;
}
div[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #172b3a !important;
    border: 1px solid #9bcce7 !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #617989 !important;
}
div[data-testid="stExpander"] {
    background: #f8fcff;
    border: 1px solid #b8dced;
    border-radius: 12px;
}
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary p {
    color: #123c5a !important;
}
.small-note {
    color: #40596b;
    font-size: 12px;
    text-align: center;
    margin-top: 20px;
}
/* Ajustes para que los controles mantengan buen contraste */
input, textarea {
    color: #172b3a !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand-card">
  <div class="brand-kicker">INDUMENTARIA DEPORTIVA PERSONALIZADA</div>
  <div class="brand-title">⚽ SPORT CRYB</div>
  <div class="brand-sub">Tu equipo, tu diseño, tu identidad.</div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Información de SPORT CRYB", expanded=False):
    st.write("**Productos:** conjuntos de camiseta + short y camisetas individuales personalizadas.")
    st.write("**Promociones por 10 unidades o más:**")
    st.write("- Conjunto infantil: $14.999 por unidad")
    st.write("- Conjunto adulto/dama: $16.499 por unidad")
    st.write("- Camiseta infantil: $9.999 por unidad")
    st.write("- Camiseta adulto: $11.499 por unidad")
    st.write("**Talles:** infantil del 4 al 16; adulto del S al XXL. Medidas especiales a cotizar.")
    st.write("**Pago:** 50% de seña para iniciar y 50% al finalizar.")
    st.write("**Producción:** 20 a 25 días hábiles desde la confirmación.")
    st.write("**Envíos:** únicamente a toda Argentina.")
    st.write("**Atención:** lunes a viernes de 09:00 a 18:00 h; sábados de 09:00 a 13:00 h.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! 👋 Bienvenido/a a SPORT CRYB ⚽ Soy el asistente virtual. Podés consultarme precios, talles, envíos, medios de pago y tiempos de producción."}
    ]
if "context" not in st.session_state:
    st.session_state.context = {"producto": None, "categoria": None, "cantidad": None}

st.markdown("### 💬 Chat de consultas")
st.caption("Consultá lo que necesites. Las respuestas se generan automáticamente.")

quick = [
    ("💲 Ver precios", "Quiero consultar precios"),
    ("👕 Talles", "¿Qué talles trabajan?"),
    ("🚚 Envíos", "¿Hacen envíos?"),
    ("💳 Medios de pago", "¿Qué medios de pago aceptan?"),
    ("🕒 Horarios", "¿Qué días y horarios trabajan?"),
    ("📦 Hacer un pedido", "Quiero hacer un pedido"),
]
cols = st.columns(3)
for i, (label, prompt_text) in enumerate(quick):
    if cols[i % 3].button(label, use_container_width=True, key=f"quick_{i}"):
        st.session_state.pending_prompt = prompt_text

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="⚽" if msg["role"] == "assistant" else "🙂"):
        st.markdown(msg["content"])

prompt = st.chat_input("Escribí tu consulta acá…")
if not prompt and "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    answer = responder(prompt, st.session_state.context)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown('<div class="small-note">SPORT CRYB · Asistente virtual de consultas · Envíos únicamente a Argentina</div>', unsafe_allow_html=True)
