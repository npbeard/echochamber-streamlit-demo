from __future__ import annotations

import importlib
import time

import streamlit as st  # type: ignore

try:
    echochamber = importlib.import_module("echochamber")
    echochamber_utils = importlib.import_module("echochamber.utils")

    NoirVoice = echochamber.NoirVoice
    Persona = echochamber.Persona
    SciFiVoice = echochamber.SciFiVoice
    TherapyVoice = echochamber.TherapyVoice
    EngineConfig = echochamber_utils.EngineConfig
except ModuleNotFoundError:
    st.set_page_config(
        page_title="echochamber demo", page_icon="🌌", layout="wide"
    )
    st.error(
        "The `echochamber` package is not installed. "
        "Install the library from TestPyPI before running this app."
    )
    st.code(
        "pip install --extra-index-url https://test.pypi.org/simple/ "
        "echochamber"
    )
    st.stop()
st.set_page_config(
    page_title="echochamber demo", page_icon="🌌", layout="wide"
)

VOICE_MAP = {
    "noir": NoirVoice,
    "scifi": SciFiVoice,
    "therapy": TherapyVoice,
}

EXAMPLES = {
    "Weather report":
        "The weather is quite rainy today.",
    "Presentation pitch":
        "Our group built a Python package for text personas.",
    "Stressful deadline":
        "We need to finish the PDF and the upload tonight.",
}


def build_persona(
    name: str, voice_name: str, include_time: bool, chaos: bool
) -> Persona:
    """Create the demo persona with a deterministic set of tags."""
    config = EngineConfig(include_time=include_time, chaos=chaos)
    persona = Persona(name=name, voice=VOICE_MAP[voice_name](), config=config)
    persona.add_tags("streamlit", "demo", voice_name)
    if chaos:
        persona.add_tags("regex")
    if include_time:
        persona.add_tags("datetime")
    return persona


st.title("🌌 echochamber demo")
st.caption(
    "Separate Streamlit project that consumes "
    "the published `echochamber` package."
)

with st.sidebar:
    st.header("Controls")
    example_name = st.selectbox("Example text", list(EXAMPLES))
    persona_name = st.text_input("Persona name", value="StreamlitUser")
    voice_name = st.selectbox("Voice", ["noir", "scifi", "therapy"])
    layers = st.slider("Layers (recursion)", min_value=1, max_value=5, value=1)
    chunk_size = st.slider(
        "Chunk size (generator streaming)", min_value=5, max_value=40, value=16
    )
    chaos = st.checkbox("Chaos mode (regex)", value=False)
    intensity = st.slider("Chaos intensity", min_value=1, max_value=3, value=1)
    include_time = st.checkbox("Include timestamp", value=True)
    stream_output = st.checkbox("Animate generator output", value=True)

text = st.text_area("Input text", value=EXAMPLES[example_name], height=140)

persona = build_persona(
    name=persona_name,
    voice_name=voice_name,
    include_time=include_time,
    chaos=chaos,
)

left_col, right_col = st.columns([3, 2])

with left_col:
    st.subheader("Transformation")
    if st.button("Echo", type="primary", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            result = persona.echo_once(
                text,
                layers=layers,
                intensity=intensity)
            transformed = result["result"].transformed

            if stream_output:
                placeholder = st.empty()
                streamed_text = ""
                for chunk in persona.echo(
                    text,
                    chunk_size=chunk_size,
                    layers=layers,
                    intensity=intensity,
                ):
                    streamed_text += chunk
                    placeholder.markdown(streamed_text)
                    time.sleep(0.03)
            else:
                st.markdown(transformed)

            st.divider()
            st.subheader("Result details")
            st.write(
                {
                    "original": result["result"].original,
                    "transformed": transformed,
                    "timestamp": result["result"].timestamp,
                    "seconds": round(result["seconds"], 6),
                }
            )

with right_col:
    st.subheader("Library concepts in use")
    st.markdown(
        """
        - `Persona` and voice classes show composition and instances.
        - `EngineConfig` is an immutable dataclass passed into the package.
        - `persona.echo()` streams chunks with a generator.
        - `layers` drives recursion inside the library.
        - `chaos` and `intensity` trigger regex-based transformations.
        - `include_time` shows datetime formatting.
        """
    )

    st.subheader("Current persona")
    st.write(repr(persona))
    st.write({"tags": list(persona), "voice": voice_name, "layers": layers})

    st.subheader("How to run")
    st.code("streamlit run app.py")
