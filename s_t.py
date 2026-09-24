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
    initial_sidebar_state="expanded",
)

TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)


# ============================================================
# ESTILOS — DISEÑO PROFESIONAL / MODO CLARO
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #818cf8;
        --accent: #06b6d4;
        --accent-2: #a855f7;
        --text: #0f172a;
        --muted: #64748b;
        --heading: #0b1437;
        --surface: #ffffff;
        --surface-soft: #f8fafc;
        --border: #e2e8f0;
        --success: #10b981;
        --gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        --gradient-soft: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 50%, #ecfeff 100%);
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ---------- FONDO ---------- */

    .stApp {
        background: #f7f8fc;
        color: var(--text);
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(1000px 500px at 10% -10%, rgba(99, 102, 241, 0.10), transparent 60%),
            radial-gradient(900px 500px at 100% 0%, rgba(6, 182, 212, 0.08), transparent 55%),
            radial-gradient(700px 500px at 50% 100%, rgba(168, 85, 247, 0.07), transparent 60%),
            linear-gradient(180deg, #fbfcff 0%, #f5f7fc 100%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu, footer { visibility: hidden; }

    /* ---------- TIPOGRAFÍA ---------- */

    h1, h2, h3, h4, .hero-title, .feature-title, .result-text {
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        color: var(--heading) !important;
        letter-spacing: -0.03em;
    }

    h1 { font-size: 2.6rem !important; font-weight: 700 !important; line-height: 1.05 !important; }
    h2 { font-weight: 700 !important; letter-spacing: -0.025em; }
    h3 {
        font-weight: 700 !important;
        font-size: 1.35rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    p, label, span { color: var(--text); }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-right: 1px solid var(--border);
        box-shadow: 5px 0 30px rgba(15, 23, 42, 0.04);
    }

    section[data-testid="stSidebar"] > div { background: transparent; }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--heading) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #475569 !important;
    }

    /* ---------- SELECTBOX ---------- */

    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        min-height: 46px;
        color: var(--text) !important;
        transition: border-color 0.18s ease, box-shadow 0.18s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: var(--primary-light) !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.08) !important;
    }

    div[data-baseweb="select"] input { color: var(--text) !important; }

    /* ---------- BOTONES ---------- */

    .stButton > button {
        width: 100%;
        min-height: 50px;
        border-radius: 14px;
        border: none;
        background: var(--gradient);
        background-size: 200% 200%;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: -0.01em;
        box-shadow:
            0 8px 22px rgba(99, 102, 241, 0.25),
            0 2px 6px rgba(99, 102, 241, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
        transition: transform 0.2s ease, box-shadow 0.25s ease, background-position 0.5s ease;
        position: relative;
        overflow: hidden;
    }

    .stButton > button p,
    .stButton > button span { color: #ffffff !important; }

    .stButton > button:hover {
        background-position: 100% 0%;
        transform: translateY(-2px);
        box-shadow:
            0 14px 30px rgba(99, 102, 241, 0.35),
            0 4px 10px rgba(99, 102, 241, 0.20),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .stButton > button:active { transform: translateY(0); }

    /* ---------- INPUTS ---------- */

    textarea, input {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        transition: all 0.18s ease;
    }

    textarea:focus, input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.12) !important;
    }

    /* ---------- HERO ---------- */

    .hero-card {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(600px 300px at 90% 10%, rgba(168, 85, 247, 0.14), transparent 60%),
            radial-gradient(500px 300px at 10% 90%, rgba(6, 182, 212, 0.12), transparent 60%),
            linear-gradient(135deg, #ffffff 0%, #fbfaff 100%);
        border: 1px solid var(--border);
        border-radius: 28px;
        padding: 2.6rem 2.6rem 2.4rem;
        margin-bottom: 1.6rem;
        box-shadow:
            0 20px 50px rgba(15, 23, 42, 0.08),
            0 4px 12px rgba(15, 23, 42, 0.04);
        animation: fadeUp 0.6s ease both;
    }

    .hero-card::before {
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 30px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(99,102,241,0.5), rgba(6,182,212,0.3), rgba(168,85,247,0.5));
        -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        background: linear-gradient(135deg, #eef2ff, #f5f3ff);
        color: var(--primary-dark) !important;
        border: 1px solid #c7d2fe;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.12);
    }

    .hero-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #06b6d4);
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        animation: pulse 1.8s ease-in-out infinite;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.02;
        margin-bottom: 0.85rem;
        background: linear-gradient(135deg, #0b1437 0%, #4f46e5 60%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-description {
        color: #64748b !important;
        font-size: 1.06rem;
        line-height: 1.7;
        max-width: 720px;
        margin-bottom: 0;
    }

    /* ---------- FEATURE CARDS ---------- */

    .feature-card {
        position: relative;
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.5rem 1.4rem;
        min-height: 165px;
        box-shadow:
            0 6px 20px rgba(15, 23, 42, 0.05),
            0 1px 2px rgba(15, 23, 42, 0.04);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        animation: fadeUp 0.6s ease both;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        border-color: #c7d2fe;
        box-shadow:
            0 18px 40px rgba(99, 102, 241, 0.14),
            0 4px 10px rgba(15, 23, 42, 0.05);
    }

    .feature-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        font-size: 1.4rem;
        margin-bottom: 0.9rem;
        box-shadow: inset 0 0 0 1px rgba(99, 102, 241, 0.15);
    }

    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .feature-text {
        color: #64748b !important;
        font-size: 0.92rem;
        line-height: 1.55;
    }

    /* ---------- RESULT CARDS ---------- */

    .result-card {
        position: relative;
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.5rem 1.6rem;
        box-shadow:
            0 8px 24px rgba(15, 23, 42, 0.06),
            0 2px 4px rgba(15, 23, 42, 0.03);
        margin-top: 0.75rem;
        animation: fadeUp 0.5s ease both;
    }

    .result-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 20%;
        bottom: 20%;
        width: 4px;
        border-radius: 4px;
        background: var(--gradient);
    }

    .result-label {
        color: #64748b !important;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.55rem;
    }

    .result-text {
        color: var(--heading);
        font-size: 1.3rem;
        font-weight: 600;
        line-height: 1.5;
    }

    /* ---------- STATUS ---------- */

    .status-card {
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdfa 100%);
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 1rem 1.15rem;
        color: #065f46 !important;
        font-weight: 600;
        margin-top: 1rem;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.10);
        animation: fadeUp 0.5s ease both;
    }

    .status-card::before {
        content: '';
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 0 5px rgba(16, 185, 129, 0.18);
        animation: pulse 1.8s ease-in-out infinite;
        flex-shrink: 0;
    }

    /* ---------- MIC WAVE (decorativo) ---------- */

    .mic-wave {
        display: inline-flex;
        align-items: flex-end;
        gap: 3px;
        height: 22px;
        margin-top: 1.2rem;
        vertical-align: middle;
    }

    .mic-wave span {
        display: block;
        width: 4px;
        background: linear-gradient(180deg, #6366f1, #06b6d4);
        border-radius: 2px;
        animation: wave 1.1s ease-in-out infinite;
    }

    .mic-wave span:nth-child(1) { height: 40%; animation-delay: 0s; }
    .mic-wave span:nth-child(2) { height: 80%; animation-delay: 0.15s; }
    .mic-wave span:nth-child(3) { height: 55%; animation-delay: 0.3s; }
    .mic-wave span:nth-child(4) { height: 95%; animation-delay: 0.45s; }
    .mic-wave span:nth-child(5) { height: 45%; animation-delay: 0.6s; }

    /* ---------- FOOTER ---------- */

    .footer-card {
        text-align: center;
        color: #64748b !important;
        font-size: 0.85rem;
        padding-top: 2rem;
        line-height: 1.7;
    }

    .footer-card strong {
        color: #334155 !important;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.01em;
    }

    /* ---------- SEPARADORES ---------- */

    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #dfe7f1 20%, #dfe7f1 80%, transparent);
        margin: 2.2rem 0;
    }

    /* ---------- AUDIO ---------- */

    audio {
        width: 100%;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    }

    /* ---------- CHECKBOX ---------- */

    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p { color: #475569 !important; }

    /* ---------- ALERTAS ---------- */

    div[data-testid="stAlert"] {
        border-radius: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.03);
    }

    /* ---------- ANIMACIONES ---------- */

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1);    opacity: 1; }
        50%      { transform: scale(1.15); opacity: 0.85; }
    }

    @keyframes wave {
        0%, 100% { transform: scaleY(0.5); }
        50%      { transform: scaleY(1);   }
    }

    /* ---------- RESPONSIVE ---------- */

    @media (max-width: 700px) {
        .hero-card { padding: 1.6rem; border-radius: 20px; }
        .hero-title, h1 { font-size: 2.1rem !important; }
        .hero-description { font-size: 0.96rem; }
        .result-text { font-size: 1.15rem; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATOS
# ============================================================

LANGUAGES = {
    "🇪🇸 Español": "es",
    "🇺🇸 Inglés": "en",
    "🇧🇩 Bengali": "bn",
    "🇰🇷 Coreano": "ko",
    "🇨🇳 Mandarín": "zh-cn",
    "🇯🇵 Japonés": "ja",
    "🇬🇷 Griego": "el",
}

ACCENTS = {
    "🌎 Predeterminado": "com",
    "🇪🇸 Español": "com.mx",
    "🇬🇧 Reino Unido": "co.uk",
    "🇺🇸 Estados Unidos": "com",
    "🇨🇦 Canadá": "ca",
    "🇦🇺 Australia": "com.au",
    "🇮🇪 Irlanda": "ie",
    "🇿🇦 Sudáfrica": "co.za",
}


# ============================================================
# FUNCIONES
# ============================================================

def clean_filename(text):
    """Crea un nombre de archivo seguro y corto."""
    name = re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ_-]+", "_", text[:35])
    name = name.strip("_")

    if not name:
        name = "traduccion"

    return name


def text_to_speech(input_language, output_language, text, tld):
    """Traduce el texto y genera el audio."""
    translator = Translator()

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language,
    )

    translated_text = translation.text
    filename = clean_filename(translated_text)

    audio_path = os.path.join(
        TEMP_FOLDER,
        filename + ".mp3",
    )

    speech = gTTS(
        text=translated_text,
        lang=output_language,
        tld=tld,
        slow=False,
    )

    speech.save(audio_path)

    return audio_path, translated_text


def remove_old_files(days=7):
    """Elimina audios temporales antiguos."""
    mp3_files = glob.glob(
        os.path.join(TEMP_FOLDER, "*.mp3")
    )

    now = time.time()
    max_age = days * 86400

    for file_path in mp3_files:
        try:
            if os.stat(file_path).st_mtime < now - max_age:
                os.remove(file_path)
        except OSError:
            pass


# ============================================================
# LIMPIEZA
# ============================================================

remove_old_files(7)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            display:flex; align-items:center; gap:0.7rem;
            margin-bottom: 0.35rem;
        ">
            <div style="
                width: 38px; height: 38px; border-radius: 12px;
                background: linear-gradient(135deg, #6366f1, #06b6d4);
                display: flex; align-items: center; justify-content: center;
                font-size: 1.15rem;
                box-shadow: 0 6px 16px rgba(99,102,241,0.35);
            ">🎙️</div>
            <div style="
                font-family: 'Space Grotesk', sans-serif;
                font-size: 1.4rem;
                font-weight: 700;
                color: #0b1437;
                letter-spacing: -0.02em;
            ">VoxTranslate</div>
        </div>
        <div style="
            color: #64748b;
            font-size: 0.88rem;
            line-height: 1.55;
            margin-bottom: 1.4rem;
        ">
            Traducción por voz rápida y elegante.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### ⚙️ Configuración")

    st.caption(
        "Primero habla, después elige los idiomas "
        "y finalmente genera la traducción."
    )

    st.markdown("#### 🌐 Idiomas")

    in_lang_name = st.selectbox(
        "Idioma de entrada",
        list(LANGUAGES.keys()),
        index=0,
    )

    out_lang_name = st.selectbox(
        "Idioma de salida",
        list(LANGUAGES.keys()),
        index=1,
    )

    st.markdown("#### 🔊 Voz")

    accent_name = st.selectbox(
        "Acento de pronunciación",
        list(ACCENTS.keys()),
        index=0,
    )

    st.divider()

    st.markdown("#### 💡 Consejos")

    st.info(
        "Habla cerca del micrófono y utiliza frases "
        "claras para mejorar el reconocimiento."
    )

    st.caption("VoxTranslate · Proyecto académico")


input_language = LANGUAGES[in_lang_name]
output_language = LANGUAGES[out_lang_name]
tld = ACCENTS[accent_name]


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-badge">
            TRADUCCIÓN POR VOZ
        </div>
        <div class="hero-title">
            Habla. Traduce. Escucha.
        </div>
        <p class="hero-description">
            Convierte tu voz en texto, tradúcela al idioma que necesitas
            y escúchala al instante. Una experiencia sencilla pensada
            para hablar sin complicaciones.
        </p>
        <div class="mic-wave" aria-hidden="true">
            <span></span><span></span><span></span><span></span><span></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FLUJO DE USO
# ============================================================

st.markdown("### ✨ ¿Cómo funciona?")

feature_1, feature_2, feature_3 = st.columns(3)

with feature_1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎤</div>
            <div class="feature-title">1. Habla</div>
            <div class="feature-text">
                Presiona el botón y di la frase que quieres traducir.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature_2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🌎</div>
            <div class="feature-title">2. Traduce</div>
            <div class="feature-text">
                Selecciona el idioma de origen y el idioma al que quieres traducir.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature_3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔊</div>
            <div class="feature-title">3. Escucha</div>
            <div class="feature-text">
                Genera el audio y escucha cómo se pronuncia la traducción.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()


# ============================================================
# RECONOCIMIENTO DE VOZ
# ============================================================

st.markdown(
    """
    <h3 style="display:flex; align-items:center; gap:0.6rem;">
        <span style="
            display:inline-flex; align-items:center; justify-content:center;
            width:36px; height:36px; border-radius:12px;
            background: linear-gradient(135deg,#eef2ff,#e0e7ff);
            font-size:1.05rem;
            box-shadow: inset 0 0 0 1px rgba(99,102,241,0.15);
        ">🎙️</span>
        Habla para comenzar
    </h3>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Pulsa el botón, espera la señal del navegador y pronuncia "
    "la frase que quieres traducir."
)

stt_button = Button(
    label="🎤  Comenzar a escuchar",
    width=420,
    height=58,
)

stt_button.js_on_event(
    "button_click",
    CustomJS(
        code="""
        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            document.dispatchEvent(
                new CustomEvent(
                    "GET_TEXT",
                    {
                        detail:
                        "ERROR: Este navegador no soporta reconocimiento de voz."
                    }
                )
            );
        } else {

            const recognition = new SpeechRecognition();

            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "es-ES";

            recognition.onresult = function(event) {

                let value = "";

                for (
                    let i = event.resultIndex;
                    i < event.results.length;
                    i++
                ) {
                    if (event.results[i].isFinal) {
                        value += event.results[i][0].transcript;
                    }
                }

                if (value.trim() !== "") {
                    document.dispatchEvent(
                        new CustomEvent(
                            "GET_TEXT",
                            { detail: value }
                        )
                    );
                }
            };

            recognition.onerror = function(event) {

                document.dispatchEvent(
                    new CustomEvent(
                        "GET_TEXT",
                        {
                            detail:
                            "ERROR: " + event.error
                        }
                    )
                );
            };

            recognition.start();
        }
        """,
    ),
)


result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0,
)


# ============================================================
# RESULTADO DEL RECONOCIMIENTO
# ============================================================

if result and "GET_TEXT" in result:

    text = str(result.get("GET_TEXT")).strip()

    if text.startswith("ERROR:"):

        st.error(
            "No fue posible utilizar el reconocimiento de voz. "
            "Comprueba los permisos del micrófono y utiliza un navegador compatible."
        )

    elif text:

        st.markdown("### 📝 Texto reconocido")

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">
                    Tu mensaje
                </div>
                <div class="result-text">
                    {text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ====================================================
        # CONFIGURACIÓN DE TRADUCCIÓN
        # ====================================================

        st.markdown("### 🌎 Configura tu traducción")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Idioma de origen**")
            st.info(in_lang_name)

        with col2:
            st.markdown("**Idioma de destino**")
            st.success(out_lang_name)

        st.markdown("**🔊 Acento de pronunciación**")
        st.caption(accent_name)

        display_output_text = st.checkbox(
            "Mostrar el texto traducido",
            value=True,
        )

        st.markdown("")

        convert = st.button(
            "✨  Traducir y generar audio",
            use_container_width=True,
        )

        # ====================================================
        # TRADUCCIÓN
        # ====================================================

        if convert:

            try:

                with st.spinner(
                    "Traduciendo y preparando el audio..."
                ):

                    audio_path, output_text = text_to_speech(
                        input_language,
                        output_language,
                        text,
                        tld,
                    )

                st.markdown("### ✅ Traducción completada")

                if display_output_text:

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-label">
                                Traducción
                            </div>
                            <div class="result-text">
                                {output_text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("### 🔊 Escucha el resultado")

                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()

                st.audio(
                    audio_bytes,
                    format="audio/mp3",
                )

                st.markdown(
                    """
                    <div class="status-card">
                        Tu traducción está lista para escuchar.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as error:

                st.error(
                    "No se pudo completar la traducción. "
                    "Comprueba tu conexión a Internet y los idiomas seleccionados."
                )

                with st.expander("Ver información técnica"):
                    st.code(str(error))


# ============================================================
# ESTADO INICIAL
# ============================================================

elif not result:

    st.markdown(
        """
        <div style="
            margin-top: 1.5rem;
            padding: 1.15rem 1.3rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #ffffff 0%, #fbfaff 100%);
            border: 1px solid #e2e8f0;
            color: #64748b;
            display: flex; align-items: center; gap: 0.8rem;
            box-shadow: 0 6px 20px rgba(15,23,42,0.05);
            animation: fadeUp 0.5s ease both;
        ">
            <span style="
                display:inline-flex; align-items:center; justify-content:center;
                width:38px; height:38px; border-radius:12px;
                background: linear-gradient(135deg,#eef2ff,#e0e7ff);
                font-size:1.15rem;
            ">👋</span>
            <div>
                <strong style="color:#0b1437; font-family:'Space Grotesk',sans-serif;">
                    Listo para comenzar.
                </strong><br>
                Presiona el botón de arriba y habla para iniciar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer-card">
        <div style="
            display:inline-flex; align-items:center; gap:0.55rem;
            padding: 0.5rem 1rem;
            border-radius: 999px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 14px rgba(15,23,42,0.05);
            margin-bottom: 0.85rem;
        ">
            <span style="
                width: 22px; height: 22px; border-radius: 8px;
                background: linear-gradient(135deg,#6366f1,#06b6d4);
                display: inline-flex; align-items: center; justify-content: center;
                font-size: 0.7rem;
            ">🎙️</span>
            <strong>VoxTranslate</strong>
        </div>
        <div>Una experiencia de traducción por voz.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
