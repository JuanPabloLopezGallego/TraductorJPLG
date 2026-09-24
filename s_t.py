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

    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --primary-soft: #eff6ff;
        --text: #172033;
        --muted: #64748b;
        --heading: #102a56;
        --surface: #ffffff;
        --surface-soft: #f8fafc;
        --border: #dbe4ef;
        --success: #15803d;
    }

    /* ---------- FONDO ---------- */

    .stApp {
        background: #f4f7fb;
        color: var(--text);
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 8% 0%,
                rgba(37, 99, 235, 0.08),
                transparent 28%
            ),
            linear-gradient(
                180deg,
                #f9fbff 0%,
                #f4f7fb 100%
            );
    }

    [data-testid="stHeader"] {
        background: rgba(249, 251, 255, 0.92);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    /* ---------- TIPOGRAFÍA ---------- */

    h1, h2, h3, h4 {
        color: var(--heading) !important;
        letter-spacing: -0.025em;
    }

    h1 {
        font-size: 2.7rem !important;
        font-weight: 850 !important;
        line-height: 1.05 !important;
    }

    h2 {
        font-weight: 800 !important;
    }

    h3 {
        font-weight: 750 !important;
    }

    p, label, span {
        color: var(--text);
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
        box-shadow: 5px 0 20px rgba(15, 23, 42, 0.04);
    }

    section[data-testid="stSidebar"] > div {
        background: #ffffff;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--heading) !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #475569 !important;
    }

    /* ---------- SELECTBOX ---------- */

    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        min-height: 44px;
        color: var(--text) !important;
    }

    div[data-baseweb="select"] input {
        color: var(--text) !important;
    }

    /* ---------- BOTONES ---------- */

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 13px;
        border: 1px solid var(--primary);
        background: linear-gradient(
            135deg,
            #2563eb,
            #3b82f6
        );
        color: white !important;
        font-size: 15px;
        font-weight: 750;
        box-shadow:
            0 6px 16px rgba(37, 99, 235, 0.16);
        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            background 0.18s ease;
    }

    .stButton > button p,
    .stButton > button span {
        color: white !important;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #1d4ed8,
            #2563eb
        );
        transform: translateY(-1px);
        box-shadow:
            0 9px 22px rgba(37, 99, 235, 0.23);
    }

    /* ---------- INPUTS ---------- */

    textarea,
    input {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
    }

    textarea:focus,
    input:focus {
        border-color: var(--primary) !important;
        box-shadow:
            0 0 0 3px rgba(37, 99, 235, 0.10) !important;
    }

    /* ---------- TARJETAS ---------- */

    .hero-card {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f5f9ff 100%
        );
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 2.2rem 2.4rem;
        margin-bottom: 1.5rem;
        box-shadow:
            0 10px 35px rgba(15, 23, 42, 0.06);
    }

    .hero-badge {
        display: inline-block;
        padding: 0.4rem 0.75rem;
        border-radius: 999px;
        background: var(--primary-soft);
        color: var(--primary-dark) !important;
        border: 1px solid #bfdbfe;
        font-size: 0.82rem;
        font-weight: 750;
        margin-bottom: 0.9rem;
    }

    .hero-title {
        color: var(--heading);
        font-size: 2.7rem;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: 0.7rem;
    }

    .hero-description {
        color: #64748b !important;
        font-size: 1.05rem;
        line-height: 1.65;
        max-width: 720px;
        margin-bottom: 0;
    }

    .feature-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.3rem;
        min-height: 145px;
        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.04);
    }

    .feature-icon {
        font-size: 1.65rem;
        margin-bottom: 0.5rem;
    }

    .feature-title {
        color: var(--heading);
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .feature-text {
        color: #64748b !important;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .result-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.35rem;
        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.045);
        margin-top: 0.7rem;
    }

    .result-label {
        color: #64748b !important;
        font-size: 0.8rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.45rem;
    }

    .result-text {
        color: var(--heading);
        font-size: 1.25rem;
        font-weight: 650;
        line-height: 1.5;
    }

    .status-card {
        background: #ecfdf3;
        border: 1px solid #bbf7d0;
        border-radius: 14px;
        padding: 0.85rem 1rem;
        color: #166534 !important;
        font-weight: 650;
    }

    .footer-card {
        text-align: center;
        color: #64748b !important;
        font-size: 0.82rem;
        padding-top: 2rem;
    }

    .footer-card strong {
        color: #334155 !important;
    }

    /* ---------- SEPARADORES ---------- */

    hr {
        border: 0;
        border-top: 1px solid #dfe7f1;
        margin: 2rem 0;
    }

    /* ---------- AUDIO ---------- */

    audio {
        width: 100%;
        border-radius: 10px;
    }

    /* ---------- CHECKBOX ---------- */

    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p {
        color: #475569 !important;
    }

    /* ---------- ALERTAS ---------- */

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid var(--border);
    }

    /* ---------- RESPONSIVE ---------- */

    @media (max-width: 700px) {
        .hero-card {
            padding: 1.5rem;
            border-radius: 18px;
        }

        .hero-title,
        h1 {
            font-size: 2rem !important;
        }

        .hero-description {
            font-size: 0.95rem;
        }
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
            font-size: 1.45rem;
            font-weight: 850;
            color: #102a56;
            margin-bottom: 0.2rem;
        ">
            🎙️ VoxTranslate
        </div>
        <div style="
            color: #64748b;
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 1.3rem;
        ">
            Traducción por voz rápida y sencilla.
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
            🎙️ TRADUCCIÓN POR VOZ
        </div>

        <div class="hero-title">
            Habla. Traduce. Escucha.
        </div>

        <p class="hero-description">
            Convierte tu voz en texto, tradúcelo al idioma que
            necesitas y escucha el resultado en segundos.
            Una experiencia sencilla pensada para hablar sin complicaciones.
        </p>

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

st.markdown("### 🎙️ Habla para comenzar")

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
                        ✓ Tu traducción está lista para escuchar.
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
            padding: 1rem 1.2rem;
            border-radius: 14px;
            background: #ffffff;
            border: 1px solid #dbe4ef;
            color: #64748b;
        ">
            👋 <strong style="color:#102a56;">Listo para comenzar.</strong>
            Presiona el botón de arriba y habla para iniciar.
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
        🎙️ <strong>VoxTranslate</strong><br>
        Una experiencia de traducción por voz.
    </div>
    """,
    unsafe_allow_html=True,
)
