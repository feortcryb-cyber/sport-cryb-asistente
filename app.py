import re
import unicodedata
import streamlit as st

# ============================================================
# SPORT CRYB - CHAT WEB
# Cada visitante tiene su propia sesión de conversación.
# ============================================================

st.set_page_config(
    page_title="SPORT CRYB | Asistente",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

MARCA = "SPORT CRYB"

PRECIOS = {
    "conjunto": {"infantil": 14999, "adulto": 16499},
    "camiseta": {"infantil": 9999, "adulto": 11499},
}

HORARIOS = (
    "📅 Lunes a viernes: de 09:00 a 18:00 h.\n\n"
    "📅 Sábados: de 09:00 a 13:00 h."
)

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[¿?¡!.,;:]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto

def contiene_alguna(texto, palabras):
    return any(p in texto for p in palabras)

def es_saludo(texto):
    return texto in [
        "hola", "holaa", "buenas", "buen dia", "buenos dias",
        "buenas tardes", "buenas noches", "que tal"
    ]

def detectar_producto(texto):
    if contiene_alguna(texto, [
        "conjunto", "camiseta y short", "camiseta mas short",
        "camiseta + short", "remera y short", "remera mas short",
        "uniforme completo", "juego completo", "camiseta short"
    ]):
        return "conjunto"
    if contiene_alguna(texto, [
        "camiseta", "camisetas", "remera", "remeras",
        "solo camiseta", "solo remera"
    ]):
        return "camiseta"
    return None

def detectar_categoria(texto):
    if contiene_alguna(texto, [
        "infantil", "infantiles", "nino", "nina", "ninos", "ninas",
        "nenes", "nenas", "chicos", "chicas", "juvenil", "juveniles"
    ]):
        return "infantil"
    if contiene_alguna(texto, [
        "adulto", "adultos", "adulta", "adultas", "dama", "damas",
        "mujer", "mujeres", "femenino", "femenina", "masculino",
        "masculina"
    ]):
        return "adulto"
    return None

def detectar_cantidad(texto):
    numeros = {
        "un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3,
        "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7,
        "ocho": 8, "nueve": 9, "diez": 10, "once": 11,
        "doce": 12, "quince": 15, "veinte": 20, "treinta": 30,
        "cuarenta": 40, "cincuenta": 50
    }
    match = re.search(r"\b(\d+)\s*(?:unidades|conjuntos|camisetas|remeras|prendas)?\b", texto)
    if match:
        return int(match.group(1))
    for palabra, numero in numeros.items():
        if re.search(r"\b" + palabra + r"\b", texto):
            return numero
    return None

def detectar_destino_internacional(texto):
    paises = [
        "chile", "uruguay", "paraguay", "brasil", "bolivia", "peru",
        "ecuador", "colombia", "venezuela", "mexico", "estados unidos",
        "espana", "italia", "francia", "alemania", "reino unido", "canada"
    ]
    return contiene_alguna(texto, paises)

def respuesta_precio(producto=None, categoria=None, cantidad=None, contexto=None):
    producto = producto or contexto.get("producto")
    categoria = categoria or contexto.get("categoria")
    cantidad = cantidad or contexto.get("cantidad")

    if not producto:
        return "¡Claro! 😊 Trabajamos conjuntos de camiseta + short y camisetas individuales. ¿Cuál te interesa y es para infantil o adulto?"
    if not categoria:
        return "¡Perfecto! 😊 ¿Buscás talle infantil o adulto? Los conjuntos de dama tienen el mismo precio que los de adulto."

    precio = PRECIOS[producto][categoria]
    nombre = "conjunto de camiseta + short" if producto == "conjunto" else "camiseta individual"
    tipo = "infantil" if categoria == "infantil" else "adulto"
    respuesta = f"El precio promocional del {nombre} {tipo} es de ${precio:,.0f} por unidad en pedidos de 10 unidades o más."
    respuesta = respuesta.replace(",", ".")

    if cantidad is not None:
        if cantidad >= 10:
            total = precio * cantidad
            respuesta += f"\n\nPor {cantidad} unidades, el total sería ${total:,.0f}.".replace(",", ".")
        else:
            respuesta += "\n\nPara cantidades menores a 10 unidades, las condiciones y el precio se revisan según el pedido."
    return respuesta + "\n\n¿Querés que te ayudemos a preparar tu pedido?"

def responder(mensaje, contexto):
    texto = normalizar(mensaje)

    producto = detectar_producto(texto)
    categoria = detectar_categoria(texto)
    cantidad = detectar_cantidad(texto)

    if producto:
        contexto["producto"] = producto
    if categoria:
        contexto["categoria"] = categoria
    if cantidad is not None:
        contexto["cantidad"] = cantidad

    if not texto:
        return "¡Hola! 😊 ¿En qué podemos ayudarte?"

    if es_saludo(texto):
        return "¡Hola! 👋 Bienvenido/a a SPORT CRYB ⚽ Somos fabricantes de indumentaria deportiva personalizada. ¿Buscás conjuntos de camiseta + short o camisetas individuales?"

    if contiene_alguna(texto, ["gracias", "muchas gracias"]):
        return "¡De nada! 😊 Gracias por comunicarte con SPORT CRYB ⚽"

    if detectar_destino_internacional(texto):
        return "¡Gracias por consultarnos! 😊 Actualmente realizamos envíos únicamente a toda Argentina 🇦🇷. Por el momento no hacemos envíos internacionales."

    if contiene_alguna(texto, [
        "horario", "horarios", "que dias trabajan", "que dias atienden",
        "cuando trabajan", "cuando atienden", "a que hora abren",
        "a que hora cierran", "estan abiertos", "estan atendiendo",
        "horario de atencion"
    ]):
        return "¡Claro! 😊 Nuestro horario de atención es:\n\n" + HORARIOS + "\n\n¡Estamos para ayudarte con tu pedido de SPORT CRYB! ⚽"

    if contiene_alguna(texto, ["envio", "envios", "hacen entregas", "llega a", "llegan a", "mandan a", "despachan", "correo", "delivery"]):
        return "¡Sí! 😊 Realizamos envíos a toda Argentina 🇦🇷. Decinos de qué localidad sos y te orientamos sobre el envío."

    if contiene_alguna(texto, ["pago", "pagos", "efectivo", "transferencia", "mercado pago", "debito", "tarjeta", "como se paga", "medios de pago", "sena"]):
        return "Aceptamos efectivo, transferencia bancaria, Mercado Pago y tarjeta de débito 😊.\n\nPara iniciar la producción se abona el 50% de seña y el 50% restante cuando el pedido está terminado."

    if contiene_alguna(texto, ["cuanto tardan", "cuanto demora", "demora", "tiempo de entrega", "cuando estaria", "cuando llega", "dias de produccion", "tiempo de produccion"]):
        return "El tiempo estimado de producción es de 20 a 25 días hábiles desde la confirmación del pedido 😊. El envío puede sumar tiempo adicional."

    if contiene_alguna(texto, ["minimo", "cantidad minima", "pedido minimo", "cuantas unidades", "desde cuantas", "puedo pedir una", "puedo comprar una", "hacen por unidad", "por unidad"]):
        return "¡Te cuento! 😊 Los precios promocionales son para pedidos de 10 unidades o más. La cantidad mínima y las condiciones para pedidos menores pueden variar según el producto y el pedido. Decime qué necesitás y cuántas unidades serían, así te orientamos."

    if contiene_alguna(texto, ["talle", "talles", "medida", "medidas", "talles de nene", "talles de dama"]):
        if categoria == "infantil" or contexto.get("categoria") == "infantil":
            return "Trabajamos talles infantiles del 4 al 16 😊. Si necesitás, te ayudamos a elegir según las medidas."
        if categoria == "adulto" or contexto.get("categoria") == "adulto":
            return "Trabajamos talles adultos del S al XXL 😊. Las medidas especiales se cotizan por separado."
        return "Tenemos talles infantiles del 4 al 16 y adultos del S al XXL. Las medidas especiales se cotizan por separado. ¿Buscás talles infantiles o adultos?"

    if contiene_alguna(texto, ["precio", "precios", "cuanto sale", "cuanto cuesta", "valor", "valen", "sale cada", "cuesta cada", "lista de precios"]):
        return respuesta_precio(producto, categoria, cantidad, contexto)

    if contiene_alguna(texto, ["conjunto de dama", "conjuntos de dama", "conjunto para dama", "conjuntos para dama", "conjunto de mujer", "conjuntos de mujer"]):
        contexto["producto"] = "conjunto"
        contexto["categoria"] = "adulto"
        return "¡Sí! 😊 Hacemos conjuntos de dama personalizados. El precio promocional es de $16.499 por conjunto en pedidos de 10 unidades o más. Trabajamos talles adultos del S al XXL. Las medidas especiales se cotizan por separado."

    if contiene_alguna(texto, ["quiero hacer un pedido", "quiero encargar", "quiero pedir", "hacer un pedido", "como hago el pedido", "como encargo", "quiero comprar", "te encargo"]):
        return "¡Genial! 😊 Para confirmar un pedido trabajamos con una seña del 50% para iniciar la producción y el 50% restante cuando el pedido está terminado.\n\nEl tiempo estimado de producción es de 20 a 25 días hábiles desde la confirmación. El envío puede sumar tiempo adicional.\n\nContanos qué producto necesitás y la cantidad para ayudarte a avanzar."

    if producto and categoria:
        return respuesta_precio(producto, categoria, cantidad, contexto)
    if producto:
        return "¡Perfecto! 😊 Trabajamos ese producto personalizado. ¿Lo necesitás en talle infantil o adulto?"

    if contiene_alguna(texto, ["que hacen", "que venden", "informacion", "que productos", "que ofrecen"]):
        return "Somos fabricantes de indumentaria deportiva personalizada. Trabajamos conjuntos de camiseta + short y camisetas individuales, con precios promocionales por cantidad, envíos a toda Argentina y excelente calidad y terminaciones."

    return "¡Gracias por escribir a SPORT CRYB! 😊⚽ Trabajamos conjuntos de camiseta + short y camisetas individuales personalizadas. ¿Querés consultar precios, talles, envíos o tiempos de producción?"

# ----------------------- ESTILOS -----------------------------
st.markdown("""
<style>
:root { --lime: #e7ff36; --ink: #10141d; }
.stApp { background: linear-gradient(180deg, #10141d 0%, #151c28 100%); color: #f6f7fb; }
[data-testid="stHeader"] { background: rgba(16,20,29,0); }
.block-container { max-width: 820px; padding-top: 2rem; padding-bottom: 3rem; }
.brand-card { background: #202633; border: 1px solid #343d4d; border-radius: 22px; padding: 22px; margin-bottom: 18px; }
.brand-kicker { color: var(--lime); font-size: 12px; letter-spacing: 2px; font-weight: 800; }
.brand-title { color: white; font-size: 34px; font-weight: 900; line-height: 1.1; margin: 5px 0; }
.brand-sub { color: #b6bfce; font-size: 14px; }
div[data-testid="stChatMessage"] { background: #202633; border: 1px solid #343d4d; border-radius: 16px; padding: 8px 12px; }
.stButton button { border-radius: 14px; border: 1px solid #596477; background: #202633; color: white; min-height: 44px; }
.stButton button:hover { border-color: #e7ff36; color: #e7ff36; }
div[data-testid="stChatInput"] textarea { background: #202633; color: white; }
.small-note { color: #aab3c2; font-size: 12px; text-align: center; }
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
for i, (label, prompt) in enumerate(quick):
    if cols[i % 3].button(label, use_container_width=True, key=f"quick_{i}"):
        st.session_state.pending_prompt = prompt

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
