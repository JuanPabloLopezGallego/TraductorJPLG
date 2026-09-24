import os
import re
import glob
import time

import streamlit as st
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from gtts import gTTS
from googletrans import Translator


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="VoxTranslate",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

    :root {
        --cream: #fbf8f3;
        --paper: #ffffff;
        --ink: #1a1424;
        --ink-soft: #514a68;
        --muted: #8d87a3;
        --line: #ece7f1;
        --violet: #7c3aed;
        --violet-deep: #4c1d95;
        --violet-soft: #f5f1ff;
        --coral: #f43f5e;
        --coral-soft: #fff0f3;
        --mint: #10b981;
        --mint-soft: #ecfdf5;
    }

    html, body, .stApp, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(124, 58, 237, 0.14), transparent 38%),
            radial-gradient(circle at 100% 100%, rgba(244, 63, 94, 0.10), transparent 42%),
            radial-gradient(circle at 50% 40%, rgba(245, 158, 11, 0.05), transparent 55%),
            var(--cream);
        color: var(--ink);
    }

    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    .block-container {
        max-width: 880px !important;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        margin: 0 auto;
    }

    h1, h2, h3, h4, h5, p, label, span, div { color: var(--ink); }

    /* ---------- BRAND ---------- */

    .brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 2.5rem;
        animation: fadeUp 0.5s ease both;
    }

    .brand-mark {
        width: 44px;
        height: 44px;
        border-radius: 13px;
        display: grid;
        place-items: center;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 55%, #f43f5e 130%);
        box-shadow: 0 8px 22px rgba(124, 58, 237, 0.30);
        font-size: 1.2rem;
    }

    .brand-name {
        font-weight: 800;
        font-size: 1.05rem;
        letter-spacing: -0.02em;
        color: var(--ink);
        line-height: 1;
    }

    .brand-tag {
        font-size: 0.78rem;
        color: var(--muted);
        font-weight: 500;
        margin-top: 0.25rem;
    }

    /* ---------- HERO ---------- */

    .hero-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-weight: 400;
        font-size: clamp(2.4rem, 6vw, 3.8rem);
        line-height: 1.02;
        letter-spacing: -0.03em;
        color: var(--ink);
        margin: 0 0 1rem 0;
        animation: fadeUp 0.6s ease both;
    }

    .hero-title em {
        font-style: italic;
        color: #7c3aed;
        background: linear-gradient(120deg, #7c3aed, #f43f5e);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-sub {
        font-size: 1.02rem;
        color: var(--ink-soft);
        line-height: 1.6;
        max-width: 560px;
        margin: 0 0 2rem 0;
        animation: fadeUp 0.7s ease both;
    }

    /* ---------- SECTION LABEL ---------- */

    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 1.5rem 0 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .section-label::before {
        content: "";
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--violet);
        box-shadow: 0 0 0 4px var(--violet-soft);
    }

    /* ---------- MIC HINT ---------- */

    .mic-hint {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.38rem 0.85rem;
        background: var(--mint-soft);
        border: 1px solid #c9f1dd;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #047857;
        margin-bottom: 1rem;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        position: relative;
    }

    .live-dot::after {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background: #10b981;
        animation: pulseRing 1.8s ease-out infinite;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        width: 100%;
        min-height: 54px;
        border-radius: 14px;
        border: 0;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 55%, #f43f5e 130%);
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: -0.01em;
        box-shadow: 0 10px 24px rgba(124, 58, 237, 0.28);
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.06);
        box-shadow: 0 14px 32px rgba(124, 58, 237, 0.35);
    }

    .stButton > button p, .stButton > button span {
        color: #ffffff !important;
    }

    /* ---------- TEXTAREA ---------- */

    .stTextArea textarea {
        background: var(--paper) !important;
        border: 1.5px solid var(--line) !important;
        border-radius: 14px !important;
        padding: 0.9rem 1rem !important;
        font-size: 15px !important;
        color: var(--ink) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .stTextArea textarea:focus {
        border-color: var(--violet) !important;
        box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.12) !important;
        outline: none !important;
    }

    /* ---------- SELECTBOX ---------- */

    div[data-baseweb="select"] > div {
        background: var(--paper) !important;
        border: 1.5px solid var(--line) !important;
        border-radius: 14px !important;
        min-height: 50px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #d8cfe8 !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--violet) !important;
        box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.12) !important;
    }

    /* ---------- RESULT ---------- */

    .result-block {
        background: var(--violet-soft);
        border: 1px solid #e0d5ff;
        border-radius: 18px;
        padding: 1.15rem 1.25rem;
        margin-top: 0.75rem;
        animation: fadeUp 0.4s ease both;
    }

    .result-block.coral {
        background: var(--coral-soft);
        border-color: #ffd6de;
    }

    .result-block.mint {
        background: var(--mint-soft);
        border-color: #c9f1dd;
    }

    .result-tag {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--violet-deep);
        margin-bottom: 0.5rem;
        display: block;
    }

    .result-block.coral .result-tag { color: #be123c; }
    .result-block.mint .result-tag { color: #047857; }

    .result-body {
        font-size: 1.22rem;
        line-height: 1.45;
        font-weight: 600;
        color: var(--ink);
        letter-spacing: -0.015em;
    }

    /* ---------- MISC ---------- */

    hr {
        border: none;
        border-top: 1px solid var(--line);
        margin: 1.75rem 0;
    }

    audio {
        width: 100%;
        border-radius: 12px;
        margin-top: 0.5rem;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1px solid var(--line) !important;
    }

    details {
        background: var(--paper) !important;
        border: 1px solid var(--line) !important;
        border-radius: 12px !important;
    }

    iframe[title*="bokeh"],
    div[data-testid="stCustomComponentV1"] {
        display: flex;
        justify-content: center;
    }

    /* ---------- ANIMACIONES ---------- */

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseRing {
        0%   { transform: scale(1); opacity: 0.7; }
        100% { transform: scale(2.2); opacity: 0; }
    }

    /* ---------- FOOTER ---------- */

    .vx-footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--line);
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.7;
    }

    .vx-footer strong { color: var(--ink-soft); }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATOS
# ============================================================

LANGUAGES = {
    "Español":  {"flag": "🇪🇸", "code": "es",    "bcp47": "es-ES"},
    "Inglés":   {"flag": "🇺🇸", "code": "en",    "bcp47": "en-US"},
    "Bengalí":  {"flag": "🇧🇩", "code": "bn",    "bcp47": "bn-BD"},
    "Coreano":  {"flag": "🇰🇷", "code": "ko",    "bcp47": "ko-KR"},
    "Mandarín": {"flag": "🇨🇳", "code": "zh-cn", "bcp47": "zh-CN"},
    "Japonés":  {"flag": "🇯🇵", "code": "ja",    "bcp47": "ja-JP"},
    "Griego":   {"flag": "🇬🇷", "code": "el",    "bcp47": "el-GR"},
}

ACCENTS = {
    "🌎 Automático":        "com",
    "🇲🇽 Español (México)": "com.mx",
    "🇬🇧 Reino Unido":      "co.uk",
    "🇺🇸 Estados Unidos":   "com",
    "🇨🇦 Canadá":           "ca",
    "🇦🇺 Australia":        "com.au",
    "🇮🇪 Irlanda":          "ie",
    "🇿🇦 Sudáfrica":        "co.za",
}


# ============================================================
# FUNCIONES
# ============================================================

def clean_filename(text):
    name = re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ_-]+", "_", text[:35]).strip("_")
    return name or "traduccion"


def text_to_speech(input_language, output_language, text, tld):
    translator = Translator()
    translation = translator.translate(
        text, src=input_language, dest=output_language
    )
    translated_text = translation.text
    filename = clean_filename(translated_text)
    audio_path = os.path.join(TEMP_FOLDER, filename + ".mp3")

    speech = gTTS(
        text=translated_text,
        lang=output_language,
        tld=tld,
        slow=False,
    )
    speech.save(audio_path)
    return audio_path, translated_text


def remove_old_files(days=7):
    now = time.time()
    max_age = days * 86400
    for path in glob.glob(os.path.join(TEMP_FOLDER, "*.mp3")):
        try:
            if os.stat(path).st_mtime < now - max_age:
                os.remove(path)
        except OSError:
            pass


remove_old_files(7)


# ============================================================
# ESTADO DE SESIÓN
# ============================================================

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "mic_error" not in st.session_state:
    st.session_state.mic_error = ""
if "_last_voice" not in st.session_state:
    st.session_state._last_voice = ""


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-mark">🎙️</div>
        <div>
            <div class="brand-name">VoxTranslate</div>
            <div class="brand-tag">Traducción por voz en segundos</div>
        </div>
    </div>

    <h1 class="hero-title">
        Habla. Traduce. <em>Escucha.</em>
    </h1>

    <p class="hero-sub">
        Di una frase, elige el idioma y obtén al instante su traducción
        con voz natural. Sin complicaciones, sin pasos extra.
    </p>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# IDIOMAS
# ============================================================

st.markdown('<div class="section-label">Idiomas</div>', unsafe_allow_html=True)

col_in, col_out = st.columns(2)

with col_in:
    in_lang_name = st.selectbox(
        "Hablas en",
        list(LANGUAGES.keys()),
        index=0,
        key="in_lang",
    )

with col_out:
    out_lang_name = st.selectbox(
        "Traducir a",
        list(LANGUAGES.keys()),
        index=1,
        key="out_lang",
    )

input_language = LANGUAGES[in_lang_name]["code"]
output_language = LANGUAGES[out_lang_name]["code"]
input_bcp47 = LANGUAGES[in_lang_name]["bcp47"]

accent_name = st.selectbox(
    "Acento de la voz",
    list(ACCENTS.keys()),
    index=0,
    key="accent",
)
tld = ACCENTS[accent_name]


# ============================================================
# MICRÓFONO
# ============================================================

st.markdown('<div class="section-label">Tu voz</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="mic-hint">
        <span class="live-dot"></span>
        Presiona el botón y habla con claridad
    </div>
    """,
    unsafe_allow_html=True,
)

stt_button = Button(
    label="🎤  Comenzar a escuchar",
    width=440,
    height=58,
    button_type="primary",
)

stt_button.js_on_event(
    "button_click",
    CustomJS(
        code=f"""
        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {{
            document.dispatchEvent(new CustomEvent("GET_TEXT", {{
                detail: "ERROR: Este navegador no soporta reconocimiento de voz."
            }}));
        }} else {{
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "{input_bcp47}";
            recognition.maxAlternatives = 1;

            recognition.onresult = function(event) {{
                let value = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {{
                    if (event.results[i].isFinal) {{
                        value += event.results[i][0].transcript;
                    }}
                }}
                if (value.trim() !== "") {{
                    document.dispatchEvent(new CustomEvent("GET_TEXT", {{ detail: value }}));
                }}
            }};

            recognition.onerror = function(event) {{
                document.dispatchEvent(new CustomEvent("GET_TEXT", {{
                    detail: "ERROR: " + event.error
                }}));
            }};

            recognition.start();
        }}
        """,
    ),
)

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=90,
    debounce_time=0,
)

if result and "GET_TEXT" in result:
    text = str(result.get("GET_TEXT")).strip()
    if text and text != st.session_state._last_voice:
        st.session_state._last_voice = text
        if text.startswith("ERROR:"):
            st.session_state.mic_error = text
        else:
            st.session_state.input_text = text
            st.session_state.mic_error = ""

if st.session_state.mic_error:
    st.warning(
        "No se pudo acceder al micrófono. Revisa los permisos del navegador "
        "o escribe el texto directamente abajo."
    )


# ============================================================
# TEXTO
# ============================================================

st.markdown(
    '<div class="section-label">Texto a traducir</div>',
    unsafe_allow_html=True,
)

user_text = st.text_area(
    "Texto",
    key="input_text",
    placeholder="Aquí aparecerá tu voz. También puedes escribir directamente.",
    height=110,
    label_visibility="collapsed",
)


# ============================================================
# TRADUCCIÓN
# ============================================================

if user_text.strip():

    st.markdown("")

    if st.button("✨  Traducir y generar audio", use_container_width=True):
        try:
            with st.spinner("Traduciendo y preparando el audio..."):
                audio_path, output_text = text_to_speech(
                    input_language,
                    output_language,
                    user_text,
                    tld,
                )

            st.markdown(
                f"""
                <div class="result-block coral">
                    <span class="result-tag">Original · {in_lang_name}</span>
                    <div class="result-body">{user_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="result-block">
                    <span class="result-tag">Traducción · {out_lang_name}</span>
                    <div class="result-body">{output_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-label">Escucha el resultado</div>',
                unsafe_allow_html=True,
            )

            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")

            st.markdown(
                """
                <div class="result-block mint">
                    <span class="result-tag">Listo</span>
                    <div class="result-body">
                        Tu traducción está lista para escuchar.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception as error:
            st.error(
                "No se pudo completar la traducción. Comprueba tu conexión "
                "a Internet e inténtalo de nuevo."
            )
            with st.expander("Ver detalle técnico"):
                st.code(str(error))


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="vx-footer">
        🎙️ <strong>VoxTranslate</strong> · Traducción por voz
    </div>
    """,
    unsafe_allow_html=True,
)
